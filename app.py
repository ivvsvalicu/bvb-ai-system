import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="BVB Safe Engine", layout="wide")

st.title("📊 BVB Safe Data Engine (Stable Version)")

# -----------------------
# SIMBOLURI
# -----------------------
symbols = ["TLV", "SNP", "BRD", "SNG"]
symbol = st.selectbox("Alege simbol BVB", symbols)

# -----------------------
# MOCK + SAFE DATA (temporar stabil)
# -----------------------
np.random.seed(42)

days = pd.date_range(end=pd.Timestamp.today(), periods=250)

price = np.cumsum(np.random.randn(len(days))) + 100

df = pd.DataFrame({
    "Date": days,
    "Close": price
})

df["return"] = df["Close"].pct_change()

# -----------------------
# DISPLAY
# -----------------------
st.subheader(f"📊 Evoluție simulată pentru {symbol}")

fig = px.line(df, x="Date", y="Close", title=f"{symbol} - price evolution")
st.plotly_chart(fig, use_container_width=True)

# -----------------------
# STATS
# -----------------------
st.subheader("📈 Statistici")

col1, col2, col3 = st.columns(3)

col1.metric("Ultimul preț", round(df["Close"].iloc[-1], 2))
col2.metric("Randament mediu", f"{df['return'].mean()*100:.2f}%")
col3.metric("Volatilitate", f"{df['return'].std()*100:.2f}%")

# -----------------------
# WARNING
# -----------------------
st.info("⚠️ Datele sunt temporar simulate. Următorul pas: conectare la API BVB real (XHR).")
