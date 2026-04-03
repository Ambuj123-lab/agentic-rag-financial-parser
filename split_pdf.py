"""
Split ALL large PDFs (>50MB) into LlamaParse-safe chunks.
LlamaParse file upload limit: ~50MB
"""
import fitz
import os

RAW = os.path.join(os.getcwd(), "data", "raw_pdf")

# Files that need splitting (>50MB)
splits_needed = {
    # Already split: ITA1961 (4 parts exist) — skip
    "Income-tax-Act-2025_2026-01-08_05-25-02_9f98ce_en.pdf": {
        "parts": [
            (0, 249, "ITA2025_Part1_P1to250.pdf"),
            (250, 499, "ITA2025_Part2_P251to500.pdf"),
            (500, None, "ITA2025_Part3_P501to555.pdf"),  # None = end of doc
        ]
    },
    "Income-tax-Rules_1962-01-07_01-11-59_a23933_en.pdf": {
        "parts": [
            (0, 249, "ITRules1962_Part1_P1to250.pdf"),
            (250, 499, "ITRules1962_Part2_P251to500.pdf"),
            (500, None, "ITRules1962_Part3_P501to625.pdf"),
        ]
    },
}

for src_name, config in splits_needed.items():
    src_path = os.path.join(RAW, src_name)
    if not os.path.exists(src_path):
        print(f"❌ NOT FOUND: {src_name}")
        continue
    
    doc = fitz.open(src_path)
    size_mb = os.path.getsize(src_path) / 1024 / 1024
    print(f"\n📄 {src_name} | {doc.page_count} pages | {size_mb:.1f} MB")
    
    for start, end, part_name in config["parts"]:
        if end is None:
            end = doc.page_count - 1
        out_path = os.path.join(RAW, part_name)
        part = fitz.open()
        part.insert_pdf(doc, from_page=start, to_page=end)
        part.save(out_path)
        part_mb = os.path.getsize(out_path) / 1024 / 1024
        print(f"  ✅ {part_name} | {part.page_count} pages | {part_mb:.1f} MB")
        part.close()
    
    doc.close()

# Summary of ALL files and their sizes
print("\n" + "=" * 60)
print("📊 ALL PDFs IN raw_pdf (sorted by size):")
print("=" * 60)
files = [(f, os.path.getsize(os.path.join(RAW, f))) for f in os.listdir(RAW) if f.endswith('.pdf')]
files.sort(key=lambda x: x[1], reverse=True)
for name, size in files:
    mb = size / 1024 / 1024
    flag = "⚠️ >50MB" if mb > 50 else "✅"
    print(f"  {flag} {mb:>7.1f} MB | {name}")
