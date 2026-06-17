import streamlit as st

st.title("Data Quality")

st.write("Controlli qualità sui dati")

st.subheader("2. Standardizzazione Payment Method")

st.code("""
df["Payment_Method"] = (
    df["Payment_Method"]
    .str.strip()
    .str.lower()
    .replace({
        "pay pal": "paypal",
        "creditcard": "credit card"
    })
)
""", language="python")