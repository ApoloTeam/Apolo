import tushare as ts
import os
import datetime
import pandas as pd
import numpy as np

print('version: ' + ts.__version__)
now = datetime.datetime.now()
# print(now.strftime('%Y''%m''%d'))

def get_profit_data(year, quarter):
    if os.path.exists('./data/profit_data') is False:
        os.makedirs('./data/profit_data')
    df = ts.get_profit_data(year, quarter)
    df.to_csv('./data/profit_data/%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter profit data report downloaded.' % (str(year), str(quarter)))

def get_profit_data_range(from_year, to_year):
    for y in np.arange(from_year,to_year+1):
        for q in np.arange(1,4+1):
            get_profit_data(y, q)

# 获取沪深上市公司基本情况
def get_stock_basics():
    # if folder doest exists, then create.
    if os.path.exists('./data/stock_basics') is False:
        os.makedirs('./data/stock_basics')
    df = ts.get_stock_basics()
    df.to_csv('./data/stock_basics/%s%s%s.csv' % (str(now.year), str(now.strftime('%m')), str(now.strftime('%d'))))
    print('Stock basics downloaded.')


def get_sse50(year, quarter):
    if os.path.exists('./data/sse50') is False:
        os.makedirs('./data/sse50')
    df = ts.get_sz50s()
    df.to_csv('./data/sse50/%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter sse50 downloaded.' % (str(year), str(quarter)))


def stock_master(date):
    sm = pd.DataFrame(pd.read_csv('./data/stock_basics/20170525.csv', encoding='gbk'))
    sm = sm[(sm['timeToMarket'] < date)]
    sm = sm.sort_values(by=['code'], ascending=True)
    print(sm.head(10))
    print(type(sm['code']))
    print(sm['code'])


def filter_stock_list_sse50(date):
    sse50 = pd.read_csv('./data/sse50/2017_2.csv', encoding='gbk')
    stock_list = pd.read_csv('./data/stock_basics/20170601.csv', encoding='gbk')
    data = pd.merge(sse50, stock_list, on=['code'], how='left')
    data = data[(data['timeToMarket'] < date)]
    data = data[['code', 'name_x', 'area', 'industry', 'timeToMarket']]
    data = pd.DataFrame(data)
    data = data.fillna({'area': 'miss', 'industry': 'miss'})
    data.to_csv('./data/sse50/2017_2_Filtered.csv')

if __name__ == '__main__':
    # get_sse50(2017, 2)
    # filter_stock_list_sse50(20120101)
    get_profit_data_range(2014,2017)
