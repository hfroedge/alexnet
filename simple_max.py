from utils import *
from preprocessing import normalize_df
trx = read_csv(folder='C', name='trx')

clients = read_csv(folder='C', name='clients')

df = convert_features(trx, clients)

df = normalize_df(df)

write_solution(clients, df)