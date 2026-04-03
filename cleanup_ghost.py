"""Clean up the failed 0-chunk ghost entry from last night's run."""
from app.db.supabase_client import get_supabase, REGISTRY_TABLE

supabase = get_supabase()

# Delete the ghost entry (0 chunks = failed parse from last night)
result = supabase.table(REGISTRY_TABLE).delete().eq(
    "file_name", "Income-tax-Act-1961_2025_2026-01-06_07-59-33_dd7258_en.pdf"
).execute()
print(f"Deleted ghost entry: {result.data}")

# Verify
entries = supabase.table(REGISTRY_TABLE).select("file_name, chunk_count, status").execute()
print(f"\nRemaining entries:")
for e in entries.data:
    print(f"  {e['file_name']} | chunks={e['chunk_count']} | status={e['status']}")
