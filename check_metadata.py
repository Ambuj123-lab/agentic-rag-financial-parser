import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
idx = pc.Index(os.getenv("PINECONE_INDEX_NAME", "fp-bot-v2"))

print("="*60)
print("🔍 SEARCHING FOR 'IT RULES 2026' IN PINECONE...")
print("="*60)

# Filter explicitly for the IT Rules file
r = idx.query(
    vector=[0.01]*256,
    top_k=3,
    include_metadata=True,
    filter={"source_file": {"$eq": "En-Notified-IT-Rules-2026-20-03-2026.pdf"}}
)

for i, m in enumerate(r.matches):
    print(f"\n--- Result {i+1} ---")
    md = m.metadata or {}
    print(f"source_file: {md.get('source_file')}")
    print(f"page: {md.get('page')}")
    print(f"heading_2: {md.get('heading_2')}")
    preview = md.get('text_preview', '')[:100].replace('\n', ' ')
    print(f"Preview: {preview}...")

print("\n" + "="*60)
print("🔍 SEARCHING FOR 'ITA 1961' IN PINECONE...")
print("="*60)

# Filter explicitly for the ITA 1961 file
r2 = idx.query(
    vector=[0.01]*256,
    top_k=3,
    include_metadata=True,
    filter={"source_file": {"$eq": "ITA1961_Part1_P1to300.pdf"}}
)

for i, m in enumerate(r2.matches):
    print(f"\n--- Result {i+1} ---")
    md = m.metadata or {}
    print(f"source_file: {md.get('source_file')}")
    print(f"page: {md.get('page')}")
    preview = md.get('text_preview', '')[:100].replace('\n', ' ')
    print(f"Preview: {preview}...")

stats = idx.describe_index_stats()
print(f"\n{'='*60}")
print(f"TOTAL VECTORS IN ENTIRE DATABASE: {stats.total_vector_count}")
print(f"{'='*60}")
