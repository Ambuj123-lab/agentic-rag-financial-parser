import os
from dotenv import load_dotenv
from supabase import create_client

def delete_failed_file():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("Missing Supabase credentials in .env")
        return
        
    try:
        supabase = create_client(url, key)
        # Delete the false entry
        response = supabase.table("fp_file_registry_v2").delete().eq("file_name", "Finance Act 2024.pdf").execute()
        
        print("\n--- DATABASE CLEANUP ---")
        print("✅ Successfully deleted the empty 'Finance Act 2024.pdf' entry from Supabase.")
        print("Now you can re-run the sync command safely without it being 'Skipped'.")
        print("------------------------\n")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    delete_failed_file()
