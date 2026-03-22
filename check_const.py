import os
import re
import fitz

data_dir = r"d:\Ambuj\Projects\Agentic-Financial-Parser\data\raw_pdf"
filepath = os.path.join(data_dir, "Constitution of India.pdf")

if not os.path.exists(filepath):
    print(f"FILE NOT FOUND: {filepath}")
else:
    doc = fitz.open(filepath)
    total = len(doc)
    print(f"Opening {filepath} with {total} pages")
    
    table_pages = []
    hindi_pages = []
    
    # just look at a few pages roughly
    for pg_idx in range(min(50, total)):
        page = doc.load_page(pg_idx)
        text = page.get_text("text")
        if "TABLE" in text or sum(1 for l in text.split('\n') if len(l)>3 and len(l)<50) > min(10, len(text.split('\n'))/2):
            table_pages.append(pg_idx + 1)
            
    print(f"Total pages: {total}")
    print(f"Rough table pages in first 50: {table_pages}")
    
    # let's write a full analysis script
