"""
routes.py — All REST API Routes (Chat, History, Feedback, Admin, Sync, HITL)
===============================================================================
Matches ALL patterns from previous project:
  1. /chat — Agentic RAG (8-node graph) + Redis cache + rate limiting
  2. /chat/history — Get + Delete chat history (sliding window)
  3. /feedback — Thumbs up/down (save to MongoDB)
  4. /user/chunks — HITL for user's own temp uploads
  5. /user/chunks/approve — Approve/Reject/Edit chunks
  6. /admin/sync — ADMIN-ONLY sync control (fixed email)
  7. /admin/documents/delete — ADMIN-ONLY document deletion
  8. /admin/chunks — Admin view all pending chunks
  9. /admin/stats — Dashboard statistics
  10. /me — User info + is_admin flag
"""

import json
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.api.auth import verify_token, get_current_user
from app.db.mongodb import (
    get_database, get_chat_history, save_message,
    save_feedback, clear_chat_history
)
from app.core.config import get_settings

settings = get_settings()
router = APIRouter()
logger = logging.getLogger(__name__)


# ========== PYDANTIC MODELS ==========

class ChatRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    question: str
    response: str
    rating: str  # "helpful" or "not_helpful"

class ChunkAction(BaseModel):
    chunk_id: str
    action: str  # "approve", "reject", "edit"
    edited_text: Optional[str] = None


# ========== REDIS HELPER ==========

def get_redis():
    try:
        from upstash_redis import Redis
        if settings.UPSTASH_REDIS_REST_URL:
            return Redis(url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_REST_TOKEN)
    except Exception:
        pass
    return None


# ========== ADMIN CHECK (same as prev project) ==========

def get_admin_user(user: dict = Depends(get_current_user)):
    """
    Admin check — ONLY the fixed ADMIN_EMAIL can access admin endpoints.
    Same as prev project's get_admin_user dependency.
    """
    if user["email"].lower() != settings.ADMIN_EMAIL.lower():
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ========== CHAT ENDPOINT ==========

@router.post("/chat")
async def chat_endpoint(req: ChatRequest, user: dict = Depends(get_current_user)):
    """
    Main chat endpoint — 8-node Agentic RAG graph.
    Features: Redis cache, rate limiting, chat history, save to MongoDB.
    """
    import pybreaker
    from app.rag.graph import run_query

    email = user["email"]
    name = user.get("name", "User")
    question = req.question.strip()
    redis = get_redis()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # --- RATE LIMITING (10/min per user) ---
    if redis:
        try:
            rate_key = f"ratelimit:{email}"
            current_count = redis.get(rate_key)
            if current_count and int(current_count) >= 10:
                raise HTTPException(status_code=429, detail="Rate limit: max 10 queries per minute.")
            count = redis.incr(rate_key)
            if count == 1:
                redis.expire(rate_key, 60)
        except HTTPException:
            raise
        except Exception:
            pass

    # --- REDIS CACHE CHECK ---
    cache_key = f"chat:{email}:{question[:100]}"
    if redis:
        try:
            cached = redis.get(cache_key)
            if cached:
                logger.info("⚡ Cache HIT")
                return json.loads(cached)
        except Exception:
            pass

    # --- TRACK ACTIVE USER ---
    if redis:
        try:
            redis.setex(f"active:{email}", 900, "1")
        except Exception:
            pass

    # --- GET CHAT HISTORY (sliding window, last 6 messages) ---
    history = await get_chat_history(email, limit=6)

    # --- RUN 8-NODE RAG GRAPH ---
    result = await run_query(
        query=question,
        user_email=email,
        user_name=name,
        chat_history=history
    )

    response_data = {
        "answer": result.get("answer", ""),
        "sources": result.get("sources", []),
        "confidence": result.get("confidence", 0),
        "latency": result.get("latency", 0),
        "needs_clarification": result.get("needs_clarification", False),
        "is_fallback": result.get("is_fallback", False),
        "timestamp": datetime.now().isoformat()
    }

    # --- SAVE TO MONGODB ---
    await save_message(email, "user", question)
    await save_message(email, "assistant", result.get("answer", ""), result.get("sources"))

    # --- CACHE RESPONSE (1hr TTL) ---
    if redis:
        try:
            redis.setex(cache_key, 3600, json.dumps(response_data))
        except Exception:
            pass

    return response_data


# ========== CHAT STREAM ENDPOINT (SSE — Word by Word) ==========

