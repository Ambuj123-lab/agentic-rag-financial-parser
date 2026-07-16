# 10-Node Adaptive Agentic RAG Architecture 
## Feature Integration Summary: Live Stock API (10th Node)

**Date of Implementation:** July 16, 2026
**Engineer:** Ambuj Kumar Tripathi

### 1. Objective
To enhance the existing 9-node Agentic RAG architecture by introducing a 10th Node specifically dedicated to fetching real-time stock market data. This node allows the AI to answer financial market queries without relying on vector databases (Pinecone) or standard Web Search (Tavily).

### 2. Architecture & Flow
- **Classifier Node Update:** The `Classifier` was updated with a new intent (`is_stock_search = True`). If the user asks for share prices, market caps, or financial metrics (e.g., "Reliance share price"), the classifier bypasses the Retriever and Cohere reranker.
- **Stock Tool Node (The 10th Node):** A new Python tool (`app/tools/stock_tool.py`) was integrated. It leverages the `yfinance` library to fetch live data (Current Price, High/Low, Market Cap, PE Ratio) anonymously and for free.
- **Generator Node Override:** We introduced an explicit `is_stock_search` persona in `graph.py` (Line ~1087) to override the strict RAG (Tax/Law) guardrails. This allows the LLM to format the financial data into a clean Markdown Table (for Web UI) or Bullet Points (for WhatsApp).
- **Post-Process (Citations):** Added a static citation `[Yahoo Finance (Real-Time)]` so users know the data source and can click it to view the raw JSON dump in the frontend modal.

### 3. Key Challenges Solved
- **Ticker Extraction Bug:** Initially, the LLM passed entire sentences (e.g., "What is the share price of Reliance?") to the Yahoo API instead of just the ticker. We added an auto-filter in `stock_tool.py` to extract the correct company name.
- **Guardrail Conflict:** The strict Tax Expert prompt in `generator_node` was overriding the stock data and refusing to answer ("My data feed is restricted to policy documentation"). We fixed this by dynamically switching the system prompt when `is_stock_search` is True.
- **WhatsApp Formatting:** Ensure WhatsApp Webhook compatibility. Added logic so the LLM outputs Bullet Points instead of Markdown Tables for WhatsApp clients, ensuring readability on mobile.

### 4. How to Test
You can test this flow at any time by asking:
- *"What is the market cap and 52-week high for Tata Motors?"*
- *"What is the share price of Reliance?"*

### 5. Benefits of this Implementation
- **Cost Efficiency:** Bypasses expensive Pinecone queries and Cohere Reranker API calls for simple stock queries.
- **Latency Reduction:** Direct API call to Yahoo Finance is significantly faster than standard RAG retrieval.
- **Zero Cost:** The `yfinance` library is 100% free and requires no API keys.

---
*Created by Ambuj's Agentic Assistant*
