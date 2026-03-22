import os
import re
import fitz

filepath = r"d:\Ambuj\Projects\Agentic-Financial-Parser\data\constitution of india.pdf"

def classify_page(text, images_count):
    tags = []
    hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
    if hindi_chars > 20:
        tags.append("HINDI")
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    short_lines = sum(1 for l in lines if 3 < len(l) < 50)
    if len(lines) > 0 and short_lines / max(len(lines), 1) > 0.55:
        tags.append("TABLE")
    table_kw = ["sr.", "sl.", "sr.no", "sl.no", "circular no", "annex", "schedule",
                 "rate of", "per cent", "₹", "rs.", "crore", "lakh",
                 "mandatory", "exempted", "nil", "total income"]
    if sum(1 for kw in table_kw if kw in text.lower()) >= 3:
        if "TABLE" not in tags:
            tags.append("TABLE")
    formula_patterns = [r'[=×÷±∑∫]', r'\b[A-Z][a-z]?\s*=\s*[A-Z]', r'per cent', r'%', r'₹']
    if sum(1 for p in formula_patterns if re.search(p, text)) >= 2:
        tags.append("FORMULA")
    if images_count > 0:
        tags.append(f"IMAGES({images_count})")
    toc_patterns = [r'\.{5,}', r'chapter\s+[ivx]+', r'contents']
    if sum(1 for p in toc_patterns if re.search(p, text.lower())) >= 2:
        tags.append("TOC/INDEX")
    if len(text.strip()) < 50:
        tags.append("BLANK")
    if not tags:
        tags.append("PLAIN_TEXT")
    return tags

def compress_ranges(pages):
    if not pages:
        return "None"
    pages = sorted(set(pages))
    ranges = []
    start = pages[0]
    end = pages[0]
    for p in pages[1:]:
        if p == end + 1:
            end = p
        else:
            ranges.append(f"{start}-{end}" if start != end else str(start))
            start = end = p
    ranges.append(f"{start}-{end}" if start != end else str(start))
    return ", ".join(ranges)

if not os.path.exists(filepath):
    print(f"FILE NOT FOUND: {filepath}")
else:
    doc = fitz.open(filepath)
    total = len(doc)
    results = []
    results.append(f"\n{'#'*90}")
    results.append(f"# FILE: constitution of india.pdf | TOTAL PAGES: {total}")
    results.append(f"{'#'*90}")
    
    table_pages = []
    hindi_pages = []
    formula_pages = []
    image_pages = []
    critical_pages = []
    skip_pages = []
    
    for pg_idx in range(total):
        page = doc.load_page(pg_idx)
        text = page.get_text("text")
        images = page.get_images(full=True)
        pg_num = pg_idx + 1
        
        tags = classify_page(text, len(images))
        
        for tag in tags:
            if tag.startswith("IMAGES"):
                image_pages.append(pg_num)
                critical_pages.append(pg_num)
        if "TABLE" in tags:
            table_pages.append(pg_num)
            critical_pages.append(pg_num)
        if "HINDI" in tags:
            hindi_pages.append(pg_num)
        if "FORMULA" in tags:
            formula_pages.append(pg_num)
            critical_pages.append(pg_num)
        if "TOC/INDEX" in tags or "BLANK" in tags:
            skip_pages.append(pg_num)
        
    doc.close()
    
    critical_pages = sorted(set(critical_pages))
    
    results.append(f"\n  === SUMMARY === ")
    results.append(f"  Total Pages: {total}")
    results.append(f"  TABLE pages ({len(table_pages)})")
    results.append(f"  HINDI pages ({len(hindi_pages)})")
    results.append(f"  FORMULA pages ({len(formula_pages)})")
    results.append(f"  IMAGE pages ({len(image_pages)})")
    results.append(f"  SKIP pages ({len(skip_pages)})")
    results.append(f"  >>> CRITICAL (LlamaParse MUST) pages ({len(critical_pages)})")
    results.append(f"  >>> PLAIN TEXT only pages: {total - len(critical_pages) - len(skip_pages)}")

    with open("const_analysis.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"Done scanning Constitution! Pages: {total}. Results saved to const_analysis.txt")