@router.post("/chat/stream")
async def chat_stream_endpoint(req: ChatRequest, user: dict = Depends(get_current_user)):
    """
    SSE streaming chat — same as /chat but response comes word-by-word.
    
    Flow:
      1. Rate limiting + cache check (same as /chat)
      2. Run Classifier → CrossQuestioner → Retriever (fast, non-streamed)
      3. Stream Generator output word-by-word via SSE
      4. Save complete answer to MongoDB + Redis cache
    
    Frontend uses EventSource to consume: data chunks arrive as JSON SSE events.
    """
    import pybreaker
    from fastapi.responses import StreamingResponse

    email = user["email"]
    name = user.get("name", "User")
    question = req.question.strip()
    redis = get_redis()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # --- RATE LIMITING ---
    if redis:
        try:
            rate_key = f"ratelimit:{email}"
            current_count = redis.get(rate_key)
            if current_count and int(current_count) >= 10:
                raise HTTPException(status_code=429, detail="Rate limit: max 10 queries per minute.")
            count = redis.incr(rate_key)
            if count == 1:
                redis.expire(rate_key, 60)
        except HTTPException:
            raise
        except Exception:
            pass

    # --- CACHE CHECK ---
    cache_key = f"chat:{email}:{question[:100]}"
    if redis:
        try:
            cached = redis.get(cache_key)
            if cached:
                cached_data = json.loads(cached)
                # Return cached response as single SSE event
                async def cached_stream():
                    yield f"data: {json.dumps({'type': 'cached', 'answer': cached_data.get('answer', ''), 'sources': cached_data.get('sources', []), 'confidence': cached_data.get('confidence', 0), 'pii_detected': cached_data.get('pii_detected', False), 'pii_entities': cached_data.get('pii_entities', [])})}\n\n"
                    yield "data: [DONE]\n\n"
                return StreamingResponse(cached_stream(), media_type="text/event-stream")
        except Exception:
            pass

    # --- TRACK ACTIVE USER ---
    if redis:
        try:
            redis.setex(f"active:{email}", 900, "1")
        except Exception:
            pass

    # --- GET CHAT HISTORY ---
    history = await get_chat_history(email, limit=6)

    # --- RUN GRAPH (non-LLM nodes are fast) ---
    # We run the full graph to get retrieval results, then stream only the answer
    from app.rag.graph import run_query
    result = await run_query(
        query=question, user_email=email,
        user_name=name, chat_history=history
    )

    # If it's a non-RAG response (greeting, vague, fallback) — send immediately but with animation
    if result.get("is_fallback") or result.get("needs_clarification"):
        async def quick_stream():
            import asyncio
            # Add artificial "thinking" steps for user engagement
            nodes = [
                {"id": "guard", "label": "Safety Guard", "icon": "🛡️"},
                {"id": "classifier", "label": "Classifying Query", "icon": "🔍"},
                {"id": "reasoning", "label": "Agentic Reasoning", "icon": "🧠"},
                {"id": "cross_question", "label": "Formulating Clarification", "icon": "❓"} if result.get("needs_clarification") else {"id": "fallback", "label": "System Fallback Activated", "icon": "🆘"},
            ]
            for node in nodes:
                yield f"data: {json.dumps({'type': 'node', 'id': node['id'], 'label': node['label'], 'icon': node['icon'], 'status': 'running'})}\n\n"
                await asyncio.sleep(0.5)
                yield f"data: {json.dumps({'type': 'node', 'id': node['id'], 'status': 'done'})}\n\n"
            
            yield f"data: {json.dumps({'type': 'complete', 'answer': result.get('answer', ''), 'sources': result.get('sources', []), 'confidence': result.get('confidence', 0), 'pii_detected': result.get('pii_detected', False), 'pii_entities': result.get('pii_entities', [])})}\n\n"
            yield "data: [DONE]\n\n"

        await save_message(email, "user", question)
        await save_message(email, "assistant", result.get("answer", ""))
        return StreamingResponse(quick_stream(), media_type="text/event-stream")

    # --- STREAM THE GENERATOR OUTPUT (word-by-word) ---

    async def sse_generator():
        """Yield SSE events: node progress → metadata → word-by-word tokens → DONE."""
        import asyncio

        # Node Highlighter — show pipeline steps (purely cosmetic, real processing is done)
        nodes = [
            {"id": "guard", "label": "Safety Guard", "icon": "🛡️"},
            {"id": "classifier", "label": "Classifying Query", "icon": "🔍"},
            {"id": "retriever", "label": "Searching Documents", "icon": "📚"},
            {"id": "generator", "label": "Generating Answer", "icon": "✨"},
        ]
        for node in nodes:
            yield f"data: {json.dumps({'type': 'node', 'id': node['id'], 'label': node['label'], 'icon': node['icon'], 'status': 'running'})}\n\n"
            await asyncio.sleep(0.6)  # Premium visual pause for UX
            yield f"data: {json.dumps({'type': 'node', 'id': node['id'], 'status': 'done'})}\n\n"

        # Metadata (sources, confidence, PII)
        yield f"data: {json.dumps({'type': 'meta', 'sources': result.get('sources', []), 'confidence': result.get('confidence', 0), 'pii_detected': result.get('pii_detected', False), 'pii_entities': result.get('pii_entities', [])})}\n\n"

        # Stream the answer word-by-word
        full_answer = result.get("answer", "") or ""
        words = full_answer.split(" ")
        buffer = ""
        for i, word in enumerate(words):
            buffer += word + " "
            if len(buffer) > 15 or i == len(words) - 1:
                yield f"data: {json.dumps({'type': 'token', 'content': buffer})}\n\n"
                buffer = ""
                await asyncio.sleep(0.02)

        # Final event
        yield f"data: {json.dumps({'type': 'done', 'latency': result.get('latency', 0)})}\n\n"
        yield "data: [DONE]\n\n"

    # Save to MongoDB
    await save_message(email, "user", question)
    await save_message(email, "assistant", result.get("answer", ""), result.get("sources"))

    # Cache response
    if redis:
        try:
            response_data = {
                "answer": result.get("answer", ""),
                "sources": result.get("sources", []),
                "confidence": result.get("confidence", 0),
                "latency": result.get("latency", 0),
            }
            redis.setex(cache_key, 3600, json.dumps(response_data))
        except Exception:
            pass

    return StreamingResponse(sse_generator(), media_type="text/event-stream")


