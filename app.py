import streamlit as st
import pandas as pd
import plotly.express as px

# from utils.loader import load_data

st.set_page_config(
    page_title="Transaction Dashboard",
    layout="wide"
)

st.title("Transaction Dashboard")

# df = load_data()