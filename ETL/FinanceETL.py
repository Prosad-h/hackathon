import pandas as pd

class FinanceETL:
    def __init__(self):
        pass

    def transform_daily(self, raw_data):
        """
        Converts Alpha Vantage 'Time Series (Daily)' JSON
        into a clean pandas DataFrame.
        """

        if "Time Series (Daily)" not in raw_data:
            raise ValueError("Invalid data format — 'Time Series (Daily)' missing.")

        daily_data = raw_data["Time Series (Daily)"]

        # Convert JSON → DataFrame
        df = pd.DataFrame.from_dict(daily_data, orient="index")

        # Fix column names
        df.columns = [
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]

        # Convert index → datetime
        df.index = pd.to_datetime(df.index)

        # Convert values to numeric
        df = df.astype(float)

        # Sort dates from oldest → newest
        df = df.sort_index()

        return df
