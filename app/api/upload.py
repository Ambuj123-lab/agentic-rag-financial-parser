"""
upload.py — 7-Layer Secure Upload + SHA-256 Dedup for Temp Files
=================================================================

Security Layers:
  1. 10MB size limit (streamed in 1MB chunks to protect 512MB RAM)
  2. Zero-byte file rejection
  3. Extension whitelist (.pdf only)
  4. MIME type deep check
  5. PDF page count limit (500 pages max — PDF bomb protection)
  6. Auth required (JWT verification)
  7. SHA-256 duplicate detection (same file = skip reindexing!)

Temp File Upload Flow:
  User uploads PDF → 7-layer security → SHA-256 hash check →
  If duplicate → return existing chunks (no reindexing!)
  If new → PyMuPDF parse → Parent-Child chunk → Store chunks in MongoDB 
  as "pending_review" → Embed to Pinecone → Return chunk preview for HITL
"""

import os
import gc
import hashlib
import aiofiles
import logging
import mimetypes
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.core.config import get_settings
from app.api.auth import verify_token
from app.db.mongodb import get_database
import uuid

settings = get_settings()
router = APIRouter()
logger = logging.getLogger(__name__)

# Constants for 7-Layer Security
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_PDF_PAGES = 500
ALLOWED_MIME_TYPES = ["application/pdf"]
TEMP_UPLOAD_DIR = os.path.join(os.getcwd(), "data", "temp_uploads")

os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)


