import pandas as pd

def read_csv(folder:str="B", name:str="trx")->pd.DataFrame:
    return pd.read_csv(f"../uploads_{folder}/{name}.csv")

def read_products(folder:str="B")->pd.DataFrame:
	txt = pd.read_csv(f"../uploads_{folder}/products.txt", sep=" ")
	num_products, num_clients, neg_pts = list(txt.columns)[:3]
	products = txt[list(txt.columns)[0]]
	rewards = txt[list(txt.columns)[1]]

	return pd.DataFrame(data={"products":products, "rewards":rewards})

def get_client(clients:pd.DataFrame, account_number:int)->pd.DataFrame:
    """
    return row containing client with account number
    """
    return clients.loc[clients["account_number"] == account_number]

def get_net_incomes(trx:pd.DataFrame)->pd.Series:
	"""
	Returns series <sr> with net incomes of all client account ids
	sr.loc[acct_number] gives associated net income
	"""
	debits_and_credits = trx.groupby(['account_number', 'incoming'])['amount'].sum()
	df = debits_and_credits
	acct_nets = {acct: int(f.loc[acct][1] - f.loc[acct][0]) for acct in clients["account_number"]}

	index = []
	nets = []
	for acct, net_income in acct_nets.items():
		index.append(acct)
		nets.append(net_income)

	net_incomes = pd.Series(data=nets, index=index)

	return net_incomes

def write_solution(clients:pd.DataFrame, name:str="tests")->None:
    
    save_path = "../solution_{}.txt".format(name)
    
    with open(save_path,"w") as f:
        f.write(str(clients.shape[0]))
        f.write("\n")
        for acct in clients["account_number"]:
            f.write(str(acct))
            f.write(" ")
            f.write("get_investments")
            f.write("\n")