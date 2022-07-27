import pandas as pd

def read_csv(folder:str, name:str)->pd.DataFrame:
    return pd.read_csv(f"../{folder}/{name}.csv")

def get_client(clients:pd.DataFrame, account_number:int)->pd.DataFrame:
    """
    return row containing client with account number
    """
    return clients.loc[clients["account_number"] == account_number]