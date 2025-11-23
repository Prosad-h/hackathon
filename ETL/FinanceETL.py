import pandas as pd

class FinanceETL:
    def __init__(self):
        pass

    # -----------------------------------
    # Daily / Weekly / Monthly
    # -----------------------------------
    def transform_daily(self, raw_data):
        """
        Converts Alpha Vantage 'Time Series (Daily)', 'Weekly', or 'Monthly' JSON
        into a clean pandas DataFrame.
        """
        # Detect the key automatically
        for key in ["Time Series (Daily)", "Weekly Time Series", "Monthly Time Series"]:
            if key in raw_data:
                data = raw_data[key]
                break
        else:
            raise ValueError("Invalid data format — no recognized time series found.")

        df = pd.DataFrame.from_dict(data, orient="index")

        # Fix column names
        df.columns = ["open", "high", "low", "close", "volume"][:len(df.columns)]

        # Convert index → datetime
        df.index = pd.to_datetime(df.index)

        # Convert values to numeric
        df = df.astype(float)

        # Sort dates from oldest → newest
        df = df.sort_index()

        return df

    # -----------------------------------
    # Intraday
    # -----------------------------------
    def transform_intraday(self, raw_data, interval="5min"):
        """
        Converts Alpha Vantage intraday JSON ('1min', '5min', '15min', '30min', '60min')
        into a clean pandas DataFrame.
        """
        key = f"Time Series ({interval})"
        if key not in raw_data:
            raise ValueError(f"Invalid intraday data — '{key}' missing.")

        intraday_data = raw_data[key]

        df = pd.DataFrame.from_dict(intraday_data, orient="index")

        # Fix column names
        df.columns = ["open", "high", "low", "close", "volume"]

        # Convert index → datetime
        df.index = pd.to_datetime(df.index)

        # Convert values to numeric
        df = df.astype(float)

        # Sort from oldest → newest
        df = df.sort_index()

        return df
