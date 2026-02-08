import json
import requests
from datetime import datetime

class PortfolioTracker:
    """
    A complex Portfolio Tracker to manage Crypto and Forex assets.
    Supports real-time price fetching and profit/loss calculations.
    """

    def __init__(self, user_name):
        self.user_name = user_name
        self.assets = {}
        self.base_url = "https://api.coingecko.com/api/v3/simple/price"

    def add_asset(self, symbol, quantity, buy_price):
        """
        Adds or updates an asset in the portfolio.
        """
        self.assets[symbol.lower()] = {
            "quantity": quantity,
            "buy_price": buy_price,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"✔️ {symbol.upper()} added to {self.user_name}'s portfolio.")

    def fetch_market_price(self, symbols):
        """
        Fetches live prices using an external API.
        """
        params = {
            "ids": ",".join(symbols),
            "vs_currencies": "usd"
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def generate_report(self):
        """
        Calculates PnL (Profit and Loss) for all assets.
        """
        if not self.assets:
            return "Portfolio is empty."

        symbols = list(self.assets.keys())
        prices = self.fetch_market_price(symbols)
        
        print(f"\n--- Performance Report for {self.user_name} ---")
        total_value = 0
        
        for coin, data in self.assets.items():
            current_price = prices.get(coin, {}).get("usd", 0)
            investment = data['quantity'] * data['buy_price']
            current_value = data['quantity'] * current_price
            pnl = current_value - investment
            total_value += current_value
            
            print(f"Coin: {coin.upper()} | Price: ${current_price} | PnL: ${pnl:.2f}")
        
        print(f"Total Portfolio Value: ${total_value:.2f}\n")

# --- Execution Block ---
if __name__ == "__main__":
    tracker = PortfolioTracker("Alpha_Trader")
    
    # Adding Sample Data
    tracker.add_asset("bitcoin", 0.5, 45000)
    tracker.add_asset("ethereum", 2.0, 2500)
    
    # Generating Live Report
    tracker.generate_report()