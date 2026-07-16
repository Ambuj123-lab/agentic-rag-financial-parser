import logging
import requests
import yfinance as yf
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def get_stock_price(ticker: str) -> str:
    """Fetches real-time stock data from Yahoo Finance for the given ticker symbol.

    Use this tool when the user asks about live stock prices, market cap, P/E ratio,
    52-week range, or sector information for any publicly listed company.

    Args:
        ticker: The Yahoo Finance ticker symbol. For Indian stocks append .NS
                (e.g. HDFCBANK.NS, TCS.NS, RELIANCE.NS). For US stocks use
                standard tickers (e.g. AAPL, MSFT). For Nifty 50 use ^NSEI,
                for Sensex use ^BSESN.
    """
    try:
        ticker = ticker.strip().upper()
        logger.info(f"📈 [Tool Call] Fetching live stock data for: {ticker}")

        # Use a custom session with a browser-like User-Agent to bypass Yahoo Finance rate limits on Render
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        stock = yf.Ticker(ticker, session=session)
        info = stock.info

        if not info or "regularMarketPrice" not in info and "currentPrice" not in info:
            # Fallback: try fetching latest close from history
            hist = stock.history(period="1d")
            if hist.empty:
                return f"Could not fetch real-time data for ticker '{ticker}'. Please verify the stock symbol."
            current_price = hist['Close'].iloc[-1]
            return f"Stock Data for {ticker}:\n- Current Price: ₹{current_price:.2f} (Estimated from latest close)"

        # Extract key metrics
        current_price = info.get("currentPrice") or info.get("regularMarketPrice") or "N/A"
        currency = info.get("currency", "INR")

        # Currency symbol
        curr_sym = "₹" if currency == "INR" else "$" if currency == "USD" else currency + " "

        day_high = info.get("dayHigh", "N/A")
        day_low = info.get("dayLow", "N/A")
        wk52_high = info.get("fiftyTwoWeekHigh", "N/A")
        wk52_low = info.get("fiftyTwoWeekLow", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        sector = info.get("sector", "N/A")

        # Format Market Cap
        if isinstance(market_cap, (int, float)):
            if market_cap >= 1_000_000_000_000:
                mc_str = f"{curr_sym}{market_cap / 1_000_000_000_000:.2f} Trillion"
            elif market_cap >= 1_000_000_000:
                mc_str = f"{curr_sym}{market_cap / 1_000_000_000:.2f} Billion"
            else:
                mc_str = f"{curr_sym}{market_cap:,.2f}"
        else:
            mc_str = str(market_cap)

        summary = (
            f"LIVE STOCK DATA FOR: {info.get('longName', ticker)} ({ticker})\n"
            f"Sector: {sector}\n"
            f"Current Price: {curr_sym}{current_price}\n"
            f"Today's Range: {curr_sym}{day_low} - {curr_sym}{day_high}\n"
            f"52-Week Range: {curr_sym}{wk52_low} - {curr_sym}{wk52_high}\n"
            f"Market Capitalization: {mc_str}\n"
            f"P/E Ratio: {pe_ratio}\n"
            f"(Data fetched real-time via LLM Tool Call → yfinance)"
        )

        return summary

    except Exception as e:
        logger.error(f"❌ Stock Tool failed for {ticker}: {e}")
        return f"Failed to fetch live stock data for '{ticker}'. The market API might be temporarily unavailable."
