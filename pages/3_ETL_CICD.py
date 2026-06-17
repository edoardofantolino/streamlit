import streamlit as st

st.set_page_config(
    page_title="ETL CI CD",
    page_icon="📊",
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
- Acquisire dati da file CSV
- Validare la qualità dei dati
- Correggere e standardizzare valori inconsistenti
- Generare dataset puliti e pronti all'uso
- Automatizzare i controlli tramite test unitari
- Eseguire i test automaticamente ad ogni modifica del codice
- Monitorare l'esecuzione della pipeline attraverso un sistema di logging strutturato
- Persistire i log su file in modalità append per mantenere lo storico delle esecuzioni
- Facilitare attività di monitoraggio, debugging e auditing dei processi ETL
""")


st.subheader("Pipeline")
st.code("""
            CSV INPUT
                 │
                 ▼
       DATA QUALITY CHECKS
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


st.subheader("Tecnologie")

st.markdown("""
- Python
- Pandas
- Pytest
- Git
- GitHub Actions
""")


st.subheader("Testing")

st.markdown("""
Per garantire l'affidabilità della pipeline sono stati implementati
test automatici che verificano:

- Presenza delle colonne obbligatorie
- Assenza di valori nulli nei campi critici
- Correttezza delle trasformazioni applicate
- Validità dei dati esportati

L'esecuzione automatica dei test permette di individuare rapidamente
eventuali regressioni introdotte durante lo sviluppo.
""")


st.subheader("Continuous Integration")

st.markdown("""
È stata configurata una pipeline CI/CD tramite GitHub Actions.

Ad ogni push sul repository:

1. Viene scaricato il codice sorgente
2. Vengono installate le dipendenze necessarie
3. Vengono eseguiti i test automatici
4. Il risultato viene pubblicato all'interno del repository

Questo approccio consente di mantenere elevata la qualità del progetto
e ridurre il rischio di introdurre errori in produzione.
""")


st.subheader("Valore del progetto")

st.markdown("""
La soluzione permette di migliorare la qualità dei dati e l'affidabilità
dei processi di analisi.

Grazie all'automazione dei controlli e dei test è possibile:

- Ridurre gli errori nei dataset
- Migliorare l'affidabilità dei report
- Accelerare il processo di sviluppo
- Garantire maggiore fiducia nei dati utilizzati dal business
""")

st.subheader("Risultati")

st.markdown("""
✔ Pipeline ETL completamente automatizzata

✔ Dataset puliti e standardizzati

✔ Test automatici integrati nel processo di sviluppo

✔ Controllo qualità continuo tramite GitHub Actions

✔ Processo facilmente estendibile e manutenibile
""")