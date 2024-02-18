import hashlib
import hmac
import time
from typing import Dict, List

import requests

from app.core.config import BINANCE_API_KEY, BINANCE_API_SECRET


class BinanceClient:
    def __init__(self, api_url: str, api_key: str, api_secret: str):
        self.api_url = api_url
        self.api_key = api_key
        self.api_secret = api_secret

    def get_auth_headers(self):
        timestamp = int(round(time.time() * 1000))
        query_string = f"timestamp={timestamp}"
        signature = hmac.new(
            self.api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        headers = {
            "X-MBX-APIKEY": self.api_key,
            "X-MBX-TIMESTAMP": str(timestamp),
            "X-MBX-SIGNATURE": signature,
        }
        return headers

    def get_available_tickers(self):
        headers = self.get_auth_headers()
        url = self.api_url + "/api/v3/exchangeInfo"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for error status codes
        data = response.json()
        usdt_symbols = [symbol['symbol'] for symbol in data['symbols'] if symbol['symbol'].endswith("USDT")]
        return usdt_symbols

    def get_daily_pnl(self, assets_names: List[str]):
        headers = self.get_auth_headers()
        usdt_symbols = self.get_available_tickers()
        filtered_assets_names = [symbol for symbol in assets_names if f"{symbol}USDT" in usdt_symbols]
        if not filtered_assets_names:
            return []
        url = self.api_url + "/api/v3/ticker/tradingDay?symbols=["
        for symbol in filtered_assets_names:
            url += f"\"{symbol}USDT\","
        url = url[:-1] + "]"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for error status codes
        data = response.json()

        usdt_symbols = {}
        for symbol in data:
            usdt_symbols[symbol['symbol']] = {
                'price_change': float(symbol['priceChange']),
                'price_change_percent': float(symbol['priceChangePercent']),
            }
        return usdt_symbols

    def get_assets_prices(self, assets_names: List[str]) -> Dict[str, int]:
        headers = self.get_auth_headers()
        usdt_symbols = self.get_available_tickers()
        filtered_assets_names = [symbol for symbol in assets_names if f"{symbol}USDT" in usdt_symbols]
        if not filtered_assets_names:
            return []
        url = self.api_url + "/api/v3/ticker/price?symbols=["
        for symbol in filtered_assets_names:
            url += f"\"{symbol}USDT\","
        url = url[:-1] + "]"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for error status codes

        data = response.json()

        # Filter symbols ending with USDT
        assets_prices = {symbol['symbol']: float(symbol['price']) for symbol in data}
        return assets_prices


binance_client = BinanceClient(
    api_url='https://api.binance.com',
    api_key=BINANCE_API_KEY,
    api_secret=BINANCE_API_SECRET,

)
# a = binance_client.get_daily_pnl(["BTC", 'LTC'])
# print(a)
