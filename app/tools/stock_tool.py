import logging
from langchain_core.tools import tool
from yahooquery import Ticker

logger = logging.getLogger(__name__)

@tool
def get_stock_price(ticker: str) -> str:
    """Fetches real-time stock data for the given ticker symbol.

    Use this tool when the user asks about live stock prices, market cap, P/E ratio,
    52-week range, EPS, or trading volume for any publicly listed company.

    Args:
        ticker: The Yahoo Finance ticker symbol. For Indian stocks append .NS
                (e.g. HDFCBANK.NS, TCS.NS, RELIANCE.NS). For US stocks use
                standard tickers (e.g. AAPL, MSFT). For Nifty 50 use ^NSEI.
    """
    try:
        ticker = ticker.strip().upper()
        logger.info(f"📈 [Tool Call] Fetching live stock data for: {ticker} via yahooquery")
        
        stock = Ticker(ticker)
        price_dict = stock.price
        summary_dict = stock.summary_detail
        
        # yahooquery returns a dict with the ticker as the key, or an error string
        if isinstance(price_dict, str) or ticker not in price_dict or isinstance(price_dict[ticker], str):
             return f"Could not find real-time data for ticker '{ticker}'. Please verify the stock symbol."
             
        price_data = price_dict[ticker]
        summary_data = summary_dict.get(ticker, {}) if isinstance(summary_dict, dict) else {}
        
        name = price_data.get("longName") or price_data.get("shortName") or ticker
        current_price = price_data.get("regularMarketPrice", "N/A")
        exchange = price_data.get("exchangeName", "Unknown")
        curr_sym = price_data.get("currencySymbol", "₹")
        
        day_high = price_data.get("regularMarketDayHigh", "N/A")
        day_low = price_data.get("regularMarketDayLow", "N/A")
        
        wk52_high = summary_data.get("fiftyTwoWeekHigh", "N/A")
        wk52_low = summary_data.get("fiftyTwoWeekLow", "N/A")
        
        market_cap = price_data.get("marketCap") or summary_data.get("marketCap", "N/A")
        pe_ratio = summary_data.get("trailingPE", "N/A")
        volume = price_data.get("regularMarketVolume", "N/A")

        # Format Market Cap
        if isinstance(market_cap, (int, float)) and market_cap > 0:
            if market_cap >= 1_000_000_000_000:
                mc_str = f"{curr_sym}{market_cap / 1_000_000_000_000:.2f} Trillion"
            elif market_cap >= 1_000_000_000:
                mc_str = f"{curr_sym}{market_cap / 1_000_000_000:.2f} Billion"
            else:
                mc_str = f"{curr_sym}{market_cap:,.2f}"
        else:
            mc_str = str(market_cap)
            
        # Format P/E
        if isinstance(pe_ratio, (int, float)):
            pe_ratio = f"{pe_ratio:.2f}"

        summary = (
            f"LIVE STOCK DATA FOR: {name} ({ticker})\n"
            f"Exchange: {exchange}\n"
            f"Current Price: {curr_sym}{current_price}\n"
            f"Today's Range: {curr_sym}{day_low} - {curr_sym}{day_high}\n"
            f"52-Week Range: {curr_sym}{wk52_low} - {curr_sym}{wk52_high}\n"
            f"Market Capitalization: {mc_str}\n"
            f"P/E Ratio: {pe_ratio}\n"
            f"Volume: {volume:,}\n"
            f"(Data fetched real-time via LLM Tool Call)"
        )

        return summary

    except Exception as e:
        logger.error(f"❌ Stock Tool failed for {ticker}: {e}")
        return f"Failed to fetch live stock data for '{ticker}'. An unexpected error occurred."