# ========== CHAT HISTORY ==========

@router.get("/chat/history")
async def get_history(user: dict = Depends(get_current_user)):
    """Get chat history for current user (sliding window)."""
    history = await get_chat_history(user["email"], limit=50)
    return {"history": history}


@router.delete("/chat/history")
async def delete_history(user: dict = Depends(get_current_user)):
    """Clear all chat history for current user."""
    await clear_chat_history(user["email"])
    return {"message": "Chat history cleared"}


# ========== FEEDBACK (Thumbs Up/Down) ==========

@router.post("/feedback")
async def submit_feedback(req: FeedbackRequest, user: dict = Depends(get_current_user)):
    """Submit feedback (👍/👎) for a response — same as prev project."""
    await save_feedback(user["email"], req.question, req.response, req.rating)
    return {"message": "Feedback recorded", "rating": req.rating}


# ========== USER INFO ==========

@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    """Return current user info + admin flag (same as prev project)."""
    return {
        "email": user["email"],
        "name": user.get("name", "User"),
        "is_admin": user["email"].lower() == settings.ADMIN_EMAIL.lower()
    }


# ========== HITL: USER'S OWN CHUNKS ==========

@router.get("/user/chunks")
async def get_user_chunks(user: dict = Depends(get_current_user)):
    """User sees chunks from their own uploaded temp files for review."""
    db = get_database()
    user_chunks = await db.chunks.find(
        {"is_temporary": True, "uploaded_by": user["email"]}
    ).sort("source_file", 1).limit(200).to_list(200)

    return [
        {
            "chunk_id": str(doc.get("_id", "")),
            "text": doc.get("text", ""),
            "source_file": doc.get("source_file", ""),
            "page": doc.get("page", 0),
            "chunk_type": doc.get("chunk_type", ""),
            "status": doc.get("status", ""),
        }
        for doc in user_chunks
    ]


@router.post("/user/chunks/approve")
async def user_approve_chunk(action: ChunkAction, user: dict = Depends(get_current_user)):
    """
    User approves/rejects/edits their own temp chunks.
    ONLY approved chunks get embedded into Pinecone.
    Jina API quota is NOT wasted on rejected chunks!
    """
    db = get_database()

    chunk = await db.chunks.find_one({"_id": action.chunk_id, "uploaded_by": user["email"]})
    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found or doesn't belong to you")

    if action.action == "approve":
        await db.chunks.update_one({"_id": action.chunk_id}, {"$set": {"status": "approved"}})
        # NOW trigger embedding (only for approved chunks!)
        from app.rag.embedder import embed_and_upsert_chunks
        embed_and_upsert_chunks(
            [{"chunk_id": chunk["chunk_id"], "text": chunk["text"], "metadata": {
                "source_file": chunk["source_file"], "page": chunk["page"],
                "chunk_type": chunk["chunk_type"], "parent_text": chunk.get("parent_text", ""),
                "is_temporary": True, "uploaded_by": user["email"]
            }}],
            source_file=chunk["source_file"]
        )
        return {"message": "Chunk approved and embedded"}

    elif action.action == "reject":
        await db.chunks.update_one({"_id": action.chunk_id}, {"$set": {"status": "rejected"}})
        return {"message": "Chunk rejected (no API quota used)"}

    elif action.action == "edit":
        if not action.edited_text:
            raise HTTPException(status_code=400, detail="edited_text required")
        await db.chunks.update_one(
            {"_id": action.chunk_id},
            {"$set": {"text": action.edited_text, "status": "approved"}}
        )
        return {"message": "Chunk edited and approved"}

    raise HTTPException(status_code=400, detail="Invalid action")


