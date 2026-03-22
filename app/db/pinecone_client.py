import logging
import json
import uuid
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from pinecone.grpc import PineconeGRPC as Pinecone # For faster performance
from pinecone import ServerlessSpec

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Global client
_pinecone_client = None

def get_pinecone_client() -> Pinecone:
    """Initialize and retrieve the Pinecone client (singleton)."""
    global _pinecone_client
    if _pinecone_client is None:
        try:
            logger.info("Initializing Pinecone Client...")
            _pinecone_client = Pinecone(api_key=settings.PINECONE_API_KEY)
            ensure_index(_pinecone_client)
        except Exception as e:
            logger.error(f"Failed to connect to Pinecone: {e}")
            raise
    return _pinecone_client

def ensure_index(pc: Pinecone):
    """Ensure that the financial parser index exists with dims=256."""
    index_name = settings.PINECONE_INDEX_NAME
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        logger.info(f"Index '{index_name}' not found. Creating it now (this might take a minute)...")
        try:
            pc.create_index(
                name=index_name,
                dimension=256,  # Jina v3 MRL Dimensions
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            logger.info(f"✅ Created Pinecone index: {index_name}")
        except Exception as e:
            logger.error(f"Index creation failed: {e}")
            raise
    else:
        logger.info(f"✅ Pinecone index '{index_name}' confirmed active.")

def get_index():
    """Retrieve the connected index instance."""
    pc = get_pinecone_client()
    return pc.Index(settings.PINECONE_INDEX_NAME)

def upsert_vectors(vectors: List[Dict[str, Any]], namespace: str = "") -> int:
    """
    Upsert vectors into Pinecone.
    Vectors format: [{"id": "...", "values": [...], "metadata": {...}}, ...]
    """
    index = get_index()
    # Safe batch upsert limit for Pinecone is typically ~100
    batch_size = 100
    upserted_count = 0
    
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        try:
            index.upsert(vectors=batch, namespace=namespace)
            upserted_count += len(batch)
            logger.info(f"⬆️ Upserted batch of {len(batch)} vectors to Pinecone")
        except Exception as e:
            logger.error(f"Pinecone batch upsert error: {e}")
            raise
    
    return upserted_count

def delete_vectors_by_filter(filter_dict: dict, namespace: str = ""):
    """
    Delete vectors matching a specific metadata filter.
    Used for dropping temp files or removing obsolete file chunks during sync.
    Example: filter_dict = {"source_file": "budget.pdf", "is_temporary": False}
    """
    index = get_index()
    try:
        # Note: Pinecone free tier allows delete by metadata
        index.delete(filter=filter_dict, namespace=namespace)
        logger.info(f"🗑️ Deleted vectors matching filter: {json.dumps(filter_dict)}")
    except Exception as e:
        logger.error(f"Pinecone delete error: {e}")

def cleanup_user_temp_vectors(user_email: str):
    """Delete all temporary vectors uploaded by a specific user (Logout flow)."""
    if not user_email:
        return
    
    delete_vectors_by_filter({
        "is_temporary": {"$eq": True},
        "uploaded_by": {"$eq": user_email}
    })
