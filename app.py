import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from streamlit_autorefresh import st_autorefresh


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

# df = load_data()