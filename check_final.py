import os
from dotenv import load_dotenv
from supabase import create_client
from pinecone import Pinecone

def check_final():
    load_dotenv()
    # Read Supabase
    sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    rows = sb.table("fp_file_registry_v2").select("file_name, chunk_count").execute()
    
    # Read Pinecone
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        idx = pc.Index(os.getenv("PINECONE_INDEX_NAME", "fp-bot-v2"))
        stats = idx.describe_index_stats()
        total_vectors = stats.total_vector_count
    except Exception as e:
        total_vectors = f"Error: {e}"

    print("\n" + "=" * 80)
    print("🔥 CONCRETE EVIDENCE: FINAL RAG BRAIN STATUS 🔥")
    print("=" * 80)
    
    total_files = len(rows.data)
    total_chunks = sum((r.get('chunk_count', 0) or 0) for r in rows.data)
    
    print(f"✅ Total PDF Files Indexed : {total_files}")
    print(f"✅ Total Vectors in Pinecone : {total_vectors}")
    print("-" * 80)
    
    # Sort files alphabetically for easy reading
    sorted_rows = sorted(rows.data, key=lambda x: x['file_name'])
    for i, r in enumerate(sorted_rows, 1):
        chunks = r.get('chunk_count', 0) or 0
        print(f"{i:02d}. {r['file_name'][:55]:<57} | Chunks: {chunks:<5}")
        
    print("=" * 80 + "\n")

if __name__ == "__main__":
    check_final()
