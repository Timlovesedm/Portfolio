import streamlit as st
import pandas as pd
import plotly.express as px

# --- ページ設定 ---
st.set_page_config(page_title="有名ポートフォリオ閲覧アプリ", layout="wide")

st.title("📊 有名投資家・投資信託のポートフォリオ構成")

# --- データ読み込み ---
@st.cache_data
def load_data():
    return pd.read_csv("portfolio_data.csv")

df = load_data()

# --- 投資家 or ファンド選択 ---
investors = df["investor"].unique()
selected_investor = st.selectbox("👤 投資家を選択してください", investors)

# --- データ抽出 ---
df_selected = df[df["investor"] == selected_investor]

st.subheader(f"{selected_investor} のポートフォリオ構成")

# --- 表示（テーブル） ---
st.dataframe(df_selected[["ticker", "company", "weight"]].reset_index(drop=True), use_container_width=True)

# --- 表示（円グラフ） ---
fig = px.pie(df_selected, names="company", values="weight", title="保有比率（円グラフ）")
st.plotly_chart(fig, use_container_width=True)
