from Api.Api_Vantage_Client import AlphaVantageClient
from ETL.FinanceETL import FinanceETL
from Analysis.FinanceAnalysis import FinanceAnalysis
client = AlphaVantageClient(api_key="YOUR_API_KEY")
etl = FinanceETL()
analysis = FinanceAnalysis()

raw = client.get_stock_data("AAPL")
df = etl.transform_daily(raw)
df = analysis.full_analysis(df)

print(df.tail())