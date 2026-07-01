import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

from app.rag.sync import _process_changed_file
from app.rag.parser import get_file_hash
from app.db.pinecone_client import delete_vectors_by_filter
from app.db.pinecone_client import get_pinecone_client # Initialize

def force_sync_constitution():
    filename = "constitution of india.pdf"
    file_path = os.path.join(os.getcwd(), "data", "raw_pdf", filename)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
        
    print("\n" + "="*50)
    print(f"🚀 FORCE SYNCING ONLY: {filename}")
    print("="*50 + "\n")
    
    delete_vectors_by_filter({"source_file": {"$eq": filename}}) # Safe delete
    
    current_hash = get_file_hash(file_path)
    file_size = os.path.getsize(file_path)
    
    summary = {"added": [], "updated": [], "unchanged": [], "deleted": [], "errors": []}
    
    try:
        _process_changed_file(filename, file_path, current_hash, file_size, summary)
        print("\n✅ FORCE SYNC SUCCESSFUL!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    force_sync_constitution()
