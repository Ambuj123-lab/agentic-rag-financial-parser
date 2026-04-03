import os
import fitz

target_files = [
    "En-Notified-IT-Rules-2026-20-03-2026.pdf",
    "constitution of india.pdf",
    "Finance_Bill.pdf",
    "Finance Act 2026.pdf",
    "RBI Master Direction KYC.pdf",
    "Finance Act 2024.pdf",
    "memorandum.pdf",
    "FAQs-on-Interplay-and-Transition.pdf",
    "Finance act 2025.pdf",
    "Building_Real_AI_Systems_Complete (1).pdf",
    "budget_speech_2026-2027.pdf",
    "Employees' Pension Scheme, 1995.pdf",
    "budget_at_a_glance.pdf",
    "Key Features of Budget 2026-27.pdf",
    "Circular-No 10 of 2022- 206AB and 206CCA.pdf",
    "Employees' Provident Funds Scheme.1952.pdf"
]

data_dir = r"d:\Ambuj\Projects\Agentic-Financial-Parser\data\raw_pdf"

print(f"{'File Name':<45} | {'Pages':<5} | {'Images':<8} | {'Complexity (Blocks/Pg)':<22}")
print("-" * 90)

total_pages = 0

for filename in target_files:
    path = os.path.join(data_dir, filename)
    if not os.path.exists(path):
        print(f"{filename[:43]:<45} | MISSING")
        continue

    try:
        doc = fitz.open(path)
        pages = len(doc)
        total_pages += pages
        total_images = 0
        total_blocks = 0
        
        # We sample up to the first 50 pages to keep it fast but accurate
        sample_pages = min(pages, 50)
        
        for i in range(sample_pages):
            page = doc[i]
            images = page.get_images(full=True)
            total_images += len(images)
            blocks = len(page.get_text("blocks"))
            total_blocks += blocks
            
        avg_blocks = total_blocks / sample_pages if sample_pages > 0 else 0
        img_str = f"{total_images}{'+' if pages>50 and total_images>0 else ' (total)'}"
        if pages > 50 and total_images == 0:
            img_str = "0 (sample)"
            
        print(f"{filename[:43]:<45} | {pages:<5} | {img_str:<8} | {avg_blocks:.1f}")
        doc.close()
    except Exception as e:
        print(f"{filename[:43]:<45} | ERROR: {str(e)}")

print("-" * 90)
print(f"Total Pages Remaining: {total_pages}")
