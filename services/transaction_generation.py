import uuid
from datetime import datetime, timedelta
from supabase import create_client
import random
import time
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
    print(df)
    return df

get_transactions_lastweek()

def get_total_volume():
    total_volume = (
        supabase
        .rpc("get_tot_vol")
        .execute()
        )

    return total_volume.data

def random_amount(tx_type):

    valid_or_not = random.randint(0,100)

    # if valid_or_not is lower than 100 then we get a valid amount, 
    # otherwise we get an invalid string or empty value 
    if valid_or_not < 99:
        if tx_type == "deposit":
            return round(random.uniform(50, 5000), 2)
        elif tx_type == "withdrawal":
            return round(-random.uniform(20, 2000), 2)
        else:  # transfer
            return round(random.uniform(-1500, 1500), 2)
    else:
        if valid_or_not == 99 or valid_or_not == 100:
            # return "23%02))12"
            return 10000.00
        return

def add_transaction():
    current_timestamp = get_last_transaction_timestamp()
    print("Last transaction:", current_timestamp)

    if current_timestamp.weekday() >= 5:  # Sabato o Domenica
        delta_seconds = random.randint(60, 1800)      # 1-30 minuti
    else:
        delta_seconds = random.randint(60, 3600)     # 1-60 minuti

    current_timestamp += timedelta(seconds=delta_seconds)

    timestamp = current_timestamp.strftime(
        "%Y/%m/%d %H:%M:%S"
    )

    tx_type = random.choice(types)

    i_date = timestamp
    i_account = random.choice(accounts)
    i_amount = random_amount(tx_type)
    i_currency = random.choice(currencies)

    new_transaction = {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": i_date,
        "account_id": i_account,
        "amount": i_amount,
        "transaction_type": tx_type,
        "is_fraud": False
    }

    response = supabase.table("transactions").insert(new_transaction).execute()
    print(response)


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

def simulate_day():
    print("Simulate day Start")
    starting_time = get_last_transaction_timestamp()
    ending_time = starting_time + timedelta(days=1)
    print("We need to start the creation of the transactions from", starting_time)
    print("We need to stop the creation of the transactions when we surpass", starting_time + timedelta(days=1))

    i = 0
    while get_last_transaction_timestamp() < ending_time:
        print("Add -", i)
        i+=1
        add_transaction()
        time.sleep(0.1)

    print("Simulate day End")



def simulate_day_fast():
    print("Simulate day fast Start")
    starting_time = get_last_transaction_timestamp()
    current_timestamp = get_last_transaction_timestamp()
    ending_time = starting_time + timedelta(days=1)
    print("We need to start the creation of the transactions from", starting_time)
    print("We need to stop the creation of the transactions when we surpass", starting_time + timedelta(days=1))

    transactions = []
    while current_timestamp < ending_time:
        print(current_timestamp)

        if current_timestamp.weekday() >= 5:
            delta_seconds = random.randint(60, 1800)
        else:
            delta_seconds = random.randint(60, 3600)

        current_timestamp += timedelta(seconds=delta_seconds)

        tx_type = random.choice(types)

        transactions.append({
            "transaction_id": str(uuid.uuid4()),
            "timestamp": current_timestamp.isoformat(),
            "account_id": random.choice(accounts),
            "amount": random_amount(tx_type),
            "transaction_type": tx_type,
            "is_fraud": False
        })

    response = (
        supabase
        .table("transactions")
        .insert(transactions)
        .execute()
    )

    print(response)
    print("Simulate day fast End")



def get_num_transactions_per_date():
    total_number_of_transactions = (
        supabase
        .rpc("get_num_transaction_per_day")
        .execute()
        )
    
    total_number_of_transactions = total_number_of_transactions.data
    df_total_number_of_transactions = pd.DataFrame(total_number_of_transactions)
    print(df_total_number_of_transactions)
    
    return df_total_number_of_transactions



def simulate_week_fast():
    print("Simulate week fast Start")
    starting_time = get_last_transaction_timestamp()
    current_timestamp = get_last_transaction_timestamp()
    ending_time = starting_time + timedelta(days=7)
    print("We need to start the creation of the transactions from", starting_time)
    print("We need to stop the creation of the transactions when we surpass", starting_time + timedelta(days=7))

    transactions = []
    while current_timestamp < ending_time:
        print(current_timestamp)

        if current_timestamp.weekday() >= 5:
            delta_seconds = random.randint(60, 1800)
        else:
            delta_seconds = random.randint(60, 3600)

        current_timestamp += timedelta(seconds=delta_seconds)

        tx_type = random.choice(types)

        transactions.append({
            "transaction_id": str(uuid.uuid4()),
            "timestamp": current_timestamp.isoformat(),
            "account_id": random.choice(accounts),
            "amount": random_amount(tx_type),
            "transaction_type": tx_type,
            "is_fraud": False
        })

    response = (
        supabase
        .table("transactions")
        .insert(transactions)
        .execute()
    )

    print(response)
    print("Simulate week fast End")

