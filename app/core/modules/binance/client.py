from typing import List, Dict

import requests


class BinanceClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_assets_prices(self, assets_names: List[str]) -> Dict[str, int]:
        url = self.api_url + "/api/v3/exchangeInfo"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for error status codes

        data = response.json()

        # Filter symbols ending with USDT
        usdt_symbols = {
            symbol['baseAsset']: symbol[''] for symbol in data['symbols']
            if symbol['symbol'].endswith("USDT")
        }
        result = []
        for name in assets_names:
            result.append(name)


binance_client = BinanceClient(
    api_url='https://api.binance.com'
)
