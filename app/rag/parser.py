"""
parser.py — Hybrid Document Parser
===================================
Decides which loader to use for each PDF based on the tier mapping in constants.py.

LlamaParse Tiers:
  - Agentic Plus (45 cr/pg): Budget at a Glance, Key Features (Images, Infographics)
  - Agentic (10 cr/pg): Finance Bill, Memorandum (Complex Tables, Math)
  - Cost Effective (3 cr/pg): RBI KYC, Pension, Constitution, Budget Speech (Structured)
  
PyMuPDF (Free, 0 credits):
  - PF Scheme 1952 (Plain text, no tables)
  - All temporary user uploads (to save LlamaParse credits)
"""

import os
import logging
import hashlib
from typing import Optional

from app.core.config import get_settings
from app.core.constants import LLAMA_TIER_MAPPING, PAGE_FILTER_MAPPING

settings = get_settings()
logger = logging.getLogger(__name__)


def get_file_hash(file_path: str) -> str:
    """Generate SHA-256 hash of a file for deduplication."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_loader_tier(filename: str) -> str:
    """
    Look up the LlamaParse tier for a given filename.
    If not found in our mapping, default to PyMuPDF (free).
    """
    return LLAMA_TIER_MAPPING.get(filename, "PyMuPDF")


def parse_with_pymupdf(file_path: str) -> list[dict]:
    """
    Parse a PDF using PyMuPDF (fitz). 100% Free, runs locally.
    Returns a list of dicts: [{"page": 1, "text": "..."}, ...]
    
    Best for: Plain text PDFs, temporary user uploads.
    Limitation: Tables will be messy, images are ignored.
    """
    import fitz  # PyMuPDF

    docs = []
    try:
        pdf = fitz.open(file_path)
        logger.info(f"📖 PyMuPDF: Parsing '{os.path.basename(file_path)}' ({len(pdf)} pages)")

        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text = page.get_text("text")
            if text.strip():
                docs.append({
                    "page": page_num + 1,
                    "text": text.strip(),
                    "source": os.path.basename(file_path),
                    "loader": "PyMuPDF"
                })

        pdf.close()
        logger.info(f"✅ PyMuPDF: Extracted {len(docs)} pages from '{os.path.basename(file_path)}'")
    except Exception as e:
        logger.error(f"❌ PyMuPDF parsing failed for '{file_path}': {e}")
        raise

    return docs


def parse_with_llamaparse(file_path: str, tier: str) -> list[dict]:
    """
    Parse a PDF using LlamaParse Cloud API.
    Returns Markdown-formatted text per page.
    
    Tier → parsing_instruction mapping:
      - "Agentic Plus": Premium mode for images/infographics
      - "Agentic": For complex tables and mathematical formulas
      - "Cost Effective": For structured but simpler documents
    
    Supports target_pages for partial parsing (e.g., Finance Bill specific pages).
    """
    from llama_parse import LlamaParse

    filename = os.path.basename(file_path)

    # Map our tier names to LlamaParse config
    tier_config = {
        "Agentic Plus": {
            "result_type": "markdown",
            "parsing_instruction": (
                "This is an Indian Government Budget document containing infographics, "
                "charts, complex tables with merged cells, and financial figures in ₹ crores. "
                "Extract ALL tables preserving their structure as Markdown tables. "
                "Preserve all numerical data exactly as shown (no rounding). "
                "For charts/infographics, describe them in structured detail."
            ),
            "premium_mode": True,
        },
        "Agentic": {
            "result_type": "markdown",
            "parsing_instruction": (
                "This is an Indian financial/legal document with complex tables, "
                "mathematical formulas, tax calculations, surcharge rates, and sections. "
                "Extract ALL tables as properly formatted Markdown tables. "
                "Preserve section/chapter hierarchy using Markdown headers (# ## ###). "
                "Keep all numerical values, percentages, and formulas exactly as written."
            ),
            "premium_mode": True,
        },
        "Cost Effective": {
            "result_type": "markdown",
            "parsing_instruction": (
                "This is a structured Indian government document with articles, "
                "sections, sub-sections, schedules, and serial-numbered tables. "
                "Preserve the hierarchical structure using Markdown headers. "
                "Extract tables as Markdown tables. Keep all numbering intact."
            ),
            "premium_mode": False,
        }
    }

    config = tier_config.get(tier, tier_config["Cost Effective"])

    # Build LlamaParse kwargs
    parser_kwargs = {
        "api_key": settings.LLAMA_CLOUD_API_KEY,
        "result_type": config["result_type"],
        "system_prompt": config["parsing_instruction"],
        "premium_mode": config["premium_mode"],
        "verbose": True,
    }

    # Add page filtering if specified (e.g., Finance Bill: only tax-related pages)
    page_filter = PAGE_FILTER_MAPPING.get(filename)
    if page_filter:
        parser_kwargs["target_pages"] = page_filter
        logger.info(f"📋 Page filter active for '{filename}': pages {page_filter}")

    try:
        logger.info(f"☁️ LlamaParse [{tier}]: Parsing '{filename}'...")

        parser = LlamaParse(**parser_kwargs)

        # LlamaParse returns a list of Document objects
        documents = parser.load_data(file_path)

        docs = []
        for i, doc in enumerate(documents):
            text = doc.text if hasattr(doc, 'text') else str(doc)
            if text.strip():
                docs.append({
                    "page": i + 1,
                    "text": text.strip(),
                    "source": filename,
                    "loader": f"LlamaParse-{tier}",
                    "tier": tier
                })

        logger.info(f"✅ LlamaParse [{tier}]: Extracted {len(docs)} sections from '{filename}'")
        return docs

    except Exception as e:
        logger.error(f"❌ LlamaParse [{tier}] failed for '{filename}': {e}")
        raise


def parse_document(file_path: str, is_temporary: bool = False) -> list[dict]:
    """
    Main entry point: Automatically selects the right parser for each PDF.
    
    - Core brain PDFs: Uses the tier from LLAMA_TIER_MAPPING
    - Temporary user uploads: Always uses PyMuPDF (free, to protect credits)
    """
    filename = os.path.basename(file_path)

    if is_temporary:
        logger.info(f"📋 Temp upload detected: '{filename}' → Using PyMuPDF (Free)")
        return parse_with_pymupdf(file_path)

    tier = get_loader_tier(filename)

    if tier == "PyMuPDF":
        return parse_with_pymupdf(file_path)
    else:
        return parse_with_llamaparse(file_path, tier)
