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

    # ----------------------------------------------------
    #   CHANGED: Interval support added here
    # ----------------------------------------------------
    def _fetch_from_api(self, symbol, interval):
        symbol = symbol.upper()

        # Interval → API function mapping
        interval_map = {
            "1min": ("TIME_SERIES_INTRADAY", "1min"),
            "5min": ("TIME_SERIES_INTRADAY", "5min"),
            "15min": ("TIME_SERIES_INTRADAY", "15min"),
            "30min": ("TIME_SERIES_INTRADAY", "30min"),
            "60min": ("TIME_SERIES_INTRADAY", "60min"),

            "daily": ("TIME_SERIES_DAILY", None),
            "weekly": ("TIME_SERIES_WEEKLY", None),
            "monthly": ("TIME_SERIES_MONTHLY", None)
        }

        if interval not in interval_map:
            raise ValueError(f"Invalid interval: {interval}")

        function, intraday_interval = interval_map[interval]

        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key
        }

        # Only intraday requires "interval" parameter
        if intraday_interval:
            params["interval"] = intraday_interval

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise Exception("API request failed.")

        data = response.json()

        # Error handling
        if "Error Message" in data:
            raise ValueError("Invalid stock symbol!")

        if "Note" in data:
            raise RuntimeError("API limit reached. Try again later.")

        # Check data exists
        expected_keys = {
            "1min": "Time Series (1min)",
            "5min": "Time Series (5min)",
            "15min": "Time Series (15min)",
            "30min": "Time Series (30min)",
            "60min": "Time Series (60min)",
            "daily": "Time Series (Daily)",
            "weekly": "Weekly Time Series",
            "monthly": "Monthly Time Series"
        }

        if expected_keys[interval] not in data:
            raise Exception("Unexpected API response format.")

        return data

    # ----------------------------------------------------
    #       PUBLIC METHOD
    # ----------------------------------------------------
    def get_stock_data(self, symbol, interval="daily"):
        filepath = self._cache_file(symbol, interval)

        # Try cache first
        cache = self._load_cache(filepath)
        if cache:
            print("Loaded from cache.")
            return cache

        print("Fetching from API...")
        data = self._fetch_from_api(symbol, interval)

        # Save to cache
        self._save_cache(filepath, data)

        return data
