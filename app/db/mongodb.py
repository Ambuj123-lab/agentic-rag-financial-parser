"""
mongodb.py — Chat History + Feedback + Chunk Review (Async Motor Client)
=========================================================================
Replicates ALL MongoDB patterns from the previous project:
  1. save_message()     — Push chat messages with sliding window
  2. get_chat_history() — Get last N messages for LLM context
  3. save_feedback()    — Thumbs up/down for responses
  4. GDPR TTL           — 30-day auto-delete on chat history
  5. Async Motor        — Non-blocking MongoDB for FastAPI

Previous project used pymongo (sync). This project uses motor (async) for
better performance under concurrent users.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_state = MongoDB()


async def connect_to_mongo():
    """Create MongoDB connection pool (called on FastAPI startup)."""
    logger.info("Connecting to MongoDB Atlas...")
    try:
        db_state.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            maxPoolSize=10,
            minPoolSize=1
        )
        db_state.db = db_state.client[settings.MONGODB_DB_NAME]
        logger.info(f"✅ Connected to MongoDB database: {settings.MONGODB_DB_NAME}")
    except Exception as e:
        logger.error(f"❌ Could not connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection pool (called on FastAPI shutdown)."""
    logger.info("Closing MongoDB connection...")
    if db_state.client:
        db_state.client.close()
        logger.info("✅ MongoDB connection closed.")


def get_database():
    """Get the active database instance."""
    if db_state.db is None:
        raise Exception("MongoDB not initialized. Call connect_to_mongo() first.")
    return db_state.db


async def ensure_indexes():
    """Create essential MongoDB indexes."""
    try:
        db = get_database()

        # Chat history: fast lookup by user_email
        await db.chat_history.create_index("user_email")

        # GDPR Compliance: Auto-delete chat history after 30 days of inactivity
        # (same as previous project's expireAfterSeconds=2592000)
        await db.chat_history.create_index("last_activity", expireAfterSeconds=2592000)

        # Feedback collection index
        await db.feedback.create_index("user_email")

        # Chunks: pending_review status for HITL
        await db.chunks.create_index("status")
        await db.chunks.create_index([("uploaded_by", 1), ("is_temporary", 1)])
        # Auto-delete chunks metadata after 24 hours
        await db.chunks.create_index("created_at", expireAfterSeconds=86400)

        # Temp uploads: SHA-256 hash lookup and 24-hour auto-delete
        await db.temp_uploads.create_index("file_hash")
        await db.temp_uploads.create_index("created_at", expireAfterSeconds=86400)

        logger.info("✅ MongoDB Indexes Ensured (chat, feedback, chunks, temp).")
    except Exception as e:
        logger.error(f"MongoDB index creation failed: {e}")


# ========== CHAT HISTORY (Sliding Window) ==========

async def save_message(
    user_email: str,
    role: str,
    content: str,
    sources: Optional[List[dict]] = None,
):
    """
    Save chat message to MongoDB with $push (same pattern as prev project).
    Messages are pushed into an array. last_activity updates for GDPR TTL.
    """
    db = get_database()

    try:
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        if sources:
            message["sources"] = sources

        await db.chat_history.update_one(
            {"user_email": user_email},
            {
                "$push": {"messages": message},
                "$set": {"last_activity": datetime.now()}
            },
            upsert=True
        )
    except Exception as e:
        logger.error(f"Save message error: {e}")


async def get_chat_history(user_email: str, limit: int = 6) -> List[dict]:
    """
    Get recent chat history for a user (sliding window).
    Returns last `limit` messages for LLM context window.
    Same as prev project: doc["messages"][-limit:]
    """
    db = get_database()

    try:
        doc = await db.chat_history.find_one({"user_email": user_email})
        if doc and "messages" in doc:
            return doc["messages"][-limit:]
        return []
    except Exception as e:
        logger.error(f"Get history error: {e}")
        return []


async def clear_chat_history(user_email: str):
    """Clear all chat history for a user."""
    db = get_database()
    try:
        await db.chat_history.delete_one({"user_email": user_email})
    except Exception as e:
        logger.error(f"Clear history error: {e}")


# ========== FEEDBACK (Thumbs Up/Down) ==========

async def save_feedback(
    user_email: str,
    question: str,
    response: str,
    rating: str,  # "helpful" or "not_helpful"
):
    """
    Save user feedback (👍/👎) for a response.
    Same pattern as prev project — separate 'feedback' collection.
    """
    db = get_database()

    try:
        await db.feedback.insert_one({
            "user_email": user_email,
            "question": question,
            "response": response[:500],  # Truncate to save storage
            "rating": rating,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Save feedback error: {e}")
