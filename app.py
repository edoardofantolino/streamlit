import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from services.transaction_generation import *


response = get_all_transactions()
data = response.data
df = pd.DataFrame(data)

st_autorefresh(
    interval=5000,
    key="refresh"
)

st.set_page_config(
    page_title="Transaction Dashboard",
    layout="wide"
)

st.title("Transaction Dashboard (Next Transaction)")

st.metric("Numero Transazioni", get_total_number_of_transactions())

if len(df) != 0:
    st.metric(
        "Volume Totale",
        f"€ {df['amount'].sum():,.2f}"
    )

    st.subheader("Singola transazione")

    single_volume = (
        df.groupby("timestamp")["amount"]
        .sum()
        .reset_index()
        .sort_values("timestamp")
    )

    st.line_chart(
        single_volume.set_index("timestamp")
    )

if st.button("Simulate transactions"):
    st.write("Creating transaction")
    add_transaction()

if st.button("Simulate a day"):
    st.write("Creating transactions")
    # add_transaction()