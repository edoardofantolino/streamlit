import streamlit as st
import pandas as pd
from services.db_functions import *
from services.transaction_generator import *


response = get_all_transactions()
data = response.data
df = pd.DataFrame(data)


st.set_page_config(
    page_title="Dashboard",
    page_icon="📈",
    layout="wide"
)


st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:6px;">
        <div style="font-weight:600;">Current simulation time:</div>
        <div style="color:gray;">
            {db_functions.get_last_transaction_timestamp()}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Dashboard")

st.sidebar.header("Simulation Board")

if st.sidebar.button("Single Transaction"):
    add_transaction()
    st.rerun()

if st.sidebar.button("Simulate Day Fast"):
    simulate_day_fast()
    st.rerun()

if st.sidebar.button("Simulate Week Fast"):
    simulate_week_fast()
    st.rerun()

if st.sidebar.button("Simulate Single High Value Fraud"):
    single_anomalous_transaction_high_amount()
    st.rerun()

if st.sidebar.button("Simulate Multiple Low Value Fraud"):
    multiple_anomalous_transactions_low_amount()
    st.rerun()



col_tot_tr, col_tot_vol = st.columns(2)

with col_tot_tr:
    st.metric("Numero Transazioni Totali", get_total_number_of_transactions())

with col_tot_vol:
    st.metric(
        "Volume Totale",
        f"€ {get_total_volume():,.2f}"
    )

fraud_count = count_high_withdrawal_anomalies()
print(fraud_count)
if fraud_count > 0:
    if fraud_count == 1:
        st.error("🚨 Una transazione ad Alto Volume Anomala")
    else:
        st.error(f"🚨 {fraud_count} transazioni ad Alto Volume Anomale")

lv_fraud_count = count_low_value_frauds()
print(lv_fraud_count)
if lv_fraud_count > 0:
    if lv_fraud_count == 1:
        st.error("🚨 Una frode a basso volume e alta frequenza")
    else:
        st.error(f"🚨 {lv_fraud_count} frodi a Basso Volume e Alta Frequenza")

st.title("Top Filiali")

df = get_volume_per_filiale()

if not df.empty:
    df = df.sort_values("total_volume", ascending=False)
    df["filiale_name"] = pd.Categorical(
        df["filiale_name"],
        categories=df["filiale_name"],
        ordered=True
    )

    cols = st.columns(3)

    for i in range(3):
        if i == len(df):
            break
        
        cols[i].metric(
            label=df["filiale_name"].iloc[i],
            value=f"€ {df['total_volume'].iloc[i]:,.2f}".replace(",", " "),
        )

    st.bar_chart(
        df.set_index("filiale_name")["total_volume"]
    )
else:
    st.write("Nessuna transazione")




st.subheader("Transazioni dell'ultima settimana")

last_week_volume = get_transactions_lastweek()

if(len(last_week_volume)) != 0:
    st.bar_chart(
        last_week_volume.set_index("timestamp")
    )
else:
    st.write("Nessuna transazione")


bottom_col1, bottom_col2, bottom_col3, bottom_col4, bottom_col5 = st.columns(5)

with bottom_col1:
    if st.button("Simulate transaction"):
        add_transaction()
        st.rerun()

with bottom_col2:
    if st.button("Simulate a day fast"):
        simulate_day_fast()
        st.rerun()

with bottom_col3:
    if st.button("Simulate a week fast"):
        simulate_week_fast()
        st.rerun()

with bottom_col4:
    if st.button("Simulate HV Fraud"):
        single_anomalous_transaction_high_amount()
        st.rerun()

with bottom_col5:
    if st.button("Simulate LV Fraud"):
        multiple_anomalous_transactions_low_amount()
        st.rerun()

# --------------------------------------------
st.subheader("Numero transazioni giornaliere")

daily_volume = get_num_transactions_per_date()

if (len(daily_volume)) != 0:
    st.bar_chart(
        daily_volume.set_index("date")
    )
else:
    st.write("Nessuna transazione")


