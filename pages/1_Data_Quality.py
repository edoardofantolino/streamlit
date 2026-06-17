import streamlit as st

st.set_page_config(
    page_title="Spiegazione script Data Quality",
    page_icon="📊",
    layout="wide",
)

st.title("Data Quality")
st.caption("Pagina statica per raccontare cosa fa lo script di estrazione, analisi preliminare e data quality.")

st.subheader("Requisito")
st.write("""
         L’obiettivo di questo progetto è pulire e analizzare un dataset di transazioni finanziarie. 
         Il dataset contiene informazioni sulle transazioni come il nome del prodotto, la quantità, il prezzo, il metodo di pagamento e lo stato della transazione.

Il focus principale di questo progetto è:

- Pulizia dei dati
- Gestione dei valori mancanti
- Standardizzazione dei dati inconsistenti""")

st.subheader("Codice")

with st.expander("1. Lettura File e Fase di Esplorazione"):
    st.code(
        """import zipfile
import pandas as pd


print("INIZIO")


# Estrazione del file

zip_path = "./archive.zip"
extract_path = "data"

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(extract_path)

print("Estrazione .zip completata")


# ANALISI PRELIMINARE DEL DATASET

df = pd.read_csv("./data/dirty_financial_transactions.csv")

print("-------------------------------------------")
print("INIZIO DELLA FASE DI ESPLOREAZIONE")
print("Informazioni generali su Dataset")

print(f"Il dataset contiene {len(df)} records")

print("Visualizza le prime righe del dataset")
print(df.head())

print("Visualizza le ultime righe del dataset")
print(df.tail())

print("Visualizza le tipologie di dato, le colonne, i non-nulli e la memoria occupata")
print(df.info())

print("Visualizza la sintesi statistica delle colonne di tipo numerico")
print(df.describe())

print("Visualizza quanti valori unici ci sono per colonna")
print(df.nunique())

print("Visualizza la presenza di Transaction_ID duplicati")
print(df["Transaction_ID"].value_counts())
print("Quante transazioni sono duplicate?", df["Transaction_ID"].duplicated().sum())
print("Quante transazioni hanno id nullo?", df["Transaction_ID"].isna().sum())

print("Visualizza quante celle mancanti ci sono per ogni colonna")
print(df.isnull().sum().sort_values(ascending=False))

print("Quante righe totalmente vuote?")
print(df.isnull().all(axis=1).sum())

print("Quante righe con almeno un dato mancante?")
print(df.isnull().any(axis=1).sum())


print("FASE DI ESPLORAZIONE COMPLETATA")
print("-------------------------------------------")
""",
        language="python",
    )

with st.expander("2. Trasformazioni per Data Quality e Salvataggio"):
    st.code(
        """print("-------------------------------------------")
print("INIZIO FASE DI DATA QUALITY")

# Creo una nuova colonna per tracciare la validità del record.
# Tutte le colonne sono inizializzate come 'valide'
# Creo una ulteriore colonna per tracciare le motivazioni dello scarto.

df["row_status"] = "VALID"
df["reject_reason"] = [[] for _ in range(len(df))]

# VALIDITY CHECKS

def add_reason(df, mask, reason):
    df.loc[mask, "row_status"] = "INVALID"
    df.loc[mask, "reject_reason"] = df.loc[mask, "reject_reason"].apply(
        lambda x: x + [reason]
    )


# Controllo duplicati Transaction_ID
print("Segna come non valide le transazioni con ID duplicato")
mask = df["Transaction_ID"].duplicated(keep=False)
add_reason(df, mask, "DUPLICATE_TRANSACTION_ID")

# Controllo Quantità Negativa
print("Segna come non valide le transazioni con quantità negativa")
mask = df["Quantity"] < 0
add_reason(df, mask, "NEGATIVE_QUANTITY")

# Controllo Prezzo Negativo 
print("Segna come non valide le transazioni con prezzo negativo")
# Fase 1 -> ripulisci il prezzo da possibili caratteri e currencies
df["Price_clean"] = (
    df["Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .astype(float)
)

mask = df["Price_clean"] < 0
add_reason(df, mask, "NEGATIVE_PRICE")

mask = df["Price_clean"].isna()
add_reason(df, mask, "NULL_PRICE")

mask = df["Quantity"].isna()
add_reason(df, mask, "NULL_QUANTITY")

mask = df["Transaction_Date"].isna()
add_reason(df, mask, "NULL_DATE")

mask = df["Customer_ID"].isna()
add_reason(df, mask, "NULL_CUSTOMER_ID")

print("Distribuzione righe valide e non valide")
print(df["row_status"].value_counts())


# Split Transazioni valide e transazioni non valide

df_valid = df[df["row_status"] == "VALID"]
df_invalid = df[df["row_status"] != "VALID"]

print("Numero record validi:", len(df_valid))
print("Numero record non validi:", len(df_invalid))

# print("DF valido")
# print(df_valid)

# print("DF non valido")
# print(df_invalid)





# RECOVERABLE ROWS

valid_methods = ["PayPal", "Credit Card", "Cash", "Bank Transfer"]
df_valid.loc[~df["Payment_Method"].isin(valid_methods), "row_status"] = "RECOVERABLE"

valid_transaction_status = ["Completed", "Failed", "Pending"]
df_valid.loc[~df["Transaction_Status"].isin(valid_transaction_status), "row_status"] = "RECOVERABLE"

print("Visualizza DF dei record validi e recuperabili")
print(df_valid)


# Recupero e trasformazione dei Payment Methods
print("Normalizzazione dei valori dell'attributo Payment Method")
print("Quanti record hanno Payment Method null? ->", df_valid["Payment_Method"].isna().sum())
print("Distribuzione dei valori Payment Method")
print(df_valid["Payment_Method"].value_counts())

print("Dettaglio con delimitatori delle stringhe Payment Methods")
for value in df_valid["Payment_Method"].unique():
    print(f"|{value}|")

print("Normalizzazione dei valori dell'attributo Payment Method")
# Normalizzazione metodi di pagamento
df_valid["Payment_Method"] = (
    df_valid["Payment_Method"]
    .str.strip()
    .str.lower()
)

df_valid["Payment_Method"] = df_valid["Payment_Method"].replace({
    "pay pal": "paypal",
    "creditcard": "credit card"
})  

print("Nuova distribuzione valori Payment Method")
print(df_valid["Payment_Method"].value_counts())




# Recupero e trasformazione del Transaction_Status
print("Normalizzazione dei valori dell'attributo Transaction Status")
print("Quanti record hanno Transaction Status a null? ->", df_valid["Transaction_Status"].isna().sum())
df_valid["Transaction_Status"] = df_valid["Transaction_Status"].fillna("On Hold")
print("Distribuzione orignale dei valori Transaction Status")
print(df_valid["Transaction_Status"].value_counts())

for value in df_valid["Transaction_Status"].unique():
    print(f"|{value}|")


print("Normalizzazione dei valori dell'attributo Transaction Status")
# Normalizzazione Stato della Transazione
df_valid["Transaction_Status"] = (
    df_valid["Transaction_Status"]
    .str.strip()
    .str.lower()
)

df_valid["Transaction_Status"] = df_valid["Transaction_Status"].replace({
    "complete": "completed",
})  

print("Nuova distribuzione valori Transaction Status")
print(df_valid["Transaction_Status"].value_counts())


# Normalizzazione Nome del Prodotto
print("Normalizzazione del Nome del Prodotto")
print("Distribuzione originale del Nome del Prodotto")
print(df_valid["Product_Name"].value_counts())
# replacing the wrong product name with original
replace_name = {
    'tab' : 'tablet',
    'coffee ma' : 'coffee machine',
    'coffee' : 'coffee machine',
    'cof' : 'coffee machine',
    'smar' : 'smartphone',
    'coffee m' : 'coffee machine',
    't' : 'tablet',
    'smartpho' : 'smartphone',
    'headp' : 'headphones',
    'smart' : 'smartphone',
    'smartph':'smartphone',
    'la' : 'laptop',
    'lapt' : 'laptop',
    'tabl' : 'tablet',
    'l' : 'laptop',
    'c' : 'coffee machine',
    'co' : 'coffee machine',
    'headphone': 'headphones',
    'coffee mac' : 'coffee machine',
    'sm' : 'smartphone',
    'headph' : 'headphones',
    's' : 'smartphone',
    'coffee mach' : 'coffee machine',
    'smartphon' : 'smartphone',
    'headpho' : 'headphones',
    'coffee machin' : 'coffee machine',
    'coff' : 'coffee machine',
    'lap' : 'laptop',
    'h' : 'headphones',
    'he' : 'headphones',
    'ta': 'tablet',
    'coffee machi' : 'coffee machine',
    'coffe' : 'coffee machine',
    'sma' : 'smartphone',
    'smartp' : 'smartphone',
    'hea' : 'headphones',
    'headphon': 'headphones',
    'head' : 'headphones',
    'lapto' :  'laptop',
    'table' : 'tablet'
}

df_valid["Product_Name"] = (
    df_valid["Product_Name"]
    .str.strip()
    .str.lower()
)

df_valid["Product_Name"] = df_valid["Product_Name"].replace(replace_name)  
print("\nNuova distribuzione Nome del Prodotto")
print(df_valid["Product_Name"].value_counts())



print("Frequenza valide e recuperabili")
print(df_valid["row_status"].value_counts())

print("Statistica finale di valori nulli per colonna")
print(df_valid.isnull().sum())

print("FINE FASE DI DATA QUALITY")
print("-------------------------------------------")




print("-------------------------------------------")
print("INIZIO CARICAMENTO DATI")

# Pulizia Finale e Riordinamento Colonne
df_valid["Price_clean"] = df_valid["Price_clean"].round(2)
df_valid = df_valid.drop(columns=["Price"])
df_valid.rename(columns={"Price_clean": "Price"}, inplace=True)
df_valid = df_valid[["Transaction_ID","Transaction_Date","Customer_ID","Price","Product_Name","Quantity","Payment_Method","Transaction_Status"]]
# df_valid.drop(columns=["Price","row_status", "reject_reason"]).to_csv("./data/output/valid_transactions.csv", index=False)
df_valid.to_csv("./data/output/valid_transactions.csv", index=False)
df_invalid.to_csv("./data/output/invalid_transactions.csv", index=False)

print("FINE CARICAMENTO DATI")
print("-------------------------------------------")


print("FINE")""",
        language="python",
    )


st.title("Spiegazione dello script Python")

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
    st.metric("Fasi principali", "5")
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
    """
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

with st.expander("Estratto del Codice - Fase di Esplorazione"):
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


with st.expander("Estratto della Risposta - Fase di Esplorazione"):
    st.code(
        """
Visualizza le prime righe del dataset
  Transaction_ID Transaction_Date Customer_ID    Product_Name  Quantity                Price Payment_Method Transaction_Status
0          T0001       2024-08-02       C2205      Headphones      -5.0              $420.21        pay pal                NaN
1          T0002       2020-02-10       C3156         Coffee      469.0  -445.34202525395585     creditcard            Pending
2          T0003       2025-02-30       C2919          Tablet      -4.0    810.9930123946459    credit card          completed
3          T0004       2020-08-17       C3009             Tab      -7.0    868.6083413217348         PayPal            Pending
4          T0005       2025-02-30       C3488  Coffee Machine     -10.0   -763.1224490039416         PayPal          completed


Visualizza le ultime righe del dataset
      Transaction_ID Transaction_Date Customer_ID Product_Name  Quantity               Price Payment_Method Transaction_Status
99995            NaN       2021-10-06       C1743   Headphones      -8.0   240.0032380562687        PayPal            complete
99996         T99997       2024-08-25       C4830   Smartphone       NaN  503.82951729633896    credit card          Completed
99997         T99998       2023-13-01        C280       Laptop     -10.0                 NaN        PayPal           completed
99998         T99999       2020-07-12       C4059   Headphones      10.0                 NaN        PayPal           Completed
99999        T100000       2023-10-04       C1805       Tablet       2.0   89.37402345793535        PayPal              Failed
""",
        language="text",
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

with st.expander("Estratto del Codice - Fase di verifica della validità dei record"):
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


with st.expander("Estratto della Risposta - Fase di verifica della validità dei record"):
    st.code("""
Record validi
      Transaction_ID Transaction_Date Customer_ID    Product_Name  Quantity  ... Payment_Method Transaction_Status row_status reject_reason Price_clean
13             T0014       2020-06-19       C2992  Coffee Machine     696.0  ...     creditcard             Failed      VALID            []  905.514730
24             T0025       2022-11-18       C4985          Tablet     114.0  ...         PayPal                NaN      VALID            []  276.936320
27             T0028       2025-02-30       C3025            Smar       7.0  ...         PayPal           complete      VALID            []  797.340000
34             T0035       2022-07-25       C2579  Coffee Machine     485.0  ...    credit card          Completed      VALID            []  970.280000
52             T0053       2022-07-22       C1077          Laptop     559.0  ...    credit card             Failed      VALID            []  154.185054
...              ...              ...         ...             ...       ...  ...            ...                ...        ...           ...         ...
99978         T99979       2025-02-30       C4733      Smartphone       3.0  ...         PayPal            Pending      VALID            []  588.007874
99986         T99987       2024-07-11        C173     Coffee Mach       7.0  ...    Credit Card                NaN      VALID            []  826.040830
99988         T99989       2025-02-30        C011         Smartph     542.0  ...    credit card             Failed      VALID            []  460.251987
99990         T99991       2023-13-01       C4555             Tab       2.0  ...        pay pal             Failed      VALID            []  131.036869
99991         T99992       2022-11-25        C836  Coffee Machine       3.0  ...     creditcard          completed      VALID            []  312.026301

[17671 rows x 11 columns]
Record non validi
      Transaction_ID Transaction_Date Customer_ID    Product_Name  ...  Transaction_Status row_status                                  reject_reason Price_clean
0              T0001       2024-08-02       C2205      Headphones  ...                 NaN    INVALID                            [NEGATIVE_QUANTITY]  420.210000
1              T0002       2020-02-10       C3156         Coffee   ...             Pending    INVALID                               [NEGATIVE_PRICE] -445.342025
2              T0003       2025-02-30       C2919          Tablet  ...           completed    INVALID                            [NEGATIVE_QUANTITY]  810.993012
3              T0004       2020-08-17       C3009             Tab  ...             Pending    INVALID                            [NEGATIVE_QUANTITY]  868.608341
4              T0005       2025-02-30       C3488  Coffee Machine  ...           completed    INVALID            [NEGATIVE_QUANTITY, NEGATIVE_PRICE] -763.122449
...              ...              ...         ...             ...  ...                 ...        ...                                            ...         ...
99995            NaN       2021-10-06       C1743      Headphones  ...            complete    INVALID  [DUPLICATE_TRANSACTION_ID, NEGATIVE_QUANTITY]  240.003238
99996         T99997       2024-08-25       C4830      Smartphone  ...           Completed    INVALID                                [NULL_QUANTITY]  503.829517
99997         T99998       2023-13-01        C280          Laptop  ...           completed    INVALID                [NEGATIVE_QUANTITY, NULL_PRICE]         NaN
99998         T99999       2020-07-12       C4059      Headphones  ...           Completed    INVALID                                   [NULL_PRICE]         NaN
99999        T100000       2023-10-04       C1805          Tablet  ...              Failed    INVALID                     [DUPLICATE_TRANSACTION_ID]   89.374023
    """, language="text",
)


st.header("4. Normalizzazione e record recuperabili")
st.markdown(
    """
    Lo script separa i record validi da quelli invalidi e poi sanifica alcune righe:
    - normalizza i metodi di pagamento;
    - normalizza lo stato della transazione;
    - corregge abbreviazioni o errori nei nomi prodotto.
    """
)

st.info(
    "Alcune anomalie non sono veri errori, ma solo variazioni di scrittura o dati sporchi correggibili.")

with st.expander("Estratto del Codice - Esempi di Normalizzazione"):
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


with st.expander("Estratto della Risposta - Esempi di Normalizzazione"):
    st.code(
"""
Distribuzione dei valori Payment Method prima della Normalizzazione
Payment_Method
pay pal        2558
creditcard     2557
Credit Card    2555
PayPal         2533
Cash           2512
PayPal         2486
credit card    2470

Distribuzione dei valori Payment Method dopo la Normalizzazione
Payment_Method
credit card    7582
paypal         7577
cash           2512
""",
        language="text",
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
        Il dataset originale presenta diverse criticità e il problema principale è la qualità del contenuto.
       
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

