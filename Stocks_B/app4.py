import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

# --- アプリ設定 ---
st.set_page_config(layout="wide", page_title="ポートフォリオ分析アプリ")

# --- データ読み込み ---
@st.cache_data
def load_data():
    return pd.read_csv("portfolio_data.csv")

df = load_data()

# --- 投資家の選択 ---
investors = df["name"].unique()
selected_investor = st.selectbox("投資家を選択してください", investors)

# --- 選ばれた投資家のポートフォリオを抽出 ---
portfolio = df[df["name"] == selected_investor].copy()
tickers = portfolio["ticker"].tolist()
weights = portfolio["weight"].values

# --- 株価データの取得 ---
start_date = datetime.today() - timedelta(days=365 * 3)
end_date = datetime.today()

price_data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
price_data = price_data.dropna()

# --- 日次リターンの計算 ---
daily_returns = price_data.pct_change().dropna()

# --- ポートフォリオのリターン ---
portfolio_returns = daily_returns.dot(weights)

# --- パフォーマンス指標の計算 ---
cumulative_return = (1 + portfolio_returns).cumprod()
annual_return = portfolio_returns.mean() * 252
volatility = portfolio_returns.std() * np.sqrt(252)
risk_free_rate = 0.01  # 仮の無リスク金利
sharpe_ratio = (annual_return - risk_free_rate) / volatility

# --- 結果の表示 ---
st.header(f"{selected_investor} のポートフォリオ分析")

st.subheader("ポートフォリオ構成")
st.dataframe(portfolio.reset_index(drop=True))

st.subheader("パフォーマンス指標")
col1, col2, col3 = st.columns(3)
col1.metric("年間リターン", f"{annual_return:.2%}")
col2.metric("リスク (年率)", f"{volatility:.2%}")
col3.metric("シャープレシオ", f"{sharpe_ratio:.2f}")

# --- チャート表示 ---
st.subheader("ポートフォリオ価値の推移")
st.line_chart(cumulative_return)

