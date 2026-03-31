import fitz  # PyMuPDF
import os

pdf_dir = r"d:\Ambuj\Projects\Agentic-Financial-Parser\data\raw_pdf"

print("PDF Page Counts:")
print("-" * 30)

for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        filepath = os.path.join(pdf_dir, filename)
        try:
            doc = fitz.open(filepath)
            print(f"{filename} | Pages: {len(doc)} | Size: {os.path.getsize(filepath) / (1024*1024):.2f} MB")
        except Exception as e:
            print(f"{filename} : ERROR - {e}")
