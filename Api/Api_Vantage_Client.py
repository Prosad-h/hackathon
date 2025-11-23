import requests
import os
import json
from datetime import datetime, timedelta

class AlphaVantageClient:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key, cache_path="../cache"):
        self.api_key = api_key
        self.cache_path = cache_path
        os.makedirs(cache_path, exist_ok=True)

    def _cache_file(self, symbol, interval):
        return os.path.join(self.cache_path, f"{symbol}_{interval}.json")

    def _load_cache(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
        return None

    def _save_cache(self, filepath, data):
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def _fetch_from_api(self, symbol, interval):
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol.upper(),
            "apikey": self.api_key
        }

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise Exception("API request failed.")

        data = response.json()

        # Error handling
        if "Error Message" in data:
            raise ValueError("Invalid stock symbol!")
        if "Note" in data:
            raise RuntimeError("API limit reached. Try again later.")
        if "Time Series (Daily)" not in data:
            raise Exception("Unexpected API response format.")

        return data

    def get_stock_data(self, symbol, interval="daily"):
        filepath = self._cache_file(symbol, interval)

        # Try cache first
        cache = self._load_cache(filepath)
        if cache:
            print("Loaded from cache.")
            return cache

        # Otherwise fetch from API
        print("Fetching from API...")
        data = self._fetch_from_api(symbol, interval)

        # Save to cache
        self._save_cache(filepath, data)

        return data
