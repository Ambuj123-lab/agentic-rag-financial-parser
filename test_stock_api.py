import asyncio
import os
from app.rag.graph import run_query

async def main():
    # Setup test env vars if needed
    
    print("Testing Live Stock Query...")
    result = await run_query("What is the share price of Reliance?", "test@example.com")
    print("\n--- RESULT ---")
    print("Answer:", result["answer"])
    print("Confidence:", result["confidence"])
    print("Sources:", result["sources"])
    print("Web/Stock Search Flag:", result["is_web_search"], result.get("is_stock_search", False))
    print("--------------\n")

if __name__ == "__main__":
    asyncio.run(main())
