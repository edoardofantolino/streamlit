import streamlit as st


st.set_page_config(
    page_title="Home",
    layout="wide",
)

st.title("Progetto per CRA")

st.markdown("""
Questo progetto è composto da diversi moduli di data engineering per la gestione di dati bancari:
- [Python] trasformazioni, pulizia e controlli di qualità sui dati
- [SQL] dashboard di monitoraggio
- [Git - CICD] test locali e workflow su GitHub
""")

st.divider()

st.markdown("### Seleziona una sezione:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Data Quality", use_container_width=True):
        st.switch_page("pages/1_Data_Quality.py")

with col2:
    if st.button("📈 Dashboard", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")

with col3:
    if st.button("⚙️ ETL & CI/CD", use_container_width=True):
        st.switch_page("pages/3_ETL_CICD.py")