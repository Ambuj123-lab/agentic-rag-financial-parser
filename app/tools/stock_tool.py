import logging
import yfinance as yf

logger = logging.getLogger(__name__)

def fetch_stock_data(ticker_symbol: str) -> str:
    """
    Fetches real-time stock data for a given ticker symbol using yfinance.
    Returns a formatted string containing key financial metrics.
    """
    try:
        # Most Indian users will be querying Indian stocks. If no suffix is provided and it's not a known US ticker,
        # we append .NS to default to National Stock Exchange (NSE).
        # If the LLM passed a full sentence, try to extract the company name.
        # Simple heuristic: remove common stopwords and pick the last/most prominent word.
        # Or even simpler, just ask the LLM to provide ONLY the ticker, but as a fallback here:
        

        original_ticker = ticker_symbol.upper().strip()
                
        # A simple heuristic: if it doesn't have a dot and is not a major US index/stock, assume NSE.
        # (The LLM should ideally extract with .NS, but this is a safety net).
        if "." not in original_ticker and original_ticker not in ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META"]:
            ticker_symbol = f"{original_ticker}.NS"
        else:
            ticker_symbol = original_ticker
            
        logger.info(f"📈 Fetching live stock data for: {ticker_symbol}")
        
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        if not info or "regularMarketPrice" not in info and "currentPrice" not in info:
            # Fallback if standard info fails (sometimes yfinance is finicky with certain tickers)
            hist = stock.history(period="1d")
            if hist.empty:
                return f"Could not fetch real-time data for ticker '{ticker_symbol}'. Please verify the stock symbol."
            current_price = hist['Close'].iloc[-1]
            return f"Stock Data for {ticker_symbol}:\n- Current Price: ₹{current_price:.2f} (Estimated from latest close)"

        # Extract useful metrics
        current_price = info.get("currentPrice") or info.get("regularMarketPrice") or "N/A"
        currency = info.get("currency", "INR")
        
        # Determine currency symbol
        curr_sym = "₹" if currency == "INR" else "$" if currency == "USD" else currency + " "
        
        day_high = info.get("dayHigh", "N/A")
        day_low = info.get("dayLow", "N/A")
        wk52_high = info.get("fiftyTwoWeekHigh", "N/A")
        wk52_low = info.get("fiftyTwoWeekLow", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        sector = info.get("sector", "N/A")
        
        # Format Market Cap for readability
        if isinstance(market_cap, (int, float)):
            if market_cap >= 1_000_000_000_000:
                mc_str = f"{curr_sym}{market_cap / 1_000_000_000_000:.2f} Trillion"
            elif market_cap >= 1_000_000_000:
                mc_str = f"{curr_sym}{market_cap / 1_000_000_000:.2f} Billion"
            else:
                mc_str = f"{curr_sym}{market_cap:,.2f}"
        else:
            mc_str = str(market_cap)
            
        # Build a rich textual summary to feed into the LangGraph context
        summary = (
            f"LIVE STOCK DATA FOR: {info.get('longName', ticker_symbol)} ({ticker_symbol})\n"
            f"Sector: {sector}\n"
            f"Current Price: {curr_sym}{current_price}\n"
            f"Today's Range: {curr_sym}{day_low} - {curr_sym}{day_high}\n"
            f"52-Week Range: {curr_sym}{wk52_low} - {curr_sym}{wk52_high}\n"
            f"Market Capitalization: {mc_str}\n"
            f"P/E Ratio: {pe_ratio}\n"
            f"(Data fetched real-time via yfinance Tool Call)"
        )
        
        return summary

    except Exception as e:
        logger.error(f"❌ Stock Tool failed for {ticker_symbol}: {e}")
        return f"Failed to fetch live stock data for '{ticker_symbol}'. The market API might be temporarily unavailable."