# ========== ADMIN: SYNC ENGINE (ADMIN-ONLY) ==========

@router.post("/admin/sync")
async def sync_documents(user: dict = Depends(get_admin_user)):
    """
    ADMIN-ONLY: Trigger sync engine.
    Only ADMIN_EMAIL can run this.
    Same pattern as prev project's /admin/documents/sync.
    """
    from app.rag.sync import sync_core_brain

    try:
        results = sync_core_brain()
        return {
            "message": "Sync complete",
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Sync error: {e}")
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


# ========== ADMIN: DELETE DOCUMENT (ADMIN-ONLY) ==========

@router.delete("/admin/documents/{file_name}")
async def delete_document(file_name: str, user: dict = Depends(get_admin_user)):
    """
    ADMIN-ONLY: Delete a document.
    Removes vectors from Pinecone + marks inactive in Supabase registry.
    Same as prev project's admin delete.
    """
    from app.db.pinecone_client import delete_vectors_by_filter
    from app.db.supabase_client import mark_file_inactive

    try:
        delete_vectors_by_filter({"source_file": {"$eq": file_name}})
        mark_file_inactive(file_name)
        return {"message": f"Deleted: {file_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== ADMIN: VIEW ALL PENDING CHUNKS ==========

@router.get("/admin/chunks")
async def get_admin_chunks(user: dict = Depends(get_admin_user)):
    """Admin view: all chunks with pending_review status."""
    db = get_database()
    pending = await db.chunks.find({"status": "pending_review"}).limit(200).to_list(200)
    return [
        {
            "chunk_id": str(doc.get("_id", "")),
            "text": doc.get("text", "")[:200],
            "source_file": doc.get("source_file", ""),
            "status": doc.get("status", ""),
        }
        for doc in pending
    ]


@router.post("/admin/chunks/approve")
async def admin_approve_chunk(action: ChunkAction, user: dict = Depends(get_admin_user)):
    """Admin approves/rejects chunks for core brain."""
    db = get_database()
    if action.action == "approve":
        await db.chunks.update_one({"_id": action.chunk_id}, {"$set": {"status": "approved"}})
        return {"message": "Chunk approved"}
    elif action.action == "reject":
        await db.chunks.update_one({"_id": action.chunk_id}, {"$set": {"status": "rejected"}})
        return {"message": "Chunk rejected"}
    raise HTTPException(status_code=400, detail="Invalid action")


@router.get("/common/stats")
async def get_common_stats(user: str = Depends(get_current_user)):
    """Public stats for normal users to build trust (Files & Vectors count)."""
    from app.db.supabase_client import get_all_active_files
    files = get_all_active_files()
    total_files = len(files)
    total_chunks = sum(f.get("chunk_count", 0) for f in files)
    
    return {
        "total_files": total_files,
        "total_chunks": total_chunks,
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

# ========== ADMIN: STATS ==========

@router.get("/admin/stats")
async def get_admin_stats(user: dict = Depends(get_admin_user)):
    """Admin dashboard statistics."""
    db = get_database()
    redis = get_redis()

    active_users = 0
    if redis:
        try:
            keys = redis.keys("active:*")
            active_users = len(keys) if keys else 0
        except Exception:
            pass

    total_chunks = await db.chunks.count_documents({})
    pending_chunks = await db.chunks.count_documents({"status": "pending_review"})
    total_feedback = await db.feedback.count_documents({})
    helpful_count = await db.feedback.count_documents({"rating": "helpful"})

    return {
        "active_users": active_users,
        "total_chunks": total_chunks,
        "pending_review": pending_chunks,
        "total_feedback": total_feedback,
        "helpful_feedback": helpful_count,
        "timestamp": datetime.now().isoformat()
    }
