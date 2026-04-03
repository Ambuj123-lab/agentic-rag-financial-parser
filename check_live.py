import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone

def check_live():
    load_dotenv()
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        idx = pc.Index(os.getenv("PINECONE_INDEX_NAME", "fp-bot-v2"))
        
        print("\n" + "="*50)
        print("🌟 LIVE PINECONE DB UPLOAD MONITOR 🌟")
        print("="*50)
        print("Ye script har 3 second me refresh hoke batayegi ki Jina AI ne")
        print("Pinecone me kitne vectors (chunks) daal diye hain.\n")
        
        last_count = -1
        while True:
            stats = idx.describe_index_stats()
            current_count = stats.total_vector_count
            
            if current_count != last_count:
                print(f"🚀 LIVE VECTORS UPLOADED IN DATABASE: {current_count}")
                last_count = current_count
                
            time.sleep(3)
            
    except Exception as e:
        print(f"Error checking Pinecone: {e}")

if __name__ == "__main__":
    check_live()
