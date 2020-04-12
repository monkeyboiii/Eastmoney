import time

import matplotlib.pyplot as plt
import pandas as pd


t = time.time()
scode = '601200'
year_list = list(range(2013, 2020))
asset = ['scode', 'reportdate',
         'sumasset', 'sumshequity']
dic = {'scode': scode,
       'reportdate': [],
       'sumasset': [],
       'sumshequity': []}

for year in year_list:
	path = 'D:\\Program\\Python\\Mining\\stock_data\\' + str(year) + '\\资产负债表.csv'
	df = pd.read_csv(path, usecols=asset)
	try:
		for i in range(df.size):
			if str(df.loc[i]['scode']) == scode:
				dic['reportdate'].append(df.loc[i]['reportdate'])
				dic['sumasset'].append(df.loc[i]['sumasset'])
				dic['sumshequity'].append(df.loc[i]['sumshequity'])
	# print('Yes')
	# input('Check?')
	except Exception as e:
		continue

pl = pd.DataFrame(dic, columns=['scode', 'reportdate', 'sumasset', 'sumshequity'])
pl['sumasset'] = pl['sumasset'].astype('float')
pl['sumshequity'] = pl['sumshequity'].astype('float')

pl.plot(x='reportdate', kind='line')
plt.show()
print('Time consumed: ' + str(time.time() - t))
