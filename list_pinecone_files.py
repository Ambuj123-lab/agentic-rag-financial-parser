"""
Get ALL unique source_file values from Pinecone fp-bot-v2.
This tells us EXACTLY which PDFs have chunks in the vector DB.
"""
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
idx = pc.Index(os.getenv("PINECONE_INDEX_NAME", "fp-bot-v2"))

# Get total stats first
stats = idx.describe_index_stats()
total = stats.total_vector_count
print(f"Total vectors in fp-bot-v2: {total}")

# Sample random vectors to collect unique source_file names
# We use a dummy vector and fetch large batches
unique_files = set()
batch_size = 100
offset = 0

# Strategy: fetch chunks in multiple passes with different dummy vectors
# to maximize coverage of unique source_files
import random
for attempt in range(5):
    dummy = [random.uniform(-0.01, 0.01) for _ in range(256)]
    r = idx.query(
        vector=dummy,
        top_k=10000,  # max allowed by Pinecone
        include_metadata=True,
    )
    for m in r.matches:
        sf = (m.metadata or {}).get("source_file", "UNKNOWN")
        unique_files.add(sf)

print(f"\n{'='*60}")
print(f"UNIQUE source_file VALUES IN PINECONE fp-bot-v2:")
print(f"{'='*60}")
for i, f in enumerate(sorted(unique_files), 1):
    print(f"  {i:2d}. {f}")
print(f"\nTotal unique files: {len(unique_files)}")
