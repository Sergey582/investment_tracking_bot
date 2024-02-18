from typing import List, Dict

import requests


class BinanceClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_available_tickers(self):
        url = self.api_url + "/api/v3/exchangeInfo"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for error status codes
        data = response.json()
        usdt_symbols = [symbol['symbol'] for symbol in data['symbols'] if symbol['symbol'].endswith("USDT")]
        return usdt_symbols

    def get_daily_pnl(self, assets_names: List[str]):
        usdt_symbols = self.get_available_tickers()
        filtered_assets_names = [symbol for symbol in assets_names if f"{symbol}USDT" in usdt_symbols]
        if not filtered_assets_names:
            return []
        url = self.api_url + "/api/v3/ticker/tradingDay?symbols=["
        for symbol in filtered_assets_names:
            url += f"\"{symbol}USDT\","
        url = url[:-1] + "]"
        response = requests.get(url)
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
        usdt_symbols = self.get_available_tickers()
        filtered_assets_names = [symbol for symbol in assets_names if f"{symbol}USDT" in usdt_symbols]
        if not filtered_assets_names:
            return []
        url = self.api_url + "/api/v3/ticker/price?symbols=["
        for symbol in filtered_assets_names:
            url += f"\"{symbol}USDT\","
        url = url[:-1] + "]"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for error status codes

        data = response.json()

        # Filter symbols ending with USDT
        assets_prices = {symbol['symbol']: float(symbol['price']) for symbol in data}
        return assets_prices


binance_client = BinanceClient(
    api_url='https://api.binance.com'
)
# binance_client.get_daily_pnl(["BTC", 'LTC'])
