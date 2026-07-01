"""
sync_one_file.py — Sync ANY single file to Pinecone + Supabase
================================================================
Usage:
    python sync_one_file.py "Finance Act 2026.pdf"
    python sync_one_file.py "RBI Master Direction KYC.pdf"

It will:
 - Auto-detect the correct parser (LlamaParse/PyMuPDF) from constants.py
 - Auto-detect the correct chunking strategy from chunker.py
 - Delete old vectors from Pinecone
 - Upload new clean vectors
 - Update Supabase registry
"""
import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

from app.rag.sync import sync_core_brain

def main():
    if len(sys.argv) < 2:
        print("\n❌ ERROR: Filename nahi diya!")
        print("Usage: python sync_one_file.py \"Finance Act 2026.pdf\"")
        sys.exit(1)

    filename = sys.argv[1]

    print("\n" + "="*50)
    print(f"🚀 FORCE SYNCING: {filename}")
    print("="*50 + "\n")

    summary = sync_core_brain(target_filename=filename)

    print("\n" + "="*50)
    if summary.get("errors"):
        print(f"❌ ERRORS: {summary['errors']}")
    else:
        print(f"✅ SYNC SUCCESSFUL!")
        if summary.get("added"):
            print(f"   🆕 Added: {summary['added']}")
        if summary.get("updated"):
            print(f"   🔄 Updated: {summary['updated']}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
