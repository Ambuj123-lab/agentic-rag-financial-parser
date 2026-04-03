from dotenv import load_dotenv
load_dotenv()
from app.db.supabase_client import get_supabase

client = get_supabase()
files = client.table('fp_file_registry_v2').select('*').eq('status', 'active').execute()

print('=' * 60)
print('SUPABASE FILE REGISTRY (fp_file_registry_v2)')
print('=' * 60)
total_chunks = 0
total_pages = 0
for f in files.data:
    chunks = f.get('chunk_count', 0)
    pages = f.get('page_count', 0)
    total_chunks += chunks
    total_pages += pages
    name = f['file_name'][:48]
    print(f"  {name:<48} | C:{chunks:>5} | P:{pages:>4}")

print('=' * 60)
print(f"Total Files:       {len(files.data)}")
print(f"Total Chunks:      {total_chunks}")
print(f"Total Pages:       {total_pages}")
print(f"Total Vectors:     14,662 (Pinecone)")
print('=' * 60)
