import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BVB Portfolio System", layout="wide")

st.title("📊 BVB Portfolio Analyzer v2 (Stable)")

# -----------------------
# STOCK LIST
# -----------------------
stocks = ["TLV.BX", "SNP.BX", "BRD.BX", "SNG.BX"]

data = {}
results = []

# -----------------------
# DOWNLOAD DATA SAFELY
# -----------------------
for s in stocks:
    try:
        df = yf.download(s, period="1y", progress=False)

        # safety checks (IMPORTANT FIX)
        if df is None or df.empty or "Close" not in df.columns or len(df) < 2:
            continue

        df["return"] = df["Close"].pct_change()

        data[s] = df

        total_return = (df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1
        volatility = df["return"].std()

        results.append({
            "Stock": s,
            "Return (%)": total_return * 100,
            "Volatility (%)": volatility * 100
        })

    except Exception as e:
        st.warning(f"Nu s-au putut încărca date pentru {s}")
        continue

# -----------------------
# HANDLE EMPTY CASE
# -----------------------
if len(results) == 0:
    st.error("Nu s-au putut încărca date pentru niciun simbol.")
    st.stop()

res_df = pd.DataFrame(results)

# -----------------------
# DISPLAY TABLE
# -----------------------
st.subheader("📊 Comparație acțiuni BVB")

st.dataframe(res_df)

# -----------------------
# RETURN CHART
# -----------------------
fig = px.bar(
    res_df,
    x="Stock",
    y="Return (%)",
    title="Randamente 1 an"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# PORTFOLIO SIMULATION
# -----------------------
st.subheader("💰 Portofoliu simulat")

investment = st.slider("Investiție totală (€)", 1000, 100000, 10000)

weights = {s: 1/len(results) for s in res_df["Stock"]}

final_value = 0

for r in results:
    stock = r["Stock"]
    growth = (r["Return (%)"] / 100) + 1

    final_value += investment * weights[stock] * growth

st.metric("Valoare finală portofoliu", f"{final_value:.2f} €")
st.metric("Profit", f"{final_value - investment:.2f} €")

# -----------------------
# RISK vs RETURN
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
