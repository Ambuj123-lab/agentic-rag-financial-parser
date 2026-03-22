"""
Verification Script: Shows how each PDF was parsed, chunked, and stored.
Run: $env:PYTHONPATH="." ; .\venv\Scripts\python verify_parse.py
"""
import os, sys, json
from dotenv import load_dotenv
load_dotenv()

from app.core.config import get_settings
from app.core.constants import LLAMA_TIER_MAPPING, PAGE_FILTER_MAPPING
from app.db.supabase_client import get_all_active_files
from app.db.pinecone_client import get_index

settings = get_settings()

def main():
    print("=" * 70)
    print("  PARSE VERIFICATION REPORT")
    print("=" * 70)

    # 1. Supabase Registry
    print("\n[1] SUPABASE FILE REGISTRY (fp_file_registry)")
    print("-" * 70)
    active_files = get_all_active_files()

    if not active_files:
        print("  (!) No files found in registry!")
        return

    total_chunks = 0
    for f in sorted(active_files, key=lambda x: x.get("file_name", "")):
        name = f.get("file_name", "?")
        chunks = f.get("chunk_count", 0)
        size_kb = round(f.get("file_size", 0) / 1024, 1)
        file_hash = f.get("file_hash", "?")[:12]
        tier = LLAMA_TIER_MAPPING.get(name, "PyMuPDF")
        page_filter = PAGE_FILTER_MAPPING.get(name, "ALL pages")
        total_chunks += (chunks or 0)

        if tier == "Agentic Plus":
            chunker = "MarkdownHeader"
            cost = "45 cr/pg"
        elif tier == "Agentic":
            chunker = "MarkdownHeader"
            cost = "10 cr/pg"
        elif tier == "Cost Effective":
            chunker = "MarkdownHeader"
            cost = "3 cr/pg"
        else:
            chunker = "Parent-Child"
            cost = "FREE"

        print(f"\n  {name}")
        print(f"    Tier:       {tier} ({cost})")
        print(f"    Chunker:    {chunker}")
        print(f"    Chunks:     {chunks}")
        print(f"    Size:       {size_kb} KB")
        print(f"    SHA-256:    {file_hash}...")
        print(f"    Pages:      {page_filter}")

    print(f"\n  TOTAL CHUNKS across all files: {total_chunks}")

    # 2. Pinecone Stats
    print("\n" + "-" * 70)
    print("[2] PINECONE INDEX STATS")
    print("-" * 70)
    try:
        index = get_index()
        stats = index.describe_index_stats()
        print(f"  Index:        {settings.PINECONE_INDEX_NAME}")
        print(f"  Dimensions:   {stats.get('dimension', '?')}")
        print(f"  Total Vectors: {stats.get('total_vector_count', '?')}")
        ns = stats.get("namespaces", {})
        if ns:
            for ns_name, ns_data in ns.items():
                label = ns_name if ns_name else "(default)"
                print(f"  Namespace '{label}': {ns_data.get('vector_count', '?')} vectors")
    except Exception as e:
        print(f"  (!) Pinecone error: {e}")

    print("\n" + "=" * 70)
    print("  VERIFICATION COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
