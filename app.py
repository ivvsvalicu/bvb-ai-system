import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BVB Portfolio System", layout="wide")

st.title("📊 BVB Portfolio Analyzer v2")

# -----------------------
# SELECT STOCKS
# -----------------------
stocks = ["TLV.BX", "SNP.BX", "BRD.BX", "SNG.BX"]

data = {}

for s in stocks:
    df = yf.download(s, period="1y")
    df["return"] = df["Close"].pct_change()
    data[s] = df

# -----------------------
# PERFORMANCE TABLE
# -----------------------
results = []

for s, df in data.items():
    total_return = (df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1
    volatility = df["return"].std()

    results.append({
        "Stock": s,
        "Return (%)": total_return * 100,
        "Volatility (%)": volatility * 100
    })

res_df = pd.DataFrame(results)

st.subheader("📊 Comparatie actiuni")

st.dataframe(res_df)

fig = px.bar(res_df, x="Stock", y="Return (%)", title="Randamente 1 an")
st.plotly_chart(fig, use_container_width=True)

# -----------------------
# PORTOFOLIO SIMULATION
# -----------------------
st.subheader("💰 Portofoliu simulat")

investment = st.slider("Investitie totala (€)", 1000, 100000, 10000)

weights = {s: 1/len(stocks) for s in stocks}

portfolio_values = []

for s, df in data.items():
    start = df["Close"].iloc[0]
    end = df["Close"].iloc[-1]

    growth = end / start

    value = investment * weights[s] * growth
    portfolio_values.append(value)

final_value = sum(portfolio_values)

st.metric("Valoare finala portofoliu", f"{final_value:.2f} €")
st.metric("Profit", f"{final_value - investment:.2f} €")

# -----------------------
# RISK VIEW
# -----------------------
st.subheader("⚖️ Risc vs Randament")

fig2 = px.scatter(
    res_df,
    x="Volatility (%)",
    y="Return (%)",
    text="Stock",
    title="Risk vs Return"
)

st.plotly_chart(fig2, use_container_width=True)
