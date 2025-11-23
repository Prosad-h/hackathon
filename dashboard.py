import streamlit as st
import pandas as pd

from Api.Api_Vantage_Client import AlphaVantageClient
from ETL.FinanceETL import FinanceETL
from Analysis.FinanceAnalysis import FinanceAnalysis

st.set_page_config(page_title="Finance ETL Dashboard", layout="wide")

st.title("📈 Finance Data ETL & Analysis Dashboard")

# SIDEBAR INPUTS
st.sidebar.header("Settings")

api_key = st.sidebar.text_input("Alpha Vantage API Key", type="password")

symbol = st.sidebar.text_input("Stock Symbol", "AAPL").upper()


run_button = st.sidebar.button("Fetch & Analyze")

# MAIN LOGIC
if run_button:
    if not api_key:
        st.error("Please enter your API key.")
        st.stop()

    client = AlphaVantageClient(api_key)
    etl = FinanceETL()
    analysis = FinanceAnalysis()

    try:
        raw = client.get_stock_data(symbol)
        df = etl.transform_daily(raw)
        df = analysis.full_analysis(df)

        # FILTER DATE RANGE
  

        st.subheader(f"📊 Showing Data for: {symbol}")
        st.dataframe(df.tail(10))

        # PLOTS
        st.subheader("Stock Price")
        st.line_chart(df["close"])

        st.subheader("20-Day Moving Average")
        st.line_chart(df["ma_20"])

        st.subheader("Daily Returns")
        st.line_chart(df["returns"])

        st.subheader("Volume")
        st.bar_chart(df["volume"])

    except Exception as e:
        st.error(f"Error: {e}")
