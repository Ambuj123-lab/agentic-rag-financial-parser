"""
embedder.py — Batch Embedding with Jina v3 + Circuit Breaker + Incremental Upsert
===================================================================================

Key Features:
  1. Jina v3 MRL (Matryoshka Representation Learning) at 256 dims
  2. Circuit Breaker: pybreaker wraps Jina API calls
  3. Exponential Backoff: 2s → 4s → 8s on rate limits
  4. Batch size = 5 (small to protect 512MB RAM)
  5. NO ORPHANED VECTORS: If embedding fails mid-batch, ALL vectors for that 
     file are surgically deleted from Pinecone
  6. INCREMENTAL UPSERT (Document Level): Uses Pinecone upsert which naturally
     handles duplicates — if same chunk_id exists, it gets overwritten, not duplicated
     
MRL (Matryoshka Representation Learning) — Explained:
  Full Jina v3 output = 1024 dimensions.
  We pass `dimensions: 256` in the API request. Jina truncates the embedding
  to the first 256 values. Because of MRL training, the first N dims contain
  the most important semantic information (like a Russian Matryoshka doll).
  
  Result: 75% less Pinecone storage with ~95% retrieval quality preserved.
  
  We also use task-specific LoRA adapters:
    - "retrieval.passage" → for document chunks (optimized for being FOUND)
    - "retrieval.query"   → for user queries (optimized for FINDING)
"""

import logging
import time
import httpx
import pybreaker
from typing import List, Dict, Any

from app.core.config import get_settings
from app.core.constants import EMBEDDING_DIMENSIONS, EMBED_BATCH_SIZE
from app.db.pinecone_client import upsert_vectors, delete_vectors_by_filter

settings = get_settings()
logger = logging.getLogger(__name__)

JINA_EMBED_URL = "https://api.jina.ai/v1/embeddings"

# Circuit Breaker: If Jina fails 3 times → stop for 30s
jina_circuit = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=30,
    name="Jina_Embedding_CircuitBreaker"
)


@jina_circuit
def embed_texts(texts: List[str], max_retries: int = 3) -> List[List[float]]:
    """
    Call Jina v3 Embeddings API with exponential backoff retry.
    Returns 256-dimensional float vectors (MRL truncated).
    """
    headers = {
        "Authorization": f"Bearer {settings.JINA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "jina-embeddings-v3",
        "input": texts,
        "dimensions": EMBEDDING_DIMENSIONS,  # MRL: 1024 → 256
        "task": "retrieval.passage",  # LoRA adapter for documents
    }
    
    for attempt in range(max_retries):
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(JINA_EMBED_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return [item["embedding"] for item in data["data"]]
                
            elif response.status_code == 429:
                # Exponential backoff: 2s → 4s → 8s
                wait_time = 2 ** (attempt + 1)
                logger.warning(f"⏳ Jina rate limited. Backoff {wait_time}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
                
            else:
                logger.error(f"❌ Jina API {response.status_code}: {response.text[:200]}")
                raise Exception(f"Jina embedding failed: {response.status_code}")
                
        except httpx.TimeoutException:
            wait_time = 2 ** (attempt + 1)
            logger.warning(f"⏳ Jina timeout. Backoff {wait_time}s (attempt {attempt+1}/{max_retries})")
            time.sleep(wait_time)
    
    raise Exception(f"Jina embedding failed after {max_retries} retries")


def embed_and_upsert_chunks(
    chunks: List[Dict[str, Any]], 
    source_file: str,
    namespace: str = ""
) -> int:
    """
    Embed chunks and UPSERT (not insert!) to Pinecone.
    
    INCREMENTAL UPSERT (Document Level):
      Pinecone's upsert() is idempotent — if a vector with the same ID already
      exists, it gets overwritten with the new values. No duplicate vectors!
      This means if chunking/embedding pauses mid-way and restarts:
        - Already-upserted chunks get overwritten (no dupes)
        - New chunks get inserted
        - Result: clean, consistent index
      
    NO ORPHAN GUARANTEE:
      If ANY batch fails during embedding, we surgically delete ALL vectors 
      from this specific source_file. The sync engine can then retry the file
      cleanly without leaving half-indexed garbage.
    
    Returns: Total vectors upserted
    """
    total_upserted = 0
    all_vectors = []
    
    logger.info(f"🔄 Embedding {len(chunks)} chunks for '{source_file}' (batch={EMBED_BATCH_SIZE})")
    
    try:
        for i in range(0, len(chunks), EMBED_BATCH_SIZE):
            batch = chunks[i:i + EMBED_BATCH_SIZE]
            texts = [c["text"] for c in batch]
            
            # Get embeddings from Jina (protected by circuit breaker)
            embeddings = embed_texts(texts)
            
            # Build Pinecone vector format
            for j, chunk in enumerate(batch):
                vector = {
                    "id": chunk["chunk_id"],  # Same ID = overwrite, not duplicate!
                    "values": embeddings[j],
                    "metadata": {
                        **chunk["metadata"],
                        "text_preview": chunk["text"][:500],
                    }
                }
                all_vectors.append(vector)
            
            batch_num = i // EMBED_BATCH_SIZE + 1
            total_batches = (len(chunks) + EMBED_BATCH_SIZE - 1) // EMBED_BATCH_SIZE
            logger.info(f"  ✅ Batch {batch_num}/{total_batches} embedded")
        
        # All batches done — upsert to Pinecone (idempotent!)
        total_upserted = upsert_vectors(all_vectors, namespace=namespace)
        logger.info(f"🎯 Upserted {total_upserted} vectors for '{source_file}'")
        
    except pybreaker.CircuitBreakerError:
        logger.error(f"⚡ Circuit breaker OPEN — Jina API down. Skipping '{source_file}'")
        _surgical_delete(source_file, namespace)
        raise
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed for '{source_file}': {e}")
        _surgical_delete(source_file, namespace)
        raise
    
    return total_upserted


def _surgical_delete(source_file: str, namespace: str = ""):
    """
    Surgical Deletion: Remove ONLY vectors belonging to the failed source file.
    No other document's vectors are touched.
    """
    logger.warning(f"🔪 Surgical delete: removing orphaned vectors for '{source_file}'")
    delete_vectors_by_filter(
        {"source_file": {"$eq": source_file}},
        namespace=namespace
    )
