import os
from dotenv import load_dotenv
from supabase import create_client

def get_synced_files():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("Missing Supabase credentials in .env")
        return
        
    try:
        supabase = create_client(url, key)
        # Assuming the table name is fp_file_registry_v2 as seen in terminal logs
        result = supabase.table("fp_file_registry_v2").select("file_name, status").execute()
        
        print("\n--- ACTUAL FILES UPLOADED (SOURCE OF TRUTH) ---\n")
        if not result.data:
            print("No files found in registry.")
        else:
            for row in result.data:
                print(f"File: {row['file_name']} | Status: {row.get('status', 'uploaded')}")
        print("\n-----------------------------------------------\n")
        
    except Exception as e:
        print(f"Error querying registry: {e}")

if __name__ == "__main__":
    get_synced_files()
