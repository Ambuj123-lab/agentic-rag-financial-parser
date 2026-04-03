import os
from dotenv import load_dotenv
from supabase import create_client
load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
rows = sb.table("fp_file_registry_v2").select("file_name, chunk_count, status").execute()
print("\nALL DB ENTRIES:")
names = []
for r in rows.data:
    c = r.get("chunk_count", 0) or 0
    s = r.get("status", "?")
    tag = "OK" if c > 0 else "FAKE-ADDED!"
    print(f"  {r['file_name']:<55} chunks={c:<6} status={s:<8} {tag}")
    names.append(r["file_name"])
dupes = set([n for n in names if names.count(n) > 1])
zeros = [r["file_name"] for r in rows.data if (r.get("chunk_count", 0) or 0) == 0]
print(f"\nDUPLICATES: {dupes if dupes else 'NONE'}")
print(f"ZERO-CHUNK (FAKE ADDED): {zeros if zeros else 'NONE'}")
print(f"TOTAL ENTRIES: {len(rows.data)}")
