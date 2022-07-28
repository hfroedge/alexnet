from utils import *
from preprocessing import normalize_df
trx = read_csv(folder='C', name='trx')

clients = read_csv(folder='C', name='clients')

df = convert_features(trx, clients)

df = normalize_df(df)




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


crutial = [car, utils, crypto, telecom, house_fee, mortage, home_insurance]

counter = 0

outfile = ""

scores_all = []

for index, row in df.iterrows():
    scores = []
    for i in crutial:
        scores.append(row[i] * meaning[i][1])
    if max(scores) > 45:
        out = str(index) + " " + str(meaning[crutial[scores.index(max(scores))]][0])
        scores_all.append(max(scores))
        outfile += out + '\n'
        counter += 1

    # if counter ==5:
    #     break

print(f'max {max(scores_all)}, avg {sum(scores_all)/len(scores_all)}')

outfile = str(counter) + '\n' + outfile

with open('answer_tmp.txt', 'w') as file:
    file.write(outfile)


# print(df[crutial])