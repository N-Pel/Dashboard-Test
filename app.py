import time
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Live CSV Dashboard", layout="wide")

st.title("📈 Live Dashboard op basis van CSV")
st.caption("Dit dashboard leest periodiek opnieuw uit een CSV-bestand.")

DEFAULT_CSV = Path("C:\Users\Administrator\Downloads\amazon_sales_dataset.csv")

with st.sidebar:
    st.header("Instellingen")
    csv_path = st.text_input("Pad naar CSV-bestand", value=str(DEFAULT_CSV))
    refresh_sec = st.slider("Refresh interval (seconden)", min_value=2, max_value=60, value=5)

# Auto-refresh zonder externe dependency
st.markdown(
    f"""
    <script>
      setTimeout(function() {{ window.location.reload(); }}, {refresh_sec * 1000});
    </script>
    """,
    unsafe_allow_html=True,
)

@st.cache_data(ttl=1)
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

try:
    df = load_csv(csv_path)
except FileNotFoundError:
    st.error(f"CSV-bestand niet gevonden: {csv_path}")
    st.stop()
except Exception as exc:
    st.error(f"Kon CSV niet inlezen: {exc}")
    st.stop()

if df.empty:
    st.warning("CSV bevat geen rijen.")
    st.stop()

st.success(f"Laatste update: {time.strftime('%H:%M:%S')}")

# Datum/tijd-kolom detecteren
possible_time_cols = [
    c for c in df.columns if any(k in c.lower() for k in ["date", "datum", "time", "tijd", "timestamp"])
]
time_col = possible_time_cols[0] if possible_time_cols else None

if time_col:
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")

numeric_cols = df.select_dtypes(include="number").columns.tolist()

if not numeric_cols:
    st.warning("Geen numerieke kolommen gevonden voor KPI's of grafieken.")
    st.dataframe(df, use_container_width=True)
    st.stop()

st.subheader("KPI's")
cols = st.columns(min(4, len(numeric_cols)))
for i, metric in enumerate(numeric_cols[:4]):
    latest_value = df[metric].dropna().iloc[-1] if not df[metric].dropna().empty else 0
    cols[i].metric(metric, f"{latest_value:,.2f}")

st.subheader("Trend")
selected_metric = st.selectbox("Kies metric", options=numeric_cols)

if time_col and df[time_col].notna().any():
    fig = px.line(df, x=time_col, y=selected_metric, markers=True, title=f"{selected_metric} over tijd")
else:
    fig = px.line(df.reset_index(), x="index", y=selected_metric, markers=True, title=f"{selected_metric} per rij")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Ruwe data")
st.dataframe(df.tail(100), use_container_width=True)
