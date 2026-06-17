from datetime import datetime, timedelta
from supabase import create_client
import pandas as pd

url = "https://yinthengfapdhtvgidoi.supabase.co"
key = "sb_publishable_P4Py0xWkBg2YAU5Wm0fpcw_Nj0--Ju9"
supabase = create_client(url, key)

accounts = [
    "IT1234", "IT2345", "IT3456", "IT4567",
    "IT5678", "IT6789", "IT7890", "IT8901"
]

# currencies = ["EUR", "USD"]
currencies = ["EUR"]
types = ["withdrawal", "deposit", "transfer"]


def get_all_transactions():
    return supabase.table("transactions").select("*").execute()


def get_transactions_lastweek():
    response = (
        supabase
        .rpc("get_last_week_transactions")
        .execute()
        )

    data = response.data
    df = pd.DataFrame(data)
    return df


def count_high_withdrawal_anomalies():
    totl_hv_anomalies = (
        supabase
        .rpc("count_high_withdrawal_anomalies")
        .execute()
        )

    totl_hv_anomalies = totl_hv_anomalies.data
    if totl_hv_anomalies != None:
        return totl_hv_anomalies
    return 0


def count_low_value_frauds():
    lv_anomalies = (
        supabase
        .rpc("get_low_value_fraud_detection")
        .execute()
        )

    lv_anomalies = lv_anomalies.data
    if len(lv_anomalies) != None:
        return len(lv_anomalies)
    return 0


def get_volume_per_filiale():
    response = (
        supabase
        .rpc("get_volume_per_filiale")
        .execute()
        )

    data = response.data
    df = pd.DataFrame(data)

    return df


def get_total_volume():
    total_volume = (
        supabase
        .rpc("get_tot_vol")
        .execute()
        )

    total_volume = total_volume.data
    if total_volume != None:
        return total_volume
    return 0


def get_last_transaction_timestamp():
    last_transaction = (
        supabase
        .rpc("get_last_transaction")
        .execute()
        )
    
    if len(last_transaction.data) != 0:
        last_transaction = datetime.strptime(last_transaction.data[0]["timestamp"], "%Y-%m-%dT%H:%M:%S")
        return last_transaction
    return datetime.now() - timedelta(days=30)


def get_total_number_of_transactions():
    total_number_of_transactions = (
        supabase
        .rpc("get_tot_num_transactions")
        .execute()
        )

    return total_number_of_transactions.data[0]["total_number_of_transactions"]


def get_num_transactions_per_date():
    total_number_of_transactions = (
        supabase
        .rpc("get_num_transaction_per_day")
        .execute()
        )
    
    total_number_of_transactions = total_number_of_transactions.data
    df_total_number_of_transactions = pd.DataFrame(total_number_of_transactions)
    
    return df_total_number_of_transactions

