import time

import pandas as pd
import psycopg2 as ps


error = 0
login = {'database': 'stock_repo',
         'user': 'stocker',
         'password': 'stockbusiness',
         'host': 'localhost'}
placeholder = ['', '-', 0, '0']
year_list = list(range(2013, 2020))
columns = {
    'stock': ['scode', 'companycode',
              'sname', 'publishname',
              'mkt',  # market
              ],
    'hybrid': ['hycode', 'scode'],
    'asset': ['scode', 'reportdate',  # released_date
              'sumasset', 'fixedasset',
              'monetaryfund', 'monetaryfund_tb',
              'accountrec', 'accountrec_tb',
              'inventory', 'inventory_tb',
              'sumliab', 'accountpay', 'accountpay_tb',
              'advancereceive', 'advancereceive_tb',
              'sumshequity', 'sumshequity_tb',
              'tsatz', 'tdetz', 'ld', 'zcfzl'],
    'premium': ['scode', 'reportdate',
                'cashanddepositcbank', 'cashanddepositcbank_tb',
                'loanadvances', 'loanadvances_tb',
                'saleablefasset', 'saleablefasset_tb',
                'borrowfromcbank', 'borrowfromcbank_tb',
                'acceptdeposit', 'acceptdeposit_tb',
                'sellbuybackfasset', 'sellbuybackfasset_tb',
                'settlementprovision', 'settlementprovision_tb',
                'borrowfund', 'borrowfund_tb',
                'agenttradesecurity', 'agenttradesecurity_tb',
                'premiumrec', 'premiumrec_tb',
                'stborrow', 'stborrow_tb',
                'premiumadvance', 'premiumadvance_tb']
}


def write_frame(table, con, file):
    """
    Write records stored in a DataFrame to a SQL database.

    Parameters
    ----------
    table: table of SQL table
    con: an open SQL database connection object
    file: path of file
    """

    frame = pd.read_csv(file, usecols=columns[table])
    frame.fillna('-', inplace=True)

    cur = con.cursor()

    for line in frame.index:

        available = []
        accum = 0
        for item in frame.loc[line]:
            if item not in placeholder:
                available.append(accum)
            accum = accum + 1

        if col == 'premium' and len(available) <= 2:
            continue

        key = [frame.columns[column] for column in available]
        keys = ','.join(key)
        # keys = 'uuid,' + keys
        value = ['\'' + str(frame.loc[line][i]) + '\'' for i in available]
        values = ','.join(value)
        # uuid[col] = uuid[col] + 1
        # values = '\'' + str(uuid[col]) + '\',' + values

        insert_query = 'INSERT INTO public.%s ' \
                       '(%s) ' \
                       'VALUES (%s);' \
                       % (table, keys, values)
        try:
            cur.execute(insert_query)
            con.commit()
        except ps.Error as e:
            con.commit()
            global error
            error = error + 1
            # uuid[col] = uuid[col] - 1
            if error % 10000 == 1:
                print(e)
                input(insert_query)
            continue

    con.commit()
    cur.close()


if __name__ == '__main__':

    start_time = time.time()

    conn = ps.connect(**login)

    for year in year_list:
        print('Year: ' + str(year))
        path = 'D:\\Program\\Python\\Mining\\stock_data\\' + str(year) + '\\资产负债表.csv'
        for col in columns:
            s_time = time.time()

            print('Inserting {}...'.format(col))
            write_frame(col, conn, path)

            # test = 'D:\\Program\\Python\\Mining\\stock_data\\2018\\learning.csv'
            # write_frame(col, conn, test)

            print('\tTask finished in {}s'.format(str(time.time() - s_time)))

        print(str(error) + ' errors in year ' + str(year))

    conn.close()

    print('\nALL finished in {}s'.format(str(time.time() - start_time)))
