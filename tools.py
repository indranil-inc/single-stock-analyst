import yfinance as yf
from crewai.tools import BaseTool

class SimplePriceTool(BaseTool):
    name: str = "get_price"
    description: str = "Get the current market price for a stock ticker."

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info.last_price
            return f"The current market price of {ticker} is INR {price:.2f}"
        except Exception:
            return f"Price data unavailable for {ticker}. Ensure the ticker is correct."

class SimpleNewsTool(BaseTool):
    name: str = "get_news"
    description: str = "Get the 2 most recent news headlines for a stock."

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            if not news:
                return f"No recent news found for {ticker}."
            
            # Extract only the first 2 headlines to keep the 'brain' fast
            headlines = []
            for item in news[:2]:
                title = item.get('title', 'Market Update')
                headlines.append(f"- {title}")
            
            return "\n".join(headlines)
        except Exception:
            return "News feed is currently busy. Focus on price data instead."
