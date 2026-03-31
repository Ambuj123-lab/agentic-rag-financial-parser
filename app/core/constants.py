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
# User has multiple LlamaParse accounts (10k credits each).
# Strategy: Use BEST possible tier for every file. No compromise on quality.

LLAMA_TIER_MAPPING = {
    # 🔴 TIER 1: Agentic Plus (45 Credits/Page) — Visual-heavy files (diagrams, infographics, charts)
    "budget_at_a_glance.pdf": "Agentic Plus",                        # 25 pg  → ~1,125 cr
    "Key Features of Budget 2026-27.pdf": "Agentic Plus",             # 23 pg  → ~1,035 cr
    "Building_Real_AI_Systems_Complete (1).pdf": "Agentic Plus",      # 77 pg  → ~3,465 cr
    "FAQs-on-Interplay-and-Transition.pdf": "Agentic Plus",           # 99 pg  → ~4,455 cr

    # 🟡 TIER 2: Agentic (10 Credits/Page) — ALL legal/financial structured docs (BEST for tables+sections)
    "Income-tax-Act-1961_2025_2026-01-06_07-59-33_dd7258_en.pdf": "Agentic",  # 1130 pg → ~11,300 cr
    "En-Notified-IT-Rules-2026-20-03-2026.pdf": "Agentic",            # 976 pg → ~9,760 cr
    "Income-tax-Rules_1962-01-07_01-11-59_a23933_en.pdf": "Agentic",  # 625 pg → ~6,250 cr
    "Income-tax-Act-2025_2026-01-08_05-25-02_9f98ce_en.pdf": "Agentic",  # 555 pg → ~5,550 cr
    "constitution of india.pdf": "Agentic",                           # 402 pg → ~4,020 cr
    "Finance_Bill.pdf": "Agentic",                                    # 232 pg → ~2,320 cr
    "Finance Act 2026.pdf": "Agentic",                                # 121 pg → ~1,210 cr
    "RBI Master Direction KYC.pdf": "Agentic",                        # 107 pg → ~1,070 cr
    "Finance Act 2024.pdf": "Agentic",                                # 103 pg → ~1,030 cr
    "memorandum.pdf": "Agentic",                                      # 100 pg → ~1,000 cr
    "Finance act 2025.pdf": "Agentic",                                # 90 pg  → ~900 cr
    "budget_speech_2026-2027.pdf": "Agentic",                         # 65 pg  → ~650 cr
    "Employees' Pension Scheme, 1995.pdf": "Agentic",                 # 28 pg  → ~280 cr
    "_Tax-Rates_2025-12-20_03-49-02_cfd926_en.pdf": "Agentic",       # 6 pg   → ~60 cr
    "Circular-No 10 of 2022- 206AB and 206CCA.pdf": "Agentic",       # 4 pg   → ~40 cr

    # 🔵 TIER 3: PyMuPDF (0 Credits / 100% Free / Local) — Pure plain text, no tables
    "Employees' Provident Funds Scheme.1952.pdf": "PyMuPDF",          # 99 pg  → FREE
}

# 5. Page Filtering (for large docs — parse only the useful pages)
# ---------------------------
# LlamaParse target_pages uses 0-indexed page numbers
PAGE_FILTER_MAPPING = {
    "Finance_Bill.pdf": "9-39,105-116,127-132",
    # You can specify exact page ranges later to save credits! e.g., "0-10, 50-60"
    "Income-tax-Act-1961_2025_2026-01-06_07-59-33_dd7258_en.pdf": "0-899",  # PART 1: 900pg × 10cr = 9,000cr
    "Income-tax-Act-2025_2026-01-08_05-25-02_9f98ce_en.pdf": "",
    "Income-tax-Rules_1962-01-07_01-11-59_a23933_en.pdf": "",
}

# 6. Metadata: Auto-Resolve Document Types (Zero API Cost)
# ---------------------------
DOC_TYPE_MAPPING = {
    "Income-tax-Act": "act",
    "Finance Act": "act",
    "Finance_Bill": "bill",
    "Income-tax-Rules": "rules",
    "IT-Rules": "rules",
    "budget": "budget",
    "memorandum": "memorandum",
    "constitution": "constitution",
    "RBI": "circular",
    "Circular": "circular",
    "FAQs": "faq",
    "Employees": "scheme",
    "Tax-Rates": "reference",
    "Key Features": "budget",
    "Building_Real": "book",
}

