import time

import matplotlib.pyplot as plt
import pandas as pd
import psycopg2 as ps

scode = 601200
login = {'database': 'stock_repo',
         'user': 'stocker',
         'password': 'stockbusiness',
         'host': 'localhost'}

st = time.time()
conn = ps.connect(**login)
query = 'select reportdate, ' \
        'sumasset, sumshequity ' \
        'from asset ' \
        'where scode in ({})' \
        ' order by reportdate;'.format(scode)

df = pd.read_sql(sql=query, con=conn)

print('Time consumed: ' + str(time.time() - st))

df.plot(x='reportdate', kind='line')
plt.show()
conn.close()
