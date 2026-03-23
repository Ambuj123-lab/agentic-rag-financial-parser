# ==========================================
# Agentic Financial Parser - Core Constants
# ==========================================

# 1. Chunking Hyperparameters
# ---------------------------
# For Parent-Child Chunking (PyMuPDF - Free temp uploads)
PARENT_CHUNK_SIZE = 2000
PARENT_CHUNK_OVERLAP = 200

CHILD_CHUNK_SIZE = 400
CHILD_CHUNK_OVERLAP = 50

# For MarkdownHeaderTextSplitter (LlamaParse Output)
# Headers dictate splitting rather than exact char counts, but we keep limits
MAX_MARKDOWN_CHUNK_SIZE = 3000

# 2. Embedding Dimensions
# ---------------------------
# Jina Embeddings v3 MRL Dimensions (Keeps DB small & cheap)
EMBEDDING_DIMENSIONS = 256
EMBED_BATCH_SIZE = 5  # Small batches to protect memory and avoid rate limits

# 3. Security & Limits (Crucial for 512MB RAM)
# ---------------------------
MAX_UPLOAD_SIZE_MB = 10
MAX_PDF_PAGES = 500
CHUNKED_UPLOAD_READ_SIZE = 1024 * 1024  # 1MB per read

# 4. LlamaParse Tier Assignment
# ---------------------------
# Filenames MUST exactly match data/raw_pdf/ on disk
LLAMA_TIER_MAPPING = {
    # Premium Data (Images, Infographics, Complex Tables) -> Agentic Plus (45 credits/pg)
    "budget_at_a_glance.pdf": "Agentic Plus",
    "Key Features of Budget 2026-27.pdf": "Agentic Plus",

    # Dense Structured Data (Tax Tables, Math, Legal Sections) -> Agentic (10 credits/pg)
    "Finance_Bill.pdf": "Agentic",
    "memorandum.pdf": "Agentic",

    # Normal Structured Data -> Cost Effective (3 credits/pg)
    "budget_speech_2026-2027.pdf": "Cost Effective",
    "RBI Master Direction KYC.pdf": "Cost Effective",
    "Employees' Pension Scheme, 1995.pdf": "Cost Effective",
    "constitution of india.pdf": "Cost Effective",

    # Plain Text -> PyMuPDF (0 credits, 100% free, runs locally)
    "Employees' Provident Funds Scheme.1952.pdf": "PyMuPDF",

    # Complex Diagrams & Flowcharts -> Agentic Plus (Sonnet 3.5 VLM)
    "Building_Real_AI_Systems_Complete (1).pdf": "Agentic Plus",
}

# 5. Page Filtering (for large docs — parse only the useful pages)
# ---------------------------
# LlamaParse target_pages uses 0-indexed page numbers
# Finance Bill: Only tax slabs, surcharge rates, TDS tables
PAGE_FILTER_MAPPING = {
    "Finance_Bill.pdf": "9-39,105-116,127-132",
    # Other PDFs: parse all pages (no entry = parse fully)
}
