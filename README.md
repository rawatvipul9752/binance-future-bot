# Binance Futures Trading Bot 🚀

A simple Python bot to place BUY/SELL orders on Binance USDT-M Futures Testnet using `python-binance`.

---

## ✅ Features

- Connects to Binance Futures Testnet
- Supports `MARKET` and `LIMIT` orders
- BUY/SELL sides supported
- Command-line interface for input
- Secure API key handling using `.env`
- Clean Object-Oriented Design (`BasicBot` class)
- Logs all activity to `bot.log`

---

## ⚙️ Setup Instructions

### 1. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate

##2. Install Dependencies
ash

pip install python-binance python-dotenv

### 3. Create Your .env File
Create a file named .env in the same folder as bot.py and write:

env

API_KEY=your_binance_api_key
API_SECRET=your_binance_api_secret

### 4. Run the Bot
bash
python bot.py

The bot will:

Show your USDT balance

Ask for order details

Place the order

Log everything in bot.log

🧾 Logging
All logs are saved in bot.log, including:

API connection status

Order placement results

Errors or exceptions