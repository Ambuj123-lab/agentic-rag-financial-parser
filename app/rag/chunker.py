"""
chunker.py — Dual Chunking Strategy
=====================================
Two strategies based on the source loader:

1. MarkdownHeaderTextSplitter (for LlamaParse output)
   - Splits on Markdown headers (# ## ### etc.)
   - Keeps entire tables inside one chunk (no mid-table cuts!)
   - Best for: Budget, Finance Bill, Constitution etc.

2. Parent-Child Chunking (for PyMuPDF output)
   - Parent chunk = 2000 chars (stored in child metadata for LLM context)
   - Child chunk = 400 chars (stored as vector for precise retrieval)
   - Best for: Plain text PDFs, temporary user uploads
   
Why not Parent-Child for everything?
   Because Parent-Child splits by character count (e.g., cut at 2000 chars).
   If a Markdown table is 2500 chars, it gets chopped at 2000 — the bottom half
   loses its column headers, and the LLM gets confused. MarkdownHeaderSplitter
   avoids this by splitting on headers, keeping tables intact.
"""

import logging
import hashlib
from typing import List, Dict, Any
from datetime import datetime

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)
from app.core.constants import (
    PARENT_CHUNK_SIZE,
    PARENT_CHUNK_OVERLAP,
    CHILD_CHUNK_SIZE,
    CHILD_CHUNK_OVERLAP,
    MAX_MARKDOWN_CHUNK_SIZE
)

logger = logging.getLogger(__name__)


