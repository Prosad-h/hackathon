import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from Api.Api_Vantage_Client import AlphaVantageClient
from ETL.FinanceETL import FinanceETL
from Analysis.FinanceAnalysis import FinanceAnalysis

st.set_page_config(page_title="Finance ETL Dashboard", layout="wide")

st.title("📈 Finance Data ETL & Analysis Dashboard")

st.sidebar.header("Settings")

api_key = "XJ0YE7BD9GJJZ033"
symbol = st.sidebar.text_input("Stock Symbol", "AAPL").upper()
interval = st.sidebar.selectbox(
    "Select Interval",
    ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"],
    index=5
)

if not api_key:
    st.error("Please enter your API key.")
    st.stop()

client = AlphaVantageClient(api_key)
etl = FinanceETL()
analysis = FinanceAnalysis()

try:
    raw = client.get_stock_data(symbol, interval=interval)

    if interval in ["daily", "weekly", "monthly"]:
        df = etl.transform_daily(raw)
    else:
        df = etl.transform_intraday(raw, interval=interval)

    df = analysis.full_analysis(df)

    st.subheader(f"📊 Showing Data for: {symbol} ({interval})")
    st.dataframe(df.tail(10))

    latest_price = df["close"].iloc[-1]
    st.metric(label="Latest Price", value=f"${latest_price:.2f}")

    st.subheader("📉 Candlestick + Moving Average (20)")

    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            increasing_line_color="green",
            decreasing_line_color="red",
            name="Candles"
        )
    )

    if "ma_20" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["ma_20"],
                mode="lines",
                line=dict(width=2, color="blue"),
                name="MA 20"
            )
        )

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=550,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily Returns")
    st.line_chart(df["returns"])

    st.subheader("Volume")
    st.bar_chart(df["volume"])

except ValueError as ve:
    st.error("Stock not found")
except RuntimeError as re:
    st.error(str(re))
except Exception as e:
    st.error(f"An error occurred: {e}")
