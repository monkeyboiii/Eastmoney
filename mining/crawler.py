import csv
import json
import os
import re
from random import randint, choice

import requests

import clock


class Stock:
    # Some static variables for www.test.com crawling
    directory = 'D:\\Program\\Python\\Eastmoney\\data\\'
    year_list = list(range(2010, 2020))
    quarter_list = ['03', '06', '09', '12']
    table_list = list(range(1, 8))
    dict_tables = {1: '业绩报表',
                   2: '业绩快报表',
                   3: '业绩预告表',
                   4: '预约披露时间表',
                   5: '资产负债表',
                   6: '利润表',
                   7: '现金流量表'}
    dicts = {1: 'YJBB',
             2: 'YJKB',
             3: 'YJYG',
             4: 'YYPL',
             5: 'ZCFZB',
             6: 'LRB',
             7: 'XJLLB'}
    seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


    def __init__(self, random_query=True, year_query=None, quarter_query=None, table_query=None):
        # Set query list
        self.random_query = random_query
        if random_query:
            self.year_query = [self.year_list[randint(0, 9)]]
            self.quarter_query = [self.quarter_list[randint(0, 3)]]
            self.table_query = [self.table_list[randint(0, 6)]]
        else:
            if year_query is None:
                year_query = self.year_list
            if quarter_query is None:
                quarter_query = self.quarter_query
            if table_query is None:
                table_query = self.table_list
            self.year_query = [year_query]
            self.quarter_query = [quarter_query]
            self.table_query = [table_query]

        # make and change directory
        file_path = self.directory
        if not os.path.exists(file_path): os.mkdir(file_path)
        os.chdir(file_path)
        print('Initiated! With ', end='')

        # Introduce a sample run
        if random_query:
            self.run_query()


    def run_query(self):
        """
        In a sample run,
            year_query, quarter_query, table_query
        are all initialized with a random variable of a size 1 list
        """
        for year in self.year_query:
            for quarter in self.quarter_query:
                for table in self.table_query:
                    # In a specific result
                    self.set_table(year, quarter, table)

                    constant = self.get_table(1)
                    page_all = constant[0]
                    data = constant[1]
                    start_page = 1
                    end_page = int(page_all.group(1))  # page_all is a regex outcome

                    if self.random_query:
                        print(' ' + self.date, end='')
                        print(len(data))
                        break

                    # Main job
                    self.write_header(table, data)
                    for page in range(start_page, end_page):
                        clk = clock.Clock(2)
                        print('\nDownloading page #{}/{}, {}, table {}...'
                              .format(page, end_page,
                                      self.date,
                                      table))
                        func = self.get_table(page)
                        data = func[1]
                        page = func[2]
                        self.write_table(table, data, page)


    def set_table(self, year, quarter, table):
        # days difference in months
        if quarter == '06' or quarter == '09':
            day = 30
        else:
            day = 31
        self.date = '{}-{}-{}'.format(year, quarter, day)

        # table to query
        if table == 1:
            self.category_type = 'YJBB20_'
            self.st = 'latestnoticedate'
            self.sr = -1
            self.filter = "(securitytypecode in ('058001001','058001002'))(reportdate=^%s^)" % self.date
        elif table == 2:
            self.category_type = 'YJBB20_'
            self.st = 'ldate'
            self.sr = -1
            self.filter = "(securitytypecode in ('058001001','058001002'))(rdate=^%s^)" % self.date
        elif table == 3:
            self.category_type = 'YJBB20_'
            self.st = 'ndate'
            self.sr = -1
            self.filter = " (IsLatest='T')(enddate=^2018-06-30^)"
        elif table == 4:
            self.category_type = 'YJBB20_'
            self.st = 'frdate'
            self.sr = 1
            self.filter = "(securitytypecode ='058001001')(reportdate=^%s^)" % self.date
        else:
            self.category_type = 'CWBB_'
            self.st = 'noticedate'
            self.sr = -1
            self.filter = '(reportdate=^%s^)' % self.date
        self.category = self.dicts[table]
        self.category_type = self.category_type + self.category

        # yield {
        #     'date': self.date,
        #     'category': self.dict_tables[table],
        #     'category_type': self.category_type,
        #     'st':self.st,
        #     'sr': self.sr,
        #     'filter': self.filter
        # }


    def get_table(self, page):
        js = 'var '
        obfuscation = ''
        for i in range(8):
            obfuscation = obfuscation + str(choice(self.seed))
        js = js + obfuscation + '={pages:(tp),data: (x)}'
        params = {
            'type': self.category_type,
            'token': '70f12f2f4f091e459a279469fe49eca5',
            'st': self.st,
            'sr': self.sr,
            'p': page,
            'ps': 50,  # page size
            'js': js,
            'filter': self.filter,
            'rt': 52800465
        }
        url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?'

        response = requests.get(url, params=params).text

        pat = re.compile('var.*?{pages:(\d+),data:.*?')
        page_all = re.search(pat, response)

        pattern = re.compile('var.*?data: (.*)}', re.S)
        items = re.search(pattern, response)

        data = items.group(1)
        data = json.loads(data)
        return page_all, data, page


    def write_header(self, table, data):
        with open('{}.csv'.format(self.dict_tables[table]),
                  'a',  # Appending mode
                  encoding='utf_8_sig', newline='') as f:
            if not f.__sizeof__():
                headers = list(data[0].keys())
            writer = csv.writer(f)
            writer.writerow(headers)


    def write_table(self, table, data, page):
        for d in data:
            with open('{}.csv'.format(self.dict_tables[table]),
                      'a',  # Appending mode
                      encoding='utf_8_sig', newline='') as f:
                w = csv.writer(f)
                w.writerow(d.values())


if __name__ == '__main__':
    _clk = clock.Clock(2)
    myStock = Stock(random_query=True)
