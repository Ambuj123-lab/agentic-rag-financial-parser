import logging
import requests
from langchain_core.tools import tool
from app.core.config import settings

logger = logging.getLogger(__name__)

@tool
def get_stock_price(ticker: str) -> str:
    """Fetches real-time stock data for the given ticker symbol.

    Use this tool when the user asks about live stock prices, market cap, P/E ratio,
    52-week range, EPS, or trading volume for any publicly listed company.

    Args:
        ticker: The Yahoo Finance ticker symbol. For Indian stocks append .NS
                (e.g. HDFCBANK.NS, TCS.NS, ZOMATO.NS). For US stocks use
                standard tickers (e.g. AAPL, MSFT). For Nifty 50 use ^NSEI. For Sensex use ^BSESN.
    """
    try:
        ticker = ticker.strip().upper()
        logger.info(f"📈 [Tool Call] Fetching live stock data for: {ticker} via RapidAPI Yahoo Finance")
        
        if not hasattr(settings, 'RAPIDAPI_KEY') or not settings.RAPIDAPI_KEY:
             return "API Key Error: RAPIDAPI_KEY is missing in the configuration."

        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"
        querystring = {"region": "IN", "symbols": ticker}
        headers = {
            "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
            "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        
        if response.status_code != 200:
             return f"Failed to fetch data for '{ticker}'. API returned status code {response.status_code}."
             
        data = response.json()
        results = data.get("quoteResponse", {}).get("result", [])
        
        if not results:
             return f"Could not find real-time data for ticker '{ticker}'. Please verify the stock symbol."
             
        price_data = results[0]
        
        name = price_data.get("longName") or price_data.get("shortName") or ticker
        current_price = price_data.get("regularMarketPrice", "N/A")
        exchange = price_data.get("fullExchangeName", "Unknown")
        curr_sym = price_data.get("currency", "INR")
        
        day_high = price_data.get("regularMarketDayHigh", "N/A")
        day_low = price_data.get("regularMarketDayLow", "N/A")
        
        wk52_high = price_data.get("fiftyTwoWeekHigh", "N/A")
        wk52_low = price_data.get("fiftyTwoWeekLow", "N/A")
        
        market_cap = price_data.get("marketCap", "N/A")
        pe_ratio = price_data.get("trailingPE", "N/A")
        
        raw_vol = price_data.get("regularMarketVolume", "N/A")
        try:
            volume = f"{int(raw_vol):,}"
        except (ValueError, TypeError):
            volume = str(raw_vol)

        # Format Currency Symbol Display
        disp_sym = "₹" if curr_sym == "INR" else "$"

        # Format Market Cap
        if isinstance(market_cap, (int, float)) and market_cap > 0:
            if market_cap >= 1_000_000_000_000:
                mc_str = f"{disp_sym}{market_cap / 1_000_000_000_000:.2f} Trillion"
            elif market_cap >= 1_000_000_000:
                mc_str = f"{disp_sym}{market_cap / 1_000_000_000:.2f} Billion"
            else:
                mc_str = f"{disp_sym}{market_cap:,.2f}"
        else:
            mc_str = str(market_cap)
            
        # Format P/E
        if isinstance(pe_ratio, (int, float)):
            pe_ratio = f"{pe_ratio:.2f}"

        summary = (
            f"LIVE STOCK DATA FOR: {name} ({ticker})\n"
            f"Exchange: {exchange}\n"
            f"Current Price: {disp_sym}{current_price}\n"
            f"Today's Range: {disp_sym}{day_low} - {disp_sym}{day_high}\n"
            f"52-Week Range: {disp_sym}{wk52_low} - {disp_sym}{wk52_high}\n"
            f"Market Capitalization: {mc_str}\n"
            f"P/E Ratio: {pe_ratio}\n"
            f"Volume: {volume}\n"
            f"(Data fetched real-time via RapidAPI)"
        )

        return summary

    except Exception as e:
        logger.error(f"❌ Stock Tool failed for {ticker}: {e}")
        return f"Failed to fetch live stock data for '{ticker}'. An unexpected error occurred."
