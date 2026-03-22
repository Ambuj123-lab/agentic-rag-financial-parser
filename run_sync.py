import os
import sys
import logging
import asyncio

# Configure logging to console
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

from app.rag.sync import sync_core_brain

def main():
    print("\n" + "="*50)
    print("🚀 STARTING SYNC (PHASE 2 - COST EFFECTIVE)")
    print("="*50 + "\n")
    
    summary = sync_core_brain()
    
    print("\n" + "="*50)
    print("✅ SYNC COMPLETED")
    print("="*50 + "\n")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
