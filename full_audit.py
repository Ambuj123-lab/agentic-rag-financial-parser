"""
FULL QUALITY AUDIT — Scans ALL 3,854 vectors in Pinecone
Checks: empty text, broken tables, garbled characters, chunk size anomalies
"""
import os, sys, re, json
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()

from app.core.config import get_settings
from app.db.pinecone_client import get_index

settings = get_settings()

def audit_chunk(meta, chunk_id, score=0):
    """Audit a single chunk's metadata for quality issues."""
    issues = []
    text = meta.get("text_preview", "")
    parent = meta.get("parent_text", "")
    chunk_type = meta.get("chunk_type", "unknown")
    source = meta.get("source_file", "unknown")
    page = meta.get("page", "?")
    
    # 1. Empty or near-empty text
    if not text or len(text.strip()) < 10:
        issues.append(f"EMPTY_CHUNK: text too short ({len(text.strip())} chars)")
    
    # 2. Garbled/corrupted characters (non-printable, excluding common unicode)
    garbled_count = sum(1 for c in text if ord(c) > 65535)
    if garbled_count > 5:
        issues.append(f"GARBLED: {garbled_count} unusual characters detected")
    
    # 3. Broken markdown table (mismatched pipes in rows)
    if "|" in text:
        table_lines = [l for l in text.split("\n") if l.strip().startswith("|")]
        if len(table_lines) >= 2:
            pipe_counts = [l.count("|") for l in table_lines]
            if len(set(pipe_counts)) > 2:  # Allow header separator to differ slightly
                issues.append(f"TABLE_MISMATCH: pipe counts vary {set(pipe_counts)}")
    
    # 4. Very long chunk (potential unsplit content)
    if len(text) > 4000:
        issues.append(f"OVERSIZED: {len(text)} chars (limit 3000)")
    
    # 5. Parent-child: parent should be longer than child
    if chunk_type == "parent_child" and parent:
        if len(parent) < len(text):
            issues.append(f"PARENT_SHORTER: parent={len(parent)} < child={len(text)}")
    
    # 6. Missing critical metadata
    if not source or source == "unknown":
        issues.append("MISSING_SOURCE")
    
    return issues


def main():
    index = get_index()
    stats = index.describe_index_stats()
    total_vectors = stats.get("total_vector_count", 0)
    
    lines = []
    lines.append("=" * 80)
    lines.append(f"  FULL QUALITY AUDIT — {total_vectors} vectors")
    lines.append("=" * 80)
    
    # Fetch ALL vectors using list + fetch approach
    # Pinecone list() returns vector IDs, then we fetch metadata in batches
    all_issues = []
    file_stats = defaultdict(lambda: {
        "total": 0, "parent_child": 0, "markdown_header": 0,
        "issues": [], "min_len": 99999, "max_len": 0, "total_len": 0,
        "has_table": 0, "has_formula": 0, "has_hindi": 0
    })
    
    lines.append(f"\nScanning all vectors from Pinecone index '{settings.PINECONE_INDEX_NAME}'...")
    
    # Use list() to get all IDs, then fetch in batches
    vector_ids = []
    for id_list in index.list():
        vector_ids.extend(id_list)
    
    lines.append(f"Found {len(vector_ids)} vector IDs. Fetching metadata in batches of 100...")
    
    total_checked = 0
    for i in range(0, len(vector_ids), 100):
        batch_ids = vector_ids[i:i+100]
        fetch_result = index.fetch(ids=batch_ids)
        
        for vid, vdata in fetch_result.get("vectors", {}).items():
            meta = vdata.get("metadata", {})
            total_checked += 1
            
            source = meta.get("source_file", "unknown")
            chunk_type = meta.get("chunk_type", "unknown")
            text = meta.get("text_preview", "")
            text_len = len(text)
            
            # Update file stats
            fs = file_stats[source]
            fs["total"] += 1
            if chunk_type == "parent_child":
                fs["parent_child"] += 1
            elif chunk_type == "markdown_header":
                fs["markdown_header"] += 1
            fs["min_len"] = min(fs["min_len"], text_len)
            fs["max_len"] = max(fs["max_len"], text_len)
            fs["total_len"] += text_len
            if "|" in text:
                fs["has_table"] += 1
            if "$" in text:
                fs["has_formula"] += 1
            hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
            if hindi_chars > 5:
                fs["has_hindi"] += 1
            
            # Audit
            issues = audit_chunk(meta, vid)
            if issues:
                for issue in issues:
                    all_issues.append(f"[{source}] page={meta.get('page','?')} | {issue}")
                    fs["issues"].append(issue)
        
        if (i // 100) % 10 == 0:
            lines.append(f"  Checked {total_checked}/{len(vector_ids)} vectors...")
    
    # Per-file report
    lines.append(f"\nTotal vectors checked: {total_checked}")
    lines.append(f"\n{'=' * 80}")
    lines.append("  PER-FILE BREAKDOWN")
    lines.append(f"{'=' * 80}")
    
    for source in sorted(file_stats.keys()):
        fs = file_stats[source]
        avg_len = fs["total_len"] // max(fs["total"], 1)
        lines.append(f"\n  {source}")
        lines.append(f"    Total Vectors:     {fs['total']}")
        lines.append(f"    Parent-Child:      {fs['parent_child']} vectors")
        lines.append(f"    Markdown-Header:   {fs['markdown_header']} vectors")
        lines.append(f"    Text Length:       min={fs['min_len']}, max={fs['max_len']}, avg={avg_len}")
        lines.append(f"    Contains Tables:   {fs['has_table']} chunks")
        lines.append(f"    Contains Formulas: {fs['has_formula']} chunks")
        lines.append(f"    Contains Hindi:    {fs['has_hindi']} chunks")
        lines.append(f"    Issues Found:      {len(fs['issues'])}")
        if fs["issues"]:
            for iss in fs["issues"][:5]:
                lines.append(f"      ! {iss}")
            if len(fs["issues"]) > 5:
                lines.append(f"      ... and {len(fs['issues'])-5} more")
    
    # Summary
    lines.append(f"\n{'=' * 80}")
    lines.append("  AUDIT SUMMARY")
    lines.append(f"{'=' * 80}")
    lines.append(f"  Total Vectors Audited:  {total_checked}")
    lines.append(f"  Total Issues Found:     {len(all_issues)}")
    lines.append(f"  Clean Vectors:          {total_checked - len(all_issues)}")
    lines.append(f"  Quality Score:          {round((total_checked - len(all_issues)) / max(total_checked, 1) * 100, 1)}%")
    
    if all_issues:
        lines.append(f"\n  ALL ISSUES:")
        for iss in all_issues[:30]:
            lines.append(f"    {iss}")
        if len(all_issues) > 30:
            lines.append(f"    ... and {len(all_issues)-30} more issues")
    
    lines.append(f"\n{'=' * 80}")
    lines.append("  AUDIT COMPLETE")
    lines.append(f"{'=' * 80}")
    
    report_path = os.path.join(os.getcwd(), "full_audit_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"Full audit report: {report_path}")
    print(f"Vectors checked: {total_checked}")
    print(f"Issues: {len(all_issues)}")

if __name__ == "__main__":
    main()
