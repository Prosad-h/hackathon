import pandas as pd 
class FinanceAnalysis:
    def __init__(self):
        pass
    def add_returns(self,df:pd.DataFrame):
        df["returns"] = df["close"].pct_change()
        return df
    def add_moving_average(self,df:pd.DataFrame,input=20):
        df[f"ma_{input}"] = df["close"].rolling(window=input).mean()
        return df
    def add_volatility(self, df:pd.DataFrame, input=20):
        df["volatility"] = df["returns"].rolling(window=input).std() * (252 ** 0.5)
        return df
    def full_analysis(self, df:pd.DataFrame):
        df = self.add_returns(df)
        df = self.add_moving_average(df, input=20)
        df = self.add_volatility(df,input=20)
        return df 