def chunk_with_markdown_headers(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Strategy 1: MarkdownHeaderTextSplitter
    Used for LlamaParse output (which produces beautiful Markdown with headers).
    
    How it works:
      - Splits text wherever it finds # headers
      - Each chunk inherits its parent headers as metadata
      - If a chunk is still too large (>3000 chars), we do a secondary
        RecursiveCharacterTextSplitter pass
    """
    headers_to_split_on = [
        ("#", "heading_1"),
        ("##", "heading_2"),
        ("###", "heading_3"),
        ("####", "heading_4"),
    ]
    
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False  # Keep headers in the text for LLM context
    )
    
    # Secondary splitter for oversized chunks
    size_splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_MARKDOWN_CHUNK_SIZE,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    all_chunks = []
    
    for doc in docs:
        text = doc.get("text", "")
        source = doc.get("source", "unknown")
        loader = doc.get("loader", "unknown")
        page = doc.get("page", 0)
        
        # Split by markdown headers
        md_chunks = md_splitter.split_text(text)
        
        for md_chunk in md_chunks:
            chunk_text = md_chunk.page_content
            chunk_metadata = dict(md_chunk.metadata) if md_chunk.metadata else {}
            
            # If chunk is too large, split further by size
            if len(chunk_text) > MAX_MARKDOWN_CHUNK_SIZE:
                sub_chunks = size_splitter.split_text(chunk_text)
                for j, sub in enumerate(sub_chunks):
                    # Deterministic ID: hash of source+page+header+subindex
                    chunk_id = hashlib.md5(f"{source}_{page}_{chunk_metadata}_{j}".encode()).hexdigest()
                    all_chunks.append({
                        "chunk_id": chunk_id,
                        "text": sub,
                        "metadata": {
                            **chunk_metadata,
                            "source_file": source,
                            "loader": loader,
                            "page": page,
                            "chunk_type": "markdown_header",
                            "sub_chunk_index": j,
                            "parent_text": chunk_text,  # Full header section for LLM context
                            "text_preview": sub[:500],
                            "is_temporary": False,
                            "uploaded_by": "system",
                            "indexed_at": datetime.now().isoformat(),
                        }
                    })
            else:
                chunk_id = hashlib.md5(f"{source}_{page}_{chunk_metadata}".encode()).hexdigest()
                all_chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "metadata": {
                        **chunk_metadata,
                        "source_file": source,
                        "loader": loader,
                        "page": page,
                        "chunk_type": "markdown_header",
                        "parent_text": chunk_text,  # Same text — it's the full header section
                        "text_preview": chunk_text[:500],
                        "is_temporary": False,
                        "uploaded_by": "system",
                        "indexed_at": datetime.now().isoformat(),
                    }
                })
    
    logger.info(f"📐 MarkdownHeaderSplitter: Created {len(all_chunks)} chunks")
    return all_chunks


def chunk_with_parent_child(docs: List[Dict[str, Any]], is_temporary: bool = False, uploaded_by: str = "") -> List[Dict[str, Any]]:
    """
    Strategy 2: Parent-Child Chunking
    Used for PyMuPDF output (plain text extraction).
    
    How it works:
      1. First, create PARENT chunks (2000 chars) from the full text
      2. Then, split each parent into CHILD chunks (400 chars)
      3. Each child chunk stores its parent's full text in metadata
      4. During retrieval, we search by child (precise match),
         but feed the parent text to the LLM (rich context)
    
    Why store parent in metadata instead of separate collection?
      → Single query = fast retrieval. No secondary database lookup needed.
      → Pinecone metadata limit is 40KB per vector, and parent (2000 chars) 
        easily fits within that.
    """
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=PARENT_CHUNK_SIZE,
        chunk_overlap=PARENT_CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHILD_CHUNK_SIZE,
        chunk_overlap=CHILD_CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    all_chunks = []
    parent_count = 0
    child_count = 0
    
    for doc in docs:
        text = doc.get("text", "")
        source = doc.get("source", "unknown")
        loader = doc.get("loader", "unknown")
        page = doc.get("page", 0)
        
        # Step 1: Create parent chunks
        parent_texts = parent_splitter.split_text(text)
        
        for parent_idx, parent_text in enumerate(parent_texts):
            # Deterministic parent ID: hash_parentIdx (same as prev project)
            parent_id = f"{source}_{page}_{parent_idx}"
            parent_count += 1
            
            child_texts = child_splitter.split_text(parent_text)
            
            for child_idx, child_text in enumerate(child_texts):
                # Deterministic child ID: hash_parentIdx_childIdx (same as prev project)
                child_id = hashlib.md5(f"{parent_id}_{child_idx}".encode()).hexdigest()
                child_count += 1
                
                all_chunks.append({
                    "chunk_id": child_id,
                    "text": child_text,  # This gets embedded as vector
                    "metadata": {
                        "parent_id": parent_id,
                        "parent_text": parent_text,  # Full parent for LLM context
                        "text_preview": child_text[:500],
                        "source_file": source,
                        "loader": loader,
                        "page": page,
                        "chunk_type": "parent_child",
                        "child_index": child_idx,
                        "parent_chunk_index": parent_idx,
                        "is_temporary": is_temporary,
                        "uploaded_by": uploaded_by if is_temporary else "system",
                        "indexed_at": datetime.now().isoformat(),
                    }
                })
    
    logger.info(
        f"👨‍👧 Parent-Child Chunker: {parent_count} parents → {child_count} children "
        f"(temp={is_temporary})"
    )
    return all_chunks


def chunk_documents(
    docs: List[Dict[str, Any]], 
    is_temporary: bool = False, 
    uploaded_by: str = ""
) -> List[Dict[str, Any]]:
    """
    Main entry point: Automatically selects the right chunking strategy.
    
    - LlamaParse output (has 'LlamaParse' in loader) → MarkdownHeaderSplitter
    - PyMuPDF output → Parent-Child Chunking
    """
    if not docs:
        return []
    
    # Check the loader field to decide strategy
    first_loader = docs[0].get("loader", "")
    
    if "LlamaParse" in first_loader:
        logger.info(f"🔀 Using MarkdownHeaderSplitter for {docs[0].get('source', 'unknown')}")
        return chunk_with_markdown_headers(docs)
    else:
        logger.info(f"🔀 Using Parent-Child Chunker for {docs[0].get('source', 'unknown')}")
        return chunk_with_parent_child(docs, is_temporary=is_temporary, uploaded_by=uploaded_by)
