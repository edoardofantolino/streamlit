import streamlit as st


st.markdown("Seleziona una sezione:")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/1_Data_Quality.py", label="📊 Data Quality")

with col2:
    st.page_link("pages/2_Dashboard.py", label="📈 Dashboard")

with col3:
    st.page_link("pages/3_ETL_CICD.py", label="⚙️ ETL & CI/CD")