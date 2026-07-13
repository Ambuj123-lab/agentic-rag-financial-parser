import os
import requests
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

print(f"🔍 Checking Live Database: {PINECONE_INDEX_NAME}")

def embed_query(query: str):
    url = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JINA_API_KEY}"
    }
    data = {
        "model": "jina-embeddings-v3",
        "task": "retrieval.query",
        "dimensions": 256,
        "input": [query]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["data"][0]["embedding"]

# 1. Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# 2. Search for Article 19
query_text = "What is Article 19 of the Constitution?"
print(f"📝 Searching for: '{query_text}'")

query_vector = embed_query(query_text)

# 3. Fetch top 10 chunks from Constitution
results = index.query(
    vector=query_vector,
    top_k=10,
    include_metadata=True,
    filter={"source_file": {"$eq": "constitution of india.pdf"}}
)

print(f"\n✅ Found {len(results.matches)} chunks. Here are the top results:\n")
print("="*60)

for i, match in enumerate(results.matches):
    score = match.score * 100
    text = match.metadata.get("text_preview", "").replace("\n", " ")
    print(f"Result {i+1} | Score: {score:.1f}%")
    print(f"Text: {text[:200]}...")
    print("-" * 60)
