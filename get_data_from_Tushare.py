import tushare as ts
import os
import datetime
import pandas as pd
import numpy as np
import pymysql
from lib.connect_database import connect_server
# from lib.connect_database import create_engine
from sqlalchemy import create_engine

print('version: ' + ts.__version__)
now = datetime.datetime.now()
DATA_DIR = 'E:\\Apolo\\raw_data'
STOCK_BASICS_DIR = os.path.join(DATA_DIR, 'stock_basics')
REPORT_DATA_DIR = os.path.join(DATA_DIR, 'report_data')
PROFIT_DATA_DIR = os.path.join(DATA_DIR, 'profit_data')


def connect_engine():
    engine = create_engine('mysql+pymysql://york:4466@localhost/apolo?charset=utf8')
    return engine


# 获取沪深上市公司基本情况
def get_stock_basics():
    # if folder doest exists, then create.
    if os.path.exists(STOCK_BASICS_DIR) is False:
        os.makedirs(STOCK_BASICS_DIR)
    df = ts.get_stock_basics()
    # df.to_csv(os.path.join(STOCK_BASICS_DIR,'%s%s%s.csv' % (str(now.year), str(now.strftime('%m')), str(now.strftime('%d')))))
    engine = connect_engine()
    print(type(df))
    df.to_sql('stock_basics', engine, if_exists='replace', index=False)
    print('Stock basics downloaded.')


# 获取某年某季度的业绩报表数据
def get_report_data(year, quarter):
    if os.path.exists(REPORT_DATA_DIR) is False:
        os.makedirs(REPORT_DATA_DIR)
    df = ts.get_report_data(year, quarter)
    # df.to_csv(os.path.join(REPORT_DATA_DIR, '%s_%s.csv' % (str(year), str(quarter))))
    # engine = connect_engine()
    df.to_sql('report_data', engine)

    print('\n%s year %s quarter report data report downloaded.' % (str(year), str(quarter)))


def get_report_data_range(from_year, to_year):
    for y in np.arange(from_year,to_year+1):
        for q in np.arange(1,4+1):
            get_report_data(y, q)


# 获取某年某季度的盈利能力数据
def get_profit_data(year, quarter):
    if os.path.exists(PROFIT_DATA_DIR) is False:
        os.makedirs(PROFIT_DATA_DIR)
    df = ts.get_profit_data(year, quarter)
    df.to_csv(os.path.join(PROFIT_DATA_DIR, './data/profit_data/%s_%s.csv' % (str(year), str(quarter))))
    print('\n%s year %s quarter profit data report downloaded.' % (str(year), str(quarter)))


def get_profit_data_range(from_year, to_year):
    for y in np.arange(from_year,to_year+1):
        for q in np.arange(1,4+1):
            get_profit_data(y, q)


def get_sse50(year, quarter):
    if os.path.exists('./data/sse50') is False:
        os.makedirs('./data/sse50')
    df = ts.get_sz50s()
    df.to_csv('./data/sse50/sse50_%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter sse50 downloaded.' % (str(year), str(quarter)))


def filter_stock_list_sse50(date):
    sse50 = pd.read_csv('./data/sse50/2017_2.csv', encoding='gbk')
    stock_list = pd.read_csv('./data/stock_basics/20170601.csv', encoding='gbk')
    data = pd.merge(sse50, stock_list, on=['code'], how='left')
    data = data[(data['timeToMarket'] < date)]
    data = data[['code', 'name_x', 'area', 'industry', 'timeToMarket']]
    data = pd.DataFrame(data)
    data = data.fillna({'area': 'miss', 'industry': 'miss'})
    data.to_csv('./data/sse50/2017_2_Filtered.csv')


def stock_master(date):
    sm = pd.DataFrame(pd.read_csv('./data/stock_basics/20170525.csv', encoding='gbk'))
    sm = sm[(sm['timeToMarket'] < date)]
    sm = sm.sort_values(by=['code'], ascending=True)
    print(sm.head(10))
    print(type(sm['code']))
    print(sm['code'])


# 按行业分类股票代号列表
def get_industry_classified():
    if os.path.exists('./data/stock_basics') is False:
        os.makedirs('./data/stock_basics')
    df = ts.get_industry_classified()
    # df.to_csv('./data/stock_basics/industry_classified_%s%s%s.csv' % (str(now.year), str(now.strftime('%m')), str(now.strftime('%d'))))
    # engine = create_engine('mysql+pymysql://york:4466@localhost/apolo?charset=utf8')
    # print(engine)
    engine = connect_engine()
    df.to_sql('industry_classified', engine)
    print('Stock basics - industry classified downloaded.')

if __name__ == '__main__':
    # get_sse50(2017, 2)
    # filter_stock_list_sse50(20120101)
    # get_profit_data_range(2014,2017)
    # get_report_data(2013,1)
    # get_report_data_range(2013, 2017)
    # get_industry_classified()
    get_stock_basics()
    # conn, cur = connect_server()
    # cur.execute("select * from york")
    # result = cur.fetchall()
    # print(result)
    # conn,cur = connect_server()
    # cur.execute("select * from york")
    # result = cur.fetchall()
    # print(result)