import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from streamlit_autorefresh import st_autorefresh
import uuid
from datetime import datetime, timedelta
import random

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

st.title("Transaction Dashboard")

st.metric("Numero Transazioni", len(df))

st.metric(
    "Volume Totale",
    f"€ {df['amount'].sum():,.2f}"
)


# df = load_data()




accounts = [
    "IT1234", "IT2345", "IT3456", "IT4567",
    "IT5678", "IT6789", "IT7890", "IT8901"
]

# currencies = ["EUR", "USD"]
currencies = ["EUR"]
types = ["withdrawal", "deposit", "transfer"]

def random_amount(tx_type):

    valid_or_not = random.randint(0,100)

    # if valid_or_not is lower than 100 then we get a valid amount, 
    # otherwise we get an invalid string or empty value 
    if valid_or_not < 99:
        if tx_type == "deposit":
            return round(random.uniform(50, 5000), 2)
        elif tx_type == "withdrawal":
            return round(-random.uniform(20, 2000), 2)
        else:  # transfer
            return round(random.uniform(-1500, 1500), 2)
    else:
        if valid_or_not == 99 or valid_or_not == 100:
            # return "23%02))12"
            return 10000.00
        return

def add_transaction():
    current_timestamp = datetime.now() - timedelta(days=30)

    if current_timestamp.weekday() >= 5:  # Sabato o Domenica
        delta_seconds = random.randint(60, 1800)      # 1-30 minuti
    else:
        delta_seconds = random.randint(60, 3600)     # 1-60 minuti

    current_timestamp += timedelta(seconds=delta_seconds)

    timestamp = current_timestamp.strftime(
        "%Y/%m/%d %H:%M:%S"
    )

    tx_type = random.choice(types)

    i_date = timestamp
    i_account = random.choice(accounts)
    i_amount = random_amount(tx_type)
    i_currency = random.choice(currencies)

    new_transaction = {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": i_date,
        "account_id": i_account,
        "amount": i_amount,
        "transaction_type": tx_type,
        "is_fraud": False
    }

    response = supabase.table("transactions").insert(new_transaction).execute()
    print(response)


if st.button("Simulate transactions"):
    st.write("Creating transaction")
    add_transaction()