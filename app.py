import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from services.db_functions import *


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

st.title("Transaction Dashboard (Next Week Transactions)")

st.sidebar.header("Simulation")

if st.sidebar.button("Single Transaction"):
    add_transaction()

if st.sidebar.button("Simulate Day"):
    simulate_day()

if st.sidebar.button("Simulate Day Fast"):
    simulate_day_fast()

if st.sidebar.button("Simulate Week Fast"):
    simulate_week_fast()

col_tot_tr, col_tot_vol = st.columns(2)

with col_tot_tr:
    st.metric("Numero Transazioni Totali", get_total_number_of_transactions())

with col_tot_vol:
    st.metric(
        "Volume Totale",
        f"€ {get_total_volume():,.2f}"
    )

st.title("Top Filiali")

df = get_volume_per_filiale().sort_values("total_volume", ascending=False)
df["filiale_name"] = pd.Categorical(
    df["filiale_name"],
    categories=df["filiale_name"],
    ordered=True
)

cols = st.columns(3)

for i in range(3):
    cols[i].metric(
        label=df["filiale_name"].iloc[i],
        value=f"€ {df['total_volume'].iloc[i]:,.2f}".replace(",", " "),
    )

st.bar_chart(
    df.set_index("filiale_name")["total_volume"]
)




st.subheader("Transazioni dell'ultima settimana")

# single_volume = (
#     df.groupby("timestamp")["amount"]
#     .sum()
#     .reset_index()
#     .sort_values("timestamp")
# )

last_week_volume = get_transactions_lastweek()

st.bar_chart(
    last_week_volume.set_index("timestamp")
)

# --------------------------------------------
st.subheader("Numero transazioni giornaliere")

daily_volume = get_num_transactions_per_date()

st.bar_chart(
    daily_volume.set_index("date")
)



col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Simulate transactions"):
        st.write("Creating transaction")
        add_transaction()

with col2:
    if st.button("Simulate a day"):
        st.write("Creating transactions")
        simulate_day()

with col3:
    if st.button("Simulate a day fast"):
        st.write("Creating transactions")
        simulate_day_fast()

with col4:
    if st.button("Simulate a week fast"):
        st.write("Creating transactions")
        simulate_week_fast()