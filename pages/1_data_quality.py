import streamlit as st

st.title("Data Quality")

st.write("Controlli qualità sui dati")

st.subheader("Problema iniziale")

st.subheader("Codice")

import streamlit as st

st.set_page_config(
    page_title="Spiegazione script Data Quality",
    page_icon="📊",
    layout="wide",
)

st.title("Spiegazione dello script Python")
st.caption("Pagina statica per raccontare cosa fa lo script di estrazione, analisi preliminare e data quality.")

st.markdown(
    """
    Questo script prende un file `.zip`, estrae un CSV di transazioni finanziarie,
    esegue una prima analisi esplorativa, applica controlli di qualità sui dati,
    normalizza alcuni campi e salva due file finali:
    uno con i record validi e uno con quelli non validi.
    """
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Fasi principali", "4")
with col2:
    st.metric("Output finali", "2 CSV")
with col3:
    st.metric("Obiettivo", "Pulizia dati")

st.divider()

st.header("1. Estrazione del file ZIP")
st.markdown(
    """
    Lo script inizia importando `zipfile` e `pandas`, poi estrae il contenuto di `archive.zip`
    nella cartella `data`.

    In pratica:
    - apre l'archivio ZIP;
    - estrae tutti i file nella directory `data`;
    - stampa un messaggio di conferma a console.
    """
)
with st.expander("Cosa succede nel codice"):
    st.code(
        """zip_path = "./archive.zip"
extract_path = "data"

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(extract_path)""",
        language="python",
    )

st.header("2. Lettura del CSV e analisi esplorativa")
st.markdown(
    """
    Dopo l'estrazione, il CSV `dirty_financial_transactions.csv` viene caricato in un DataFrame.
    La fase esplorativa serve a capire com'è fatto il dataset prima di intervenire con la pulizia.
    """
)

st.subheader("Informazioni che lo script stampa")
info_blocks = [
    "Numero totale di record",
    "Prime e ultime righe (`head()` e `tail()`)",
    "Tipi di dato e valori non nulli (`info()`)",
    "Statistiche descrittive sulle colonne numeriche (`describe()`)",
    "Numero di valori unici per colonna (`nunique()`)",
    "Duplicati e valori nulli su `Transaction_ID`",
    "Distribuzione dei valori mancanti per colonna",
    "Numero di righe completamente vuote e righe con almeno un dato mancante",
]
st.write("\n".join(f"- {x}" for x in info_blocks))

with st.expander("Estratto del codice"):
    st.code(
        """df = pd.read_csv("./data/dirty_financial_transactions.csv")

print(f"Il dataset contiene {len(df)} records")
print(df.head())
print(df.tail())
print(df.info())
print(df.describe())
print(df.nunique())
print(df["Transaction_ID"].duplicated().sum())
print(df.isnull().sum().sort_values(ascending=False))
print(df.isnull().all(axis=1).sum())
print(df.isnull().any(axis=1).sum())""",
        language="python",
    )

st.header("3. Data Quality")
st.markdown(
    """
    In questa fase lo script crea due nuove colonne:
    `row_status` per indicare se la riga è valida o meno, e `reject_reason` per salvare il motivo dello scarto.

    Poi applica diversi controlli:
    - Transaction_ID duplicato
    - Quantity negativa
    - Price negativo o nullo
    - Transaction_Date nullo
    - Customer_ID nullo
    """
)

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Stato del record")
    st.markdown(
        """
        - `VALID`: record conforme ai controlli iniziali
        - `INVALID`: record con uno o più problemi
        - `RECOVERABLE`: record con anomalie correggibili in fase di normalizzazione
        """
    )
with col_b:
    st.subheader("Motivi di scarto")
    st.markdown(
        """
        I motivi vengono accumulati in una lista, così un record può avere più problemi contemporaneamente.
        Esempi: `DUPLICATE_TRANSACTION_ID`, `NEGATIVE_PRICE`, `NULL_CUSTOMER_ID`.
        """
    )

with st.expander("Codice per individuare e marcare i record non validi"):
    st.code(
        """def add_reason(df, mask, reason):
    df.loc[mask, "row_status"] = "INVALID"
    df.loc[mask, "reject_reason"] = df.loc[mask, "reject_reason"].apply(
        lambda x: x + [reason])
        
mask = df["Transaction_ID"].duplicated(keep=False)
add_reason(df, mask, "DUPLICATE_TRANSACTION_ID")

mask = df["Quantity"] < 0
add_reason(df, mask, "NEGATIVE_QUANTITY")

mask = df["Price_clean"] < 0
add_reason(df, mask, "NEGATIVE_PRICE")

mask = df["Price_clean"].isna()
add_reason(df, mask, "NULL_PRICE")

mask = df["Quantity"].isna()
add_reason(df, mask, "NULL_QUANTITY")

mask = df["Transaction_Date"].isna()
add_reason(df, mask, "NULL_DATE")

mask = df["Customer_ID"].isna()
add_reason(df, mask, "NULL_CUSTOMER_ID")""",
        language="python",
    )

st.header("4. Normalizzazione e record recuperabili")
st.markdown(
    """
    Lo script separa i record validi da quelli invalidi e poi prova a recuperare alcune righe:
    - normalizza i metodi di pagamento;
    - normalizza lo stato della transazione;
    - corregge abbreviazioni o errori nei nomi prodotto.
    """
)

st.info(
    "Alcune anomalie non sono veri errori, ma solo variazioni di scrittura o dati sporchi correggibili.")

with st.expander("Esempi di normalizzazione"):
    st.code(
        """df_valid["Payment_Method"] = (
    df_valid["Payment_Method"]
    .str.strip()
    .str.lower()
)

df_valid["Payment_Method"] = df_valid["Payment_Method"].replace({
    "pay pal": "paypal",
    "creditcard": "credit card"
})  

df_valid["Transaction_Status"] = (
    df_valid["Transaction_Status"].fillna("On Hold").str.strip().str.lower()
)
""",
        language="python",
    )

st.header("5. Salvataggio finale")
st.markdown(
    """
    Alla fine lo script:
    - arrotonda il prezzo pulito;
    - sostituisce la colonna originale `Price` con quella pulita;
    - riordina le colonne finali;
    - salva `valid_transactions.csv` e `invalid_transactions.csv`.
    """
)

with st.expander("Output atteso"):
    st.code(
        """df_valid.to_csv("./data/output/valid_transactions.csv", index=False)
df_invalid.to_csv("./data/output/invalid_transactions.csv", index=False)""",
        language="python",
    )

st.divider()

st.header("Risultati osservati nell'esecuzione")
st.markdown(
    """
    Dall'output emergono alcuni numeri molto interessanti:
    - il dataset contiene **100.000 record**;
    - le righe totalmente vuote sono **0**;
    - le righe con almeno un valore mancante sono **54.667**;
    - i record marcati come **INVALID** sono **82.329**;
    - i record inizialmente **VALID** sono **17.671**.
    """
)

col_x, col_y = st.columns(2)
with col_x:
    st.subheader("Cosa si vede subito")
    st.markdown(
        """
        Il dataset è molto sporco, ma non è disorganizzato a livello strutturale: le colonne sono presenti,
        i tipi sono per lo più leggibili e il problema principale è la qualità del contenuto.
       
        Le anomalie più forti sono:
        - `Transaction_ID` duplicati o nulli;
        - `Quantity` negative;
        - `Price` negativo o mancante;
        - date non valide come `2025-02-30` o `2023-13-01`;
        - valori sporchi nei campi categorici.
        """
    )
with col_y:
    st.subheader("Effetto della normalizzazione")
    st.markdown(
        """
        La normalizzazione riduce drasticamente la variabilità dei valori testuali.
       
        Per esempio:
        - `Payment_Method` passa da varianti come `pay pal`, `creditcard`, `PayPal ` a valori standardizzati;
        - `Transaction_Status` converte `complete` in `completed` e sostituisce i null con `On Hold`;
        - `Product_Name` passa da molte abbreviazioni a sole 5 categorie finali.
        """
    )
