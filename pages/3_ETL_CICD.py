import streamlit as st

st.set_page_config(
    page_title="ETL CI CD",
    page_icon="⚙️",
    layout="wide",
)

st.title("Pipeline ETL con Test Automatici e CI/CD")

st.markdown("""
L'obiettivo di questo progetto è realizzare una pipeline ETL affidabile per
l'elaborazione di dati relativi a transazioni finanziarie, garantendo al
tempo stesso elevati standard di qualità attraverso test automatici e
integrazione continua.

La pipeline acquisisce dati grezzi, applica regole di validazione e
trasformazione, e produce dataset puliti e pronti per attività di
reporting e analisi.

Per garantire la qualità del software, ogni modifica al codice viene
verificata automaticamente tramite GitHub Actions.
""")


st.subheader("Obiettivi")

st.markdown("""
- Estrarre i dati e generare dataset puliti e pronti all'uso
- Automatizzare i controlli tramite test unitari
- Eseguire i test automaticamente ad ogni modifica del codice
- Monitorare l'esecuzione della pipeline attraverso un sistema di logging strutturato
- Persistire i log su file in modalità append per mantenere lo storico delle esecuzioni
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
       st.subheader("Pipeline")
       st.code("""
            CSV INPUT
                 │
                 ▼
       DATA QUALITY CHECKS,
   DATA CLEANING e STANDARDIZATION
                 │
        ┌────────┴────────┐
        ▼                 ▼
 VALID RECORDS     INVALID RECORDS
        │                 │
        └────────┬────────┘
                 ▼
         LOGGING e AUDIT TRAIL
                 │
                 ▼
          PYTEST TESTS
                 │
                 ▼
       GITHUB ACTIONS CICD
""")

with col2:
       st.subheader("Architettura")
       st.code("""
bank-etl2/

├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── generator/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── main.py    
│   └── logger.py
│
├── tests/
├── logs/
│   └── etl.log            
├── .github/workflows/
│   └── ci.yml                
├── requirements.txt
└── README.md
""")


st.subheader("Tecnologie")

st.markdown("""
- Python e Pandas
- Pytest
- Git e GitHub Actions
""")


st.subheader("Test Automatici in Locale")

st.markdown("""
Per garantire l'affidabilità della pipeline sono stati implementati
test automatici in locale.

L'esecuzione automatica dei test permette di individuare rapidamente
eventuali regressioni introdotte durante lo sviluppo.
""")


with st.expander("Estratto del File di Test - Test Automatici"):
    st.code(
        """
# [...]
                
# Verify that accountid is not null
def test_account_nan():
    df = pd.DataFrame(data)
    df_valid, _, _ = transform(df, "test")

    assert not df_valid["account"].isna().any()


# Verify that transaction id is unique after clean_date
def test_transaction_id_unique():
    df = pd.DataFrame(data)
    df = clean_date(df)

    assert df["transaction_id"].is_unique
""",
        language="python"
    )



with st.expander("Estratto della Risposta File di Test - Test Automatici"):
    st.code(
"""
(venve) PS D:\software\visual studio code\VS projects\etl_project02\bank-etl2> pytest\n
============================================================ test session starts =============================================================
platform win32 -- Python 3.11.5, pytest-9.0.3, pluggy-1.6.0
rootdir: D:\software\visual studio code\VS projects\etl_project02\bank-etl2
configfile: pytest.ini
testpaths: test
plugins: anyio-4.13.0
collected 4 items                                                                                                                             

test\test_transform.py ....                                                                                                             [100%]

============================================================= 4 passed in 0.72s ==============================================================
""", language="text"
    )


st.subheader("🔒 Main branch protection")

st.markdown("""
Il progetto utilizza GitHub branch protection rules.
- Il branch `main` è protetto
- Non è consentito il push diretto
- Le modifiche devono passare da Pull Request
            
##### 🔁 Workflow adottato
feature branch → pull request → review → merge → main
""")
with st.expander("Estratto della Risposta - Tentativo di push su main"):
    st.code(
"""
(venve) PS D:\software\visual studio code\VS projects\etl_project02\bank-etl2> git push                         
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 391 bytes | 391.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.                                                                           
remote: error: GH006: Protected branch update failed for refs/heads/main.                                                                      
remote: 
remote: - Changes must be made through a pull request.                                                                                         
To https://github.com/edoardofantolino/bank-etl2
 ! [remote rejected] main -> main (protected branch hook declined)
error: failed to push some refs to 'https://github.com/edoardofantolino/bank-etl2'
""", language="text"
    )

with st.expander("Esempio di Pull Request protetta con controlli CI e Reviews"):
       st.image(
       "assets/github_pr.png",
       caption="Esempio di Pull Request protetta con controlli CI",
       use_container_width=True
       )


st.divider()

col_x, col_y = st.columns(2)

with col_x:
       st.subheader("Valore del progetto")

       st.markdown("""
       La soluzione permette di migliorare la qualità dei dati e l'affidabilità
       dei processi di analisi.

       Grazie all'automazione dei controlli e dei test è possibile:

       - Ridurre le regressioni
       - Accelerare il processo di sviluppo
       - Garantire maggiore fiducia nei dati utilizzati dal business
       """)

with col_y:
       st.subheader("Risultati")

       st.markdown("""
       ✔ Pipeline ETL completamente automatizzata

       ✔ Dataset puliti e standardizzati

       ✔ Test automatici integrati nel processo di sviluppo

       ✔ Controllo qualità continuo tramite GitHub Actions

       ✔ Processo facilmente estendibile e manutenibile
       """)