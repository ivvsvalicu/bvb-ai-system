import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px

st.set_page_config(page_title="BVB Native Engine v1", layout="wide")

st.title("📊 BVB Native Data Engine v1")

# -------------------------
# SIMBOLURI BVB (simplu start)
# -------------------------
symbols = ["TLV", "SNP", "BRD", "SNG"]

symbol = st.selectbox("Alege simbol BVB", symbols)

# -------------------------
# FUNCTIE SCRAPING BVB
# -------------------------
def get_bvb_data(symbol):
    url = "https://www.bvb.ro/TradingAndStatistics/Trading/HistoricalTradingInfo"

    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")

    tables = pd.read_html(r.text)

    # caută tabelul care conține simbolul
    for t in tables:
        if t.astype(str).apply(lambda x: x.str.contains(symbol)).any().any():
            return t

    return None

# -------------------------
# LOAD DATA
# -------------------------
df = get_bvb_data(symbol)

if df is None:
    st.error("Nu s-au găsit date pentru simbol (BVB HTML limitat).")
    st.stop()

st.subheader(f"📊 Date pentru {symbol}")
st.dataframe(df)

# -------------------------
# CLEAN (best effort)
# -------------------------
try:
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) > 0:
        col = numeric_cols[0]

        st.subheader("📈 Evoluție (aproximativ)")

        fig = px.line(df, y=col, title=f"Indicator {symbol}")
        st.plotly_chart(fig, use_container_width=True)

except:
    st.warning("Nu s-a putut construi graficul din datele BVB")
