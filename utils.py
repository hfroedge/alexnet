import pandas as pd

def read_csv(folder:str="B", name:str="trx")->pd.DataFrame:
	return pd.read_csv(f"../uploads_{folder}/{name}.csv")

def read_products(folder:str="B")->pd.DataFrame:
	txt = pd.read_csv(f"../uploads_{folder}/products.txt", sep=" ")
	num_products, num_clients, neg_pts = list(txt.columns)[:3]
	products = txt[list(txt.columns)[0]]
	rewards = txt[list(txt.columns)[1]]

	return pd.DataFrame(data={"products":products, "rewards":rewards})

def convert_features(trx:pd.DataFrame, clients:pd.DataFrame)->pd.DataFrame:
	categ = set(trx.value_counts('description').index)

	clothes = 'clothes'
	income = 'income'
	utils = 'utilities'
	crypto = 'crypto'
	car = 'car'
	food = 'food'
	telecom = 'telecom'
	house_fee = 'house_fee'
	health = 'health'
	education = 'education'
	shopping = 'shopping'

	usefull_categ = ['clothes', 'food shopping', 'gas electricity', 'gas station', 'housing fee', 'Monthly Rent subsidy', 'crypto', 'allowance', 'tuition fee', 'fuel', 'doctor appointment', 'telco', 'groceries', 'internet&tv', 'salary', 'pension', 'housing', 'monthly pension', 'shopping', 'Month payment student financing', 'monthly salary', 'gas', 'clothes shopping', 'grocery shopping', 'petrol', 'buy crypto', 'energy', 'crypto trading', 'utilities', 'dentist', 'accomodation', 'medicine',  'monthly allowance']
	conversion = {'clothes':clothes, 'food shopping':food, 'gas electricity':car, 'gas station':car, 'housing fee':house_fee, 'Monthly Rent subsidy':income, 'crypto':crypto, 'allowance':income, 'tuition fee':education, 'fuel':car, 'doctor appointment':health, 'telco':telecom, 'groceries':food, 'internet&tv':telecom, 'salary':income, 'pension':income, 'housing':house_fee, 'monthly pension':income, 'shopping':shopping, 'Month payment student financing':income, 'monthly salary':income, 'gas':car, 'clothes shopping':clothes, 'grocery shopping':food, 'petrol':car, 'buy crypto':crypto, 'energy':utils, 'crypto trading':crypto, 'utilities':utils, 'dentist':health, 'accomodation':house_fee, 'medicine':health,  'monthly allowance':income}


	trx = trx.drop(trx[trx.description.isin(usefull_categ) == False].index)

	trx = trx.replace({'description':conversion})

	sum_feat = trx.groupby(by=['description', 'account_number'])['amount'].sum()

	series = []
	names = []
	for cat in set(trx['description']):
	    names.append(cat)
	    series.append(sum_feat.loc[cat])

	df = pd.DataFrame(data={k:v for k,v in zip(names, series)})
	df = df.fillna(0)

	df = pd.merge(clients, df, on='account_number')
	df = df.set_index("account_number")
	df = df.drop(["name", "address"], axis=1)

	feature_set = df

	return feature_set


def get_client(clients:pd.DataFrame, account_number:int)->pd.DataFrame:
    """
    return row containing client with account number
    """
    return clients.loc[clients["account_number"] == account_number]

def get_net_incomes(trx:pd.DataFrame, clients:pd.DataFrame)->pd.Series:
	"""
	Returns series <sr> with net incomes of all client account ids
	sr.loc[acct_number] gives associated net income
	"""
	debits_and_credits = trx.groupby(['account_number', 'incoming'])['amount'].sum()
	df = debits_and_credits
	acct_nets = {acct: int(df.loc[acct][1] - df.loc[acct][0]) for acct in clients["account_number"]}

	index = []
	nets = []
	for acct, net_income in acct_nets.items():
		index.append(acct)
		nets.append(net_income)

	net_incomes = pd.Series(data=nets, index=index)

	return net_incomes

def __get_recommendation(client:pd.DataFrame, features:pd.DataFrame, acct_num:int)->str:
	"""
	Given client row, gives recommendation 

	:param client: row from clients csv
	:param features: consolidated data of all clients

	:return recommendation
	"""
	# if client["has_mortgage"].values[0] == 1:
	#     recommendation =  "refinance_mortgage"
	# elif features.loc[acct_num]["crypto"] > 0.19:
	#     recommendation = "get_investments"
	# else:
	# 	recommendation = ""

	# Hand picked values which connect feature with product
	clothes = 'clothes'
	income = 'income'
	utils = 'utilities'
	crypto = 'crypto'
	car = 'car'
	food = 'food'
	telecom = 'telecom'
	house_fee = 'house_fee'
	health = 'health'
	education = 'education'
	shopping = 'shopping'
	mortage = 'has_mortgage'
	home_insurance = 'has_home_insurance'
	car_insurance = 'has_car_insurance'


	meaning = {
		telecom: ["switch_telco", 80],
		home_insurance: ["switch_home_insurance", 100],
		mortage: ["refinance_mortgage", 850],
		house_fee: ["get_home_insurance", 200],
		crypto: ["get_investments", 900],
		car: ["get_car_insurance", 300],
		utils: ["switch_utils", 100],
	}

	# chosen features
	crutial = [car, utils, crypto, telecom, house_fee, mortage, home_insurance]

	# generating score for each important feature
	scores = []
	for i in crutial:
		scores.append(features.loc[acct_num][i] * meaning[i][1])

	if max(scores) > 45:
		return str(meaning[crutial[scores.index(max(scores))]][0])
	return ""

def write_solution(clients:pd.DataFrame, features:pd.DataFrame, name:str="tests")->None:
    
	save_path = "../solution_{}.txt".format(name)

	num_clients = 0
	recommendations = []
	accounts = []
	for acct in clients["account_number"]:
	    
		recommendation = __get_recommendation(clients.loc[clients["account_number"]==acct], features, acct)
        
		if recommendation != "":
			recommendations.append(recommendation)
			accounts.append(acct)

    
	with open(save_path,"w") as f:
		f.write(str(len(recommendations)))
		f.write("\n")
		for acct, rec in zip(accounts, recommendations):
			f.write(str(acct))
			f.write(" ")
			f.write(rec)
			f.write("\n")

