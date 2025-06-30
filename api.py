import requests
import pandas as pd

# Binance endpoint for real-time price
BINANCE_TICKER_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_HISTORICAL_URL = "https://api.binance.com/api/v3/klines"

# Mapping your coin_id to Binance symbols
BINANCE_SYMBOLS = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "solana": "SOLUSDT",
    "dogecoin": "DOGEUSDT",
    "cardano": "ADAUSDT",
    "polygon": "MATICUSDT",
    "ripple": "XRPUSDT",
    "shiba-inu": "SHIBUSDT",
}

# Approx conversion (can be updated dynamically if needed)
USD_TO_INR = 83.0


def get_price(coin_id):
    """
    Fetch current price from Binance and convert to INR.
    """
    symbol = BINANCE_SYMBOLS.get(coin_id)
    if not symbol:
        return None
    try:
        response = requests.get(
            BINANCE_TICKER_URL, params={"symbol": symbol}, timeout=5
        )
        response.raise_for_status()
        data = response.json()
        price_usd = float(data["price"])
        return round(price_usd * USD_TO_INR, 2)
    except Exception as e:
        print(f"[ERROR] Real-time price fetch error: {e}")
        return None


def get_price_chart_data(coin_id, days=1):
    """
    Fetch historical price chart data using Binance Kline (candlestick) data.
    """
    symbol = BINANCE_SYMBOLS.get(coin_id)
    if not symbol:
        return None

    interval = "1h" if days == 1 else "1d"
    limit = min(
        days * 24 if days <= 7 else 100, 1000
    )  # Binance allows up to 1000 points

    params = {"symbol": symbol, "interval": interval, "limit": limit}

    try:
        res = requests.get(BINANCE_HISTORICAL_URL, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()

        # Each row format: [Open time, Open, High, Low, Close, Volume, ...]
        timestamps = [int(entry[0]) for entry in data]
        prices = [float(entry[4]) for entry in data]  # Close prices

        df = pd.DataFrame(
            {
                "Timestamp": pd.to_datetime(timestamps, unit="ms"),
                "Price": [round(p * USD_TO_INR, 2) for p in prices],
            }
        )
        return df
    except Exception as e:
        print(f"[ERROR] Chart data fetch error: {e}")
        return None
