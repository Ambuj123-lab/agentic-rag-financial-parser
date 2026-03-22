"""
Quality Inspector: Pulls REAL chunk text from Pinecone to visually verify parsing quality.
Shows tables, symbols, math formulas, headings from each document.
"""
import os, sys, random
from dotenv import load_dotenv
load_dotenv()

from app.core.config import get_settings
from app.core.constants import LLAMA_TIER_MAPPING
from app.db.pinecone_client import get_index
from app.rag.embedder import embed_texts

settings = get_settings()

# Documents to spot-check (one from each tier)
SPOT_CHECK = [
    ("Finance_Bill.pdf", "Agentic - Tax Tables & Slabs"),
    ("budget_at_a_glance.pdf", "Agentic Plus - Charts & Figures"),
    ("Key Features of Budget 2026-27.pdf", "Agentic Plus - Scheme Tables"),
    ("constitution of india.pdf", "Cost Effective - Articles & Sections"),
    ("RBI Master Direction KYC.pdf", "Cost Effective - KYC Rules"),
    ("Employees' Provident Funds Scheme.1952.pdf", "PyMuPDF FREE - PF Rules"),
    ("memorandum.pdf", "Agentic - Explanatory Notes"),
    ("budget_speech_2026-2027.pdf", "Cost Effective - FM Speech"),
]

def query_sample_chunks(index, source_file, n=3):
    """Query Pinecone for sample chunks from a specific source file."""
    # Use a generic finance query to get relevant chunks
    queries = [
        "tax slab rates percentage income",
        "budget allocation expenditure crores",
        "article section clause schedule",
        "KYC verification identity document",
        "pension provident fund contribution",
        "revenue deficit fiscal surplus",
    ]
    
    # Pick a query relevant to the document
    query_text = random.choice(queries)
    
    # Embed the query with retrieval.query task
    import httpx
    headers = {
        "Authorization": f"Bearer {settings.JINA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "jina-embeddings-v3",
        "input": [query_text],
        "dimensions": 256,
        "task": "retrieval.query",
    }
    
    with httpx.Client(timeout=30.0) as client:
        resp = client.post("https://api.jina.ai/v1/embeddings", json=payload, headers=headers)
    
    if resp.status_code != 200:
        return []
    
    query_vector = resp.json()["data"][0]["embedding"]
    
    # Query Pinecone with source filter
    results = index.query(
        vector=query_vector,
        top_k=n,
        include_metadata=True,
        filter={"source_file": {"$eq": source_file}}
    )
    
    return results.get("matches", [])


def main():
    index = get_index()
    
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("  CHUNK QUALITY INSPECTION REPORT")
    output_lines.append("  Each document: 2-3 real chunks shown with FULL text")
    output_lines.append("=" * 80)
    
    for source_file, label in SPOT_CHECK:
        output_lines.append(f"\n{'#' * 80}")
        output_lines.append(f"# {source_file}")
        output_lines.append(f"# Tier: {label}")
        output_lines.append(f"{'#' * 80}")
        
        try:
            matches = query_sample_chunks(index, source_file, n=2)
            
            if not matches:
                output_lines.append("  (!) No chunks found for this file")
                continue
            
            for i, match in enumerate(matches):
                meta = match.get("metadata", {})
                score = round(match.get("score", 0), 4)
                chunk_type = meta.get("chunk_type", "?")
                page = meta.get("page", "?")
                loader = meta.get("loader", "?")
                text_preview = meta.get("text_preview", "(no text)")
                parent_text = meta.get("parent_text", "(no parent)")
                
                output_lines.append(f"\n  --- Sample {i+1} (score={score}, page={page}, type={chunk_type}) ---")
                output_lines.append(f"  Loader: {loader}")
                output_lines.append(f"")
                output_lines.append(f"  [CHUNK TEXT (what gets embedded as vector)]:")
                output_lines.append(f"  {text_preview[:800]}")
                output_lines.append(f"")
                output_lines.append(f"  [PARENT TEXT (what LLM reads for context)]:")
                output_lines.append(f"  {parent_text[:1200]}")
                output_lines.append(f"  {'.' * 40}")
                
        except Exception as e:
            output_lines.append(f"  (!) Error querying: {e}")
    
    output_lines.append(f"\n{'=' * 80}")
    output_lines.append("  INSPECTION COMPLETE - Check tables, formulas, symbols above")
    output_lines.append(f"{'=' * 80}")
    
    # Write to file (avoids Windows console unicode issues)
    report_path = os.path.join(os.getcwd(), "quality_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    print(f"Report written to: {report_path}")
    print("Open quality_report.txt in VS Code to inspect chunk quality!")

if __name__ == "__main__":
    main()
