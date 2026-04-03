"""Quick status check — what's done, what's pending."""
from app.db.supabase_client import get_all_active_files
from app.db.pinecone_client import get_index

# 1. Supabase Registry
print("=" * 60)
print("📋 SUPABASE REGISTRY (fp_file_registry_v2)")
print("=" * 60)
entries = get_all_active_files()
if entries:
    for e in entries:
        print(f"  ✅ {e['file_name']} | chunks={e.get('chunk_count','?')} | status={e['status']}")
else:
    print("  (empty — no files registered yet)")

# 2. Pinecone Index
print("\n" + "=" * 60)
print("📊 PINECONE INDEX (fp-bot-v2)")
print("=" * 60)
index = get_index()
stats = index.describe_index_stats()
print(f"  Total vectors: {stats.total_vector_count}")
print(f"  Namespaces: {dict(stats.namespaces) if stats.namespaces else 'default'}")
