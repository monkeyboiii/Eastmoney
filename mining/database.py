import pandas as pd
import psycopg2 as ps


class Database:
    errors = 0
    directory = 'D:\\Program\\Python\\Mining\\data\\资产负债表.csv'
    placeholder = ['', '-', 0, '0']
    login_info = {'database': 'stock_repo',
                  'user': 'stocker',
                  'password': 'stockbusiness',
                  'host': 'localhost'}
    year_list = list(range(2010, 2020))
    columns = {
        'stock': ['scode', 'companycode',
                  'sname', 'publishname',
                  'mkt'  # market
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


    def __init__(self):
        self.conn = ps.connect(**self.login_info)
        self.cursor = self.conn.cursor()


    def run_sql(self):
        for table in self.columns:
            print('Inserting {}...'.format(table))
            self.write_frame(self.directory, table)


    def write_frame(self, file, table):
        """
        Write records stored in a DataFrame to a SQL database.

        Parameters
        ----------
        table: table of SQL table
        file: path of file
        """

        frame = pd.read_csv(file, usecols=self.columns[table])
        frame.fillna('-', inplace=True)

        for line in frame.index:

            available = []
            accum = 0
            for item in frame.loc[line]:
                if item not in self.placeholder:
                    available.append(accum)
                accum = accum + 1

            if table == 'premium' and len(available) <= 2:
                # Premium table is full of null
                continue

            # Filter the key-value pairs
            key = [frame.columns[column] for column in available]
            keys = ','.join(key)
            value = ['\'' + str(frame.loc[line][i]) + '\'' for i in available]
            values = ','.join(value)

            insert_query = 'INSERT INTO public.%s ' \
                           '(%s) ' \
                           'VALUES (%s);' \
                           % (table, keys, values)
            try:
                self.cursor.execute(insert_query)
                self.conn.commit()
            except ps.Error as e:
                # Ignore errors
                self.errors = self.errors + 1
                self.conn.commit()
                continue

        self.conn.commit()
        self.cursor.close()


if __name__ == '__main__':
    # Pretty rigid form
    db = Database()
    db.write_frame(file='D:\\Program\\Python\\Mining\\mining\\test\\Test.csv'
                   , table='hybrid')
    print(str(db.errors) + ' errors, maybe duplicates.')
