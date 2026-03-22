"""
pii_shield.py — Lightweight PII Masking (No spaCy — regex only)
================================================================
Masks sensitive data in user queries BEFORE sending to LLM.
Designed for 512MB RAM — zero ML overhead, pure regex.

Detects & masks:
  - Aadhaar numbers (12 digits: XXXX XXXX XXXX)
  - PAN numbers (ABCDE1234F pattern)
  - Mobile numbers (+91, 10 digits)
  - Email addresses
  - Bank account numbers (9-18 digit sequences near keywords)
  - IFSC codes (4 letters + 0 + 6 chars)
"""

import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

# Pattern definitions
PII_PATTERNS = [
    {
        "name": "Aadhaar",
        "pattern": r"\b(\d{4}[\s\-]?\d{4}[\s\-]?\d{4})\b",
        "mask": "XXXX-XXXX-XXXX",
        "validator": lambda m: len(re.sub(r"[\s\-]", "", m.group(1))) == 12,
    },
    {
        "name": "PAN",
        "pattern": r"\b([A-Z]{5}\d{4}[A-Z])\b",
        "mask": "XXXXX0000X",
        "validator": None,
    },
    {
        "name": "Mobile",
        "pattern": r"(?:\+91[\s\-]?)?(?:\b)([6-9]\d{9})\b",
        "mask": "XXXXXXXXXX",
        "validator": None,
    },
    {
        "name": "Email",
        "pattern": r"\b([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})\b",
        "mask": "***@***.***",
        "validator": None,
    },
    {
        "name": "IFSC",
        "pattern": r"\b([A-Z]{4}0[A-Z0-9]{6})\b",
        "mask": "XXXXXXXXXXX",
        "validator": None,
    },
    {
        "name": "BankAccount",
        "pattern": r"(?:account[\s\-:]*(?:no|number|num)?[\s\-:]*)\b(\d{9,18})\b",
        "mask": "XXXXXXXXXX",
        "validator": None,
    },
]


def mask_pii(text: str) -> Tuple[str, list]:
    """
    Scan text and replace any detected PII with masks.
    
    Returns:
        (masked_text, detections_list)
        
    detections_list: [{"type": "Aadhaar", "masked": True}, ...]
    """
    detections = []
    masked_text = text
    
    for rule in PII_PATTERNS:
        matches = list(re.finditer(rule["pattern"], masked_text, re.IGNORECASE if rule["name"] in ["Email", "BankAccount"] else 0))
        
        for match in reversed(matches):  # Reverse to preserve indices
            # Run validator if exists
            if rule["validator"] and not rule["validator"](match):
                continue
            
            original = match.group(1) if match.lastindex else match.group(0)
            masked_text = masked_text[:match.start(1 if match.lastindex else 0)] + rule["mask"] + masked_text[match.end(1 if match.lastindex else 0):]
            
            detections.append({
                "type": rule["name"],
                "masked": True,
                "score": 1.0,
                "start": match.start(1 if match.lastindex else 0),
                "end": match.end(1 if match.lastindex else 0)
            })
            logger.info(f"🛡️ PII Shield: Masked {rule['name']}")
    
    return masked_text, detections


def get_pii_badge(detections: list) -> str:
    """
    Generate a precision badge string for the response.
    Shows what PII types were detected and masked.
    """
    if not detections:
        return ""
    
    types = set(d["type"] for d in detections)
    badges = ", ".join(f"`{t}`" for t in sorted(types))
    return f"\n\n> 🛡️ **PII Shield Active** — Detected & masked: {badges}. Your data never reaches the AI model."
