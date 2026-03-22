"""
sync.py — SHA-256 Sync Engine
===============================
Syncs the local `data/raw_pdf/` folder with the vector database.

Flow:
  1. Scan all PDFs in data/raw_pdf/
  2. For each PDF, compute SHA-256 hash
  3. Check Supabase fp_file_registry:
     - NEW file (no entry): Parse → Chunk → Embed → Upload to Supabase → Register
     - CHANGED file (hash mismatch): Delete old vectors → Re-parse → Re-embed → Update registry
     - UNCHANGED file (hash matches): Skip entirely (saves credits!)
     - DELETED file (in registry but not on disk): Delete vectors → Mark inactive
  4. Report summary

This is the same proven pattern from the Constitution project,
enhanced with LlamaParse tier selection and HITL chunk review.
"""

import os
import logging
import gc
from typing import List, Dict, Tuple

from app.rag.parser import parse_document, get_file_hash
from app.rag.chunker import chunk_documents
from app.rag.embedder import embed_and_upsert_chunks
from app.db.supabase_client import (
    upload_file_to_storage,
    get_registry_entry,
    upsert_registry_entry,
    get_all_active_files,
    mark_file_inactive
)
from app.db.pinecone_client import delete_vectors_by_filter

logger = logging.getLogger(__name__)

RAW_PDF_DIR = os.path.join(os.getcwd(), "data", "raw_pdf")


def scan_local_pdfs() -> List[str]:
    """Find all PDF files in the raw_pdf directory."""
    if not os.path.exists(RAW_PDF_DIR):
        logger.warning(f"⚠️ Directory not found: {RAW_PDF_DIR}")
        return []
    
    pdfs = [
        f for f in os.listdir(RAW_PDF_DIR) 
        if f.lower().endswith('.pdf')
    ]
    logger.info(f"📂 Found {len(pdfs)} PDFs in {RAW_PDF_DIR}")
    return pdfs


def sync_core_brain() -> Dict[str, any]:
    """
    Main sync function — compares local PDFs against Supabase registry.
    
    Returns a summary dict:
    {
        "added": ["file1.pdf", ...],
        "updated": ["file2.pdf", ...],
        "unchanged": ["file3.pdf", ...],
        "deleted": ["file4.pdf", ...],
        "errors": ["file5.pdf: error message", ...]
    }
    """
    summary = {
        "added": [],
        "updated": [],
        "unchanged": [],
        "deleted": [],
        "errors": []
    }
    
    local_pdfs = scan_local_pdfs()
    
    # --- Process each local PDF ---
    for filename in local_pdfs:
        file_path = os.path.join(RAW_PDF_DIR, filename)
        
        try:
            # Compute SHA-256 hash
            current_hash = get_file_hash(file_path)
            file_size = os.path.getsize(file_path)
            
            # Check registry
            registry_entry = get_registry_entry(filename)
            
            if registry_entry is None:
                # NEW FILE — full pipeline
                logger.info(f"🆕 New file detected: {filename}")
                _process_new_file(filename, file_path, current_hash, file_size, summary)
                
            elif registry_entry.get("file_hash") != current_hash:
                # CHANGED FILE — delete old vectors, re-process
                logger.info(f"🔄 Changed file detected: {filename}")
                _process_changed_file(filename, file_path, current_hash, file_size, summary)
                
            else:
                # UNCHANGED — skip
                logger.info(f"⏭️ Unchanged: {filename}")
                summary["unchanged"].append(filename)
                
        except Exception as e:
            error_msg = f"{filename}: {str(e)}"
            logger.error(f"❌ Sync error: {error_msg}")
            summary["errors"].append(error_msg)
        
        # Force garbage collection after each file to protect 512MB RAM
        gc.collect()
    
    # --- Detect DELETED files (in registry but not on disk) ---
    active_files = get_all_active_files()
    for entry in active_files:
        reg_name = entry.get("file_name", "")
        if reg_name not in local_pdfs:
            logger.info(f"🗑️ Deleted from disk: {reg_name}")
            delete_vectors_by_filter({"source_file": {"$eq": reg_name}})
            mark_file_inactive(reg_name)
            summary["deleted"].append(reg_name)
    
    # --- Print Summary ---
    logger.info("=" * 50)
    logger.info("📊 SYNC SUMMARY")
    logger.info(f"  Added:     {len(summary['added'])} files")
    logger.info(f"  Updated:   {len(summary['updated'])} files")
    logger.info(f"  Unchanged: {len(summary['unchanged'])} files")
    logger.info(f"  Deleted:   {len(summary['deleted'])} files")
    logger.info(f"  Errors:    {len(summary['errors'])} files")
    logger.info("=" * 50)
    
    return summary


def _process_new_file(filename, file_path, file_hash, file_size, summary):
    """Parse → Chunk → Embed → Upload → Register a new file."""
    # Step 1: Parse
    docs = parse_document(file_path, is_temporary=False)
    
    # Step 2: Chunk
    chunks = chunk_documents(docs, is_temporary=False)
    
    # Step 3: Embed and upsert
    vector_count = embed_and_upsert_chunks(chunks, source_file=filename)
    
    # Step 4: Upload raw PDF to Supabase Storage
    upload_file_to_storage(file_path, filename)
    
    # Step 5: Register in Supabase table
    # parent_child type = PyMuPDF docs (child vectors with parent in metadata)
    # markdown_header type = LlamaParse docs (header-split chunks)
    pc_chunks = sum(1 for c in chunks if c["metadata"].get("chunk_type") == "parent_child")
    md_chunks = sum(1 for c in chunks if c["metadata"].get("chunk_type") == "markdown_header")
    
    upsert_registry_entry({
        "file_name": filename,
        "file_hash": file_hash,
        "file_size": file_size,
        "chunk_count": len(chunks),
        "parent_chunk_count": pc_chunks,   # Parent-Child strategy vectors
        "child_chunk_count": md_chunks,     # Markdown Header strategy chunks
        "status": "active"
    })
    
    summary["added"].append(filename)
    logger.info(f"✅ Added '{filename}' — {len(chunks)} chunks, {vector_count} vectors")


def _process_changed_file(filename, file_path, file_hash, file_size, summary):
    """Delete old vectors → Re-process the changed file."""
    # Step 1: Delete old vectors
    delete_vectors_by_filter({"source_file": {"$eq": filename}})
    
    # Step 2: Re-process (same as new file)
    _process_new_file(filename, file_path, file_hash, file_size, summary)
    
    # Move from 'added' to 'updated' in summary
    if filename in summary["added"]:
        summary["added"].remove(filename)
        summary["updated"].append(filename)
