import os
import logging
from dotenv import load_dotenv
from binance.um_futures import UMFutures
from binance.lib.utils import get_timestamp

# Load API keys from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Setup logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret):
        self.client = UMFutures(
            key=api_key,
            secret=api_secret,
            base_url="https://testnet.binancefuture.com"
        )

    def show_balance(self):
        try:
            account = self.client.account()
            print("✅ Connected to Binance Futures Testnet.")
            logging.info("Connected to Binance Futures Testnet.")
            print("Your Futures Balances:")
            for asset in account['assets']:
                if float(asset['walletBalance']) > 0:
                    print(f"{asset['asset']}: {asset['walletBalance']}")
                    logging.info(f"{asset['asset']}: {asset['walletBalance']}")
        except Exception as e:
            print("❌ Error connecting to Binance:", e)
            logging.error(f"Error connecting to Binance: {e}")

    def get_order_input(self):
        while True:
            order_type = input("Enter order type (MARKET or LIMIT): ").upper()
            if order_type in ["MARKET", "LIMIT"]:
                break
            print("Invalid order type. Please enter 'MARKET' or 'LIMIT'.")
            logging.warning("Invalid order type entered.")

        while True:
            side = input("Enter order side (BUY or SELL): ").upper()
            if side in ["BUY", "SELL"]:
                break
            print("Invalid order side. Please enter 'BUY' or 'SELL'.")
            logging.warning("Invalid order side entered.")

        while True:
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            try:
                info = self.client.exchange_info()
                symbols = [s['symbol'] for s in info['symbols'] if s['status'] == 'TRADING']
                if symbol in symbols:
                    break
                print("❌ Invalid symbol. Please enter a valid trading pair.")
                logging.warning(f"Invalid trading symbol entered: {symbol}")
            except Exception as e:
                print("❌ Failed to fetch exchange info:", e)
                logging.error(f"Exchange info fetch error: {e}")

        while True:
            try:
                quantity = float(input("Enter quantity: "))
                if quantity > 0:
                    break
                print("❌ Quantity must be greater than 0.")
            except ValueError:
                print("❌ Enter a valid number.")
                logging.warning("Invalid quantity entered.")

        price = None
        timeInForce = None

        if order_type == "LIMIT":
            while True:
                try:
                    price = float(input("Enter price: "))
                    if price > 0:
                        break
                    print("❌ Price must be greater than 0.")
                except ValueError:
                    print("❌ Enter a valid number.")
                    logging.warning("Invalid price entered.")

            while True:
                timeInForce = input("Enter time in force (GTC, IOC, FOK): ").upper()
                if timeInForce in ["GTC", "IOC", "FOK"]:
                    break
                print("❌ Invalid time in force.")
                logging.warning("Invalid time in force entered.")

        order = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "recvWindow": 5000,
        }

        if order_type == "LIMIT":
            order["price"] = price
            order["timeInForce"] = timeInForce

        return order

    def place_order(self, order):
        print("\n✅ Please confirm your order:")
        for k, v in order.items():
            print(f"{k}: {v}")
        confirm = input("Do you want to place this order? (yes/no): ").lower()
        if confirm != "yes":
            print("❌ Order cancelled by user.")
            logging.info("Order cancelled by user.")
            return

        try:
            order["timestamp"] = get_timestamp()
            response = self.client.new_order(**order)
            print("✅ Order placed successfully!")
            print("Response:", response)
            logging.info(f"Order placed: {response}")
        except Exception as e:
            print("❌ Failed to place order:", e)
            logging.error(f"Order placement failed: {e}")

# 🚀 Run the bot
if __name__ == "__main__":
    bot = BasicBot(API_KEY, API_SECRET)
    bot.show_balance()
    order = bot.get_order_input()
    bot.place_order(order)
