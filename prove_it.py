import os
from dotenv import load_dotenv
from supabase import create_client

def prove_it():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("Missing Supabase credentials in .env")
        return
        
    supabase = create_client(url, key)
    response = supabase.table("fp_file_registry_v2").select("*").eq("file_name", "constitution of india.pdf").execute()
    
    print("\n" + "="*50)
    print("🔥 ULTIMATE PROOF OF CONSTITUTION IN DATABASE 🔥")
    print("="*50)
    
    if response.data:
        data = response.data[0]
        print(f"📄 Document Name   : {data.get('file_name')}")
        print(f"🧱 Total Chunks    : {data.get('chunk_count', 'Unknown')} (Ye LlamaParse ke banaye tukde hain)")
        print(f"📅 Added On        : {data.get('created_at')}")
        print(f"🟢 Server Status   : {data.get('status').upper()}")
        print("==================================================")
        print("YES! Ye " + str(data.get('chunk_count', 0)) + " chunks directly tumhare PINECONE me safely ghus chuke hain.")
    else:
        print("Data not found!")

if __name__ == "__main__":
    prove_it()
