import tushare as ts


df = ts.get_stock_basics()

print(df.groupby(['code']))
