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
    "FAQs-on-Interplay-and-Transition.pdf": "Agentic",                # 99 pg

    # 🟡 TIER 2: Agentic (10 Credits/Page) — ALL legal/financial structured docs (BEST for tables+sections)
    "ITA1961_Part1_P1to300.pdf": "Agentic",                           # 300 pg → ~3,000 cr
    "ITA1961_Part2_P301to600.pdf": "Agentic",                         # 300 pg → ~3,000 cr
    "ITA1961_Part3_P601to900.pdf": "Agentic",                         # 300 pg → ~3,000 cr
    "ITA1961_Part4_P901to1130.pdf": "Agentic",                        # 230 pg → ~2,300 cr
    "En-Notified-IT-Rules-2026-20-03-2026.pdf": "Cost Effective",     # 976 pg → 976 credits (1 credit/page, NO SPLIT NEEDED)
    "ITRules1962_Part1_P1to250.pdf": "Agentic",                       # 250 pg → ~2,500 cr
    "ITRules1962_Part2_P251to500.pdf": "Agentic",                     # 250 pg → ~2,500 cr
    "ITRules1962_Part3_P501to625.pdf": "Agentic",                     # 125 pg → ~1,250 cr
    "ITA2025_Part1_P1to250.pdf": "Agentic",                           # 250 pg → ~2,500 cr
    "ITA2025_Part2_P251to500.pdf": "Agentic",                         # 250 pg → ~2,500 cr
    "ITA2025_Part3_P501to555.pdf": "Agentic",                         # 155 pg → ~1,550 cr
    "constitution of india.pdf": "Cost Effective",                    # 402 pg → ~1,200 cr
    "Finance_Bill.pdf": "Agentic",                                    # 232 pg → ~2,320 cr
    "Finance Act 2026.pdf": "Agentic",                                # 121 pg → ~1,210 cr
    "RBI Master Direction KYC.pdf": "Cost Effective",                 # 107 pg
    "Finance Act 2024.pdf": "Agentic",                                # 103 pg → ~1,030 cr
    "memorandum.pdf": "Agentic",                                      # 100 pg → ~1,000 cr
    "Finance act 2025.pdf": "Agentic",                                # 90 pg  → ~900 cr
    "budget_speech_2026-2027.pdf": "Cost Effective",                  # 65 pg
    "Employees' Pension Scheme, 1995.pdf": "Cost Effective",          # 28 pg
    "_Tax-Rates_2025-12-20_03-49-02_cfd926_en.pdf": "Agentic",       # 6 pg   → ~60 cr
    "Circular-No 10 of 2022- 206AB and 206CCA.pdf": "Cost Effective", # 4 pg

    # 🔵 TIER 3: PyMuPDF (0 Credits / 100% Free / Local) — Pure plain text, no tables
    "Employees' Provident Funds Scheme.1952.pdf": "PyMuPDF",          # 99 pg  → FREE
}

# 5. Page Filtering (for large docs — parse only the useful pages)
# ---------------------------
# LlamaParse target_pages uses 0-indexed page numbers
PAGE_FILTER_MAPPING = {
    "Finance_Bill.pdf": "9-39,105-116,127-132",
    # You can specify exact page ranges later to save credits! e.g., "0-10, 50-60"
    "Income-tax-Act-2025_2026-01-08_05-25-02_9f98ce_en.pdf": "",
    "Income-tax-Rules_1962-01-07_01-11-59_a23933_en.pdf": "",
}

# 6. Metadata: Strict Document Scope Registry (For Multi-Query Routing)
# ---------------------------
FILE_METADATA_REGISTRY = {
    # Acts (Substantive Law)
    "ITA1961_Part1_P1to300.pdf": {"doc_type": "act", "law": "income_tax", "year": "1961"},
    "ITA1961_Part2_P301to600.pdf": {"doc_type": "act", "law": "income_tax", "year": "1961"},
    "ITA1961_Part3_P601to900.pdf": {"doc_type": "act", "law": "income_tax", "year": "1961"},
    "ITA1961_Part4_P901to1130.pdf": {"doc_type": "act", "law": "income_tax", "year": "1961"},
    
    "ITA2025_Part1_P1to250.pdf": {"doc_type": "act", "law": "income_tax", "year": "2025"},
    "ITA2025_Part2_P251to500.pdf": {"doc_type": "act", "law": "income_tax", "year": "2025"},
    "ITA2025_Part3_P501to555.pdf": {"doc_type": "act", "law": "income_tax", "year": "2025"},
    
    # Rules (Procedural Law)
    "ITRules1962_Part1_P1to250.pdf": {"doc_type": "rules", "law": "income_tax", "year": "1962"},
    "ITRules1962_Part2_P251to500.pdf": {"doc_type": "rules", "law": "income_tax", "year": "1962"},
    "ITRules1962_Part3_P501to625.pdf": {"doc_type": "rules", "law": "income_tax", "year": "1962"},
    "En-Notified-IT-Rules-2026-20-03-2026.pdf": {"doc_type": "rules", "law": "income_tax", "year": "2026"},

    # Finance Acts (Amendment Laws — SEPARATE from Income Tax Acts)
    "Finance_Bill.pdf": {"doc_type": "bill", "law": "finance", "year": "2026"},
    "Finance Act 2026.pdf": {"doc_type": "finance_act", "law": "finance", "year": "2026"},
    "Finance act 2025.pdf": {"doc_type": "finance_act", "law": "finance", "year": "2025"},
    "Finance Act 2024.pdf": {"doc_type": "finance_act", "law": "finance", "year": "2024"},

    # Other Domains
    "constitution of india.pdf": {"doc_type": "constitution", "law": "civic", "year": "any"},
    "RBI Master Direction KYC.pdf": {"doc_type": "circular", "law": "rbi", "year": "any"},
    "Employees' Provident Funds Scheme.1952.pdf": {"doc_type": "scheme", "law": "epf", "year": "1952"},
    "Employees' Pension Scheme, 1995.pdf": {"doc_type": "scheme", "law": "pension", "year": "1995"},
    "budget_at_a_glance.pdf": {"doc_type": "budget", "law": "finance", "year": "2026"},
    "Key Features of Budget 2026-27.pdf": {"doc_type": "budget", "law": "finance", "year": "2026"},
    "budget_speech_2026-2027.pdf": {"doc_type": "budget", "law": "finance", "year": "2026"},
    "memorandum.pdf": {"doc_type": "memorandum", "law": "finance", "year": "2026"},
    "Circular-No 10 of 2022- 206AB and 206CCA.pdf": {"doc_type": "circular", "law": "income_tax", "year": "2022"},
    "_Tax-Rates_2025-12-20_03-49-02_cfd926_en.pdf": {"doc_type": "reference", "law": "income_tax", "year": "2025"},
}