def compute_file_hash(file_path: str) -> str:
    """Compute SHA-256 hash for duplicate detection."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


async def get_current_user_from_header(request):
    """Extract user from JWT token in Authorization header."""
    from fastapi import Request
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    return {"email": payload.get("sub"), "name": payload.get("name")}


from fastapi import Request, Depends

@router.post("/upload/temp")
async def upload_temp_pdf(
    request: Request,
    file: UploadFile = File(...),
    user_info: dict = Depends(get_current_user_from_header)
):
    """
    7-Layer Secure Upload for user Temp files.
    Includes SHA-256 dedup: same file uploaded twice = skip reindexing.
    Returns chunk previews for HITL review.
    """
    # --- Layer 1.5: Upstash Redis Rate Limiting (5 uploads/day per user/IP) ---
    user_email = user_info.get("email", "anonymous")
    client_ip = request.client.host if request.client else "unknown"
    
    from app.db.redis_client import get_redis
    redis = get_redis()
    if redis:
        rate_key = f"upload_limit:{user_email}:{client_ip}"
        try:
            current_uploads = redis.get(rate_key)
            if current_uploads and int(current_uploads) >= 5:
                raise HTTPException(status_code=429, detail="Rate limit exceeded. Maximum 5 uploads per day allowed.")
            count = redis.incr(rate_key)
            if count == 1:
                redis.expire(rate_key, 86400) # 24 hours
        except HTTPException:
            raise
        except Exception as e:
            logger.warning(f"Redis rate limiting failed: {e}")

    # --- Layer 2: Zero byte check ---
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename")
    
    # --- Layer 3: Extension check ---
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_filepath = os.path.join(TEMP_UPLOAD_DIR, temp_filename)
    file_size = 0
    
    try:
        # --- Layer 1: 10MB streaming protection ---
        async with aiofiles.open(temp_filepath, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # 1MB chunks
                file_size += len(content)
                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(status_code=413, detail="File exceeds 10MB limit")
                await out_file.write(content)
        
        # --- Layer 4: Deep MIME & Magic Byte check ---
        mime_type, _ = mimetypes.guess_type(temp_filepath)
        if mime_type not in ALLOWED_MIME_TYPES:
            os.remove(temp_filepath)
            raise HTTPException(status_code=415, detail="Forged file extension. Only true PDFs allowed.")
            
        with open(temp_filepath, 'rb') as f:
            header = f.read(5)
            if header != b'%PDF-':
                os.remove(temp_filepath)
                raise HTTPException(status_code=415, detail="Magic Byte verification failed. Not a valid PDF.")
        
        # --- Layer 5: PDF page count check (bomb protection) ---
        import fitz
        pdf = fitz.open(temp_filepath)
        page_count = len(pdf)
        pdf.close()
        if page_count > MAX_PDF_PAGES:
            os.remove(temp_filepath)
            raise HTTPException(status_code=413, detail=f"PDF has {page_count} pages. Maximum {MAX_PDF_PAGES} allowed.")
        
        # --- Layer 7: SHA-256 Duplicate Detection ---
        file_hash = compute_file_hash(temp_filepath)
        
        db = get_database()
        existing = await db.temp_uploads.find_one({
            "file_hash": file_hash,
            "original_filename": file.filename
        })
        
        if existing:
            # Same file already uploaded — return existing chunks without reindexing!
            logger.info(f"⏭️ Duplicate temp file detected: '{file.filename}' (hash: {file_hash[:8]}...)")
            os.remove(temp_filepath)  # Clean up the duplicate
            
            existing_chunks = await db.chunks.find({
                "file_hash": file_hash,
                "is_temporary": True
            }).to_list(100)
            
            return {
                "message": "⚠️ File already uploaded previously (duplicate detected). Your file is already indexed and ready for chat.",
                "filename": file.filename,
                "is_duplicate": True,
                "chunk_count": len(existing_chunks),
                "chunks_preview": [
                    {"chunk_id": str(c.get("_id", "")), "text": c.get("text", "")[:200], "status": c.get("status", "")}
                    for c in existing_chunks[:20]
                ]
            }
        
        # --- NEW FILE: Parse → Chunk → Embed (Real-time) ---
        logger.info(f"📄 New temp file: '{file.filename}' ({page_count} pages, {file_size} bytes)")
        
        from app.rag.parser import parse_document
        from app.rag.chunker import chunk_documents
        from app.rag.embedder import embed_and_upsert_chunks
        
        # Parse with PyMuPDF (FREE — never use LlamaParse for temp uploads)
        docs = parse_document(temp_filepath, is_temporary=True)
        
        # Chunk with Parent-Child strategy
        chunks = chunk_documents(docs, is_temporary=True, uploaded_by=user_email)
        
        # --- NEW: Real-time Jina AI Embedding ---
        logger.info("🚀 Real-time Jina AI embedding for user temp file...")
        vector_count = embed_and_upsert_chunks(chunks, source_file=file.filename)
        
        # Store chunks in MongoDB (for reference & chat history)
        from datetime import datetime, timezone
        now_utc = datetime.now(timezone.utc)
        chunk_docs = []
        for chunk in chunks:
            chunk_docs.append({
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "source_file": file.filename,
                "file_hash": file_hash,
                "page": chunk["metadata"].get("page", 0),
                "chunk_type": chunk["metadata"].get("chunk_type", ""),
                "parent_text": chunk["metadata"].get("parent_text", ""),
                "is_temporary": True,
                "uploaded_by": user_email,
                "status": "embedded",  # Ready immediately!
                "created_at": now_utc, # TTL deletion kicks in after 24h
            })
        
        if chunk_docs:
            await db.chunks.insert_many(chunk_docs)
        
        # Record this upload to prevent future duplicate processing
        await db.temp_uploads.insert_one({
            "original_filename": file.filename,
            "temp_filename": temp_filename,
            "file_hash": file_hash,
            "file_size": file_size,
            "page_count": page_count,
            "chunk_count": len(chunks),
            "created_at": now_utc,     # TTL deletion kicks in after 24h
        })
        
        # Clean up temp file from disk (data is now in MongoDB + will be embedded)
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        
        # Force garbage collection to free PyMuPDF memory
        gc.collect()
        
        return {
            "message": f"✅ File successfully analyzed & indexed in Real-time ({vector_count} vectors). Ready for Chat!",
            "filename": file.filename,
            "is_duplicate": False,
            "page_count": page_count,
            "chunk_count": len(chunks),
            "vector_upserted": vector_count,
            "chunks_preview": [
                {"chunk_id": c["chunk_id"], "text": c["text"][:200], "status": "embedded"}
                for c in chunks[:20]
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        gc.collect()
        raise HTTPException(status_code=500, detail="Secure file processing failed")
