import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from streamlit_autorefresh import st_autorefresh
from services.transaction_generation import *


url = "https://yinthengfapdhtvgidoi.supabase.co"
key = "sb_publishable_P4Py0xWkBg2YAU5Wm0fpcw_Nj0--Ju9"
supabase = create_client(url, key)

response = supabase.table("transactions").select("*").execute()
data = response.data
df = pd.DataFrame(data)

# from utils.loader import load_data

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


# df = load_data()


if st.button("Simulate transactions"):
    st.write("Creating transaction")
    add_transaction()