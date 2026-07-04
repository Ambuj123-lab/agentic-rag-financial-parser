"""
LOCAL DRY RUN — Zero API calls, zero kota waste
Simulates the ENTIRE pipeline: Parse → Clean → Chunk → Verify metadata
"""
import fitz, re, hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

doc = fitz.open(r"D:\Ambuj\Projects\Agentic-Financial-Parser\data\raw_pdf\constitution of india.pdf")

# === STEP 1: PARSER (CLEANING) ===
cleaned_pages = []
for page_num in range(doc.page_count):
    text = doc[page_num].get_text("text")
    text = re.sub(r"THE CONSTITUTION OF\s*INDIA\n\(Part.*?\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"THE CONSTITUTION OF INDIA", "", text, flags=re.IGNORECASE)
    parts = re.split(r"_{10,}", text)
    text = parts[0]
    if text.strip():
        cleaned_pages.append({"page": page_num+1, "text": text.strip(), "source": "constitution of india.pdf", "loader": "PyMuPDF"})

print(f"Pages after cleaning: {len(cleaned_pages)}")

# === STEP 2: CHUNKER (ARTICLE SPLITTING + METADATA) ===
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200, separators=["\n\n", "\n", ". ", " "])
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", ". ", " "])

all_chunks = []
for d in cleaned_pages:
    text = d["text"]
    source = d["source"]
    page = d["page"]

    parent_texts_with_meta = []
    raw_splits = re.split(r"\n(?=\d{1,3}[A-Z]*\.\s+[A-Z])", text)
    for split in raw_splits:
        split = split.strip()
        if not split:
            continue
        article_num = None
        match = re.match(r"^(\d{1,3}[A-Z]*)\.", split)
        if match:
            article_num = match.group(1)
        if len(split) > 5000:
            for sub in parent_splitter.split_text(split):
                parent_texts_with_meta.append((sub, article_num))
        else:
            parent_texts_with_meta.append((split, article_num))

    for pidx, (ptxt, anum) in enumerate(parent_texts_with_meta):
        parent_id = f"{source}_{page}_{pidx}"
        children = child_splitter.split_text(ptxt)
        for cidx, ctxt in enumerate(children):
            meta = {"source_file": source, "page": page, "parent_id": parent_id}
            if anum:
                meta["article_number"] = anum
            all_chunks.append({"text": ctxt, "metadata": meta})

# === STEP 3: VALIDATION ===
total = len(all_chunks)
with_article = sum(1 for c in all_chunks if "article_number" in c["metadata"])
without_article = total - with_article

print("\n=== ARTICLE-WISE CHECK ===")
for target in ["1", "14", "19", "21", "21A", "32", "44", "51A", "72", "110", "226", "300A", "356", "370"]:
    matches = [c for c in all_chunks if c["metadata"].get("article_number") == target]
    if matches:
        preview = matches[0]["text"][:100].replace("\n", " ")
        print(f"  Article {target:>4s}: {len(matches)} chunks | {preview}...")
    else:
        print(f"  Article {target:>4s}: NOT FOUND!")

# Noise check
noise = 0
for c in all_chunks:
    t = c["text"].lower()
    if "ins. by the constitution" in t or "subs. by the constitution" in t:
        noise += 1

print(f"\n=== FINAL REPORT ===")
print(f"Total chunks: {total}")
print(f"Chunks WITH article_number metadata: {with_article}")
print(f"Chunks WITHOUT article_number (preamble/schedules/headers): {without_article}")
print(f"Noise chunks (footnotes leaked): {noise}")
print(f"ALL CLEAN (zero noise): {noise == 0}")
