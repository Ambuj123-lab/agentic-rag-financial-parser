import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

from app.rag.parser import parse_document
from app.rag.chunker import chunk_documents
from app.rag.embedder import embed_and_upsert_chunks

def main():
    print("\n" + "="*50)
    print("[STARTING DRY RUN (PYMUPDF) - 0 CREDITS]")
    print("="*50 + "\n")
    
    file_path = os.path.join(os.getcwd(), "data", "raw_pdf", "Employees' Provident Funds Scheme.1952.pdf")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found at {file_path}")
        sys.exit(1)
        
    print(f"1. Parsing: {os.path.basename(file_path)}")
    # PyMuPDF tier will be selected automatically by parser.py
    docs = parse_document(file_path, is_temporary=False)
    print(f"   [OK] Parser returned {len(docs)} pages.")
    
    print("\n2. Chunking (Parent-Child Strategy)...")
    chunks = chunk_documents(docs, is_temporary=False)
    print(f"   [OK] Chunker returned {len(chunks)} child chunks.")
    
    if chunks:
        print(f"   [OK] Generated {len(chunks)} chunks with Parent-Child chunking.")

    print("3. Embedding and Upserting to Pinecone...")
    # Just embedding first 15 chunks (3 batches) to verify everything works quickly
    test_chunks = chunks[:15]
    print(f"   Sending {len(test_chunks)} chunks to Jina v3 -> Pinecone...")
    
    upserted = embed_and_upsert_chunks(test_chunks, source_file=os.path.basename(file_path))
    
    print(f"   [OK] Upserted {upserted} vectors successfully.")
    print("\n" + "="*50)
    print("[DRY RUN SUCCESSFUL! API Keys and Pipline flow are verified]")
    print("="*50 + "\n")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
