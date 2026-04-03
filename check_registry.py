import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

try:
    print("Fetching exact processed files from Supabase fp_file_registry_v2...")
    supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    response = supabase.table("fp_file_registry_v2").select("file_name").eq("status", "processed").execute()
    
    files = [item['file_name'] for item in response.data]
    print(f"\n✅ Total unique files actually uploaded & processed in Pinecone/Supabase: {len(files)}\n")
    for f in sorted(files):
        print(" ->", f)
except Exception as e:
    print(f"Error checking Supabase: {e}")
