import os
import pandas as pd
import numpy as np
import datetime as dt
import tushare as ts
from sqlalchemy.exc import IntegrityError
from modules.connect_database import ConnectDatabase
ts_new = ts.pro_api('0186b390ef6be64b54a89f4a23b31d97c44eac0a3acad8b40940c302')

connection = ConnectDatabase()
conn, cur = connection.connect_server()
now = dt.datetime.now()
DATA_DIR = 'E:\\Apolo\\raw_data'
STOCK_BASICS_DIR = os.path.join(DATA_DIR, 'stock_basics')
REPORT_DATA_DIR = os.path.join(DATA_DIR, 'report_data')
PROFIT_DATA_DIR = os.path.join(DATA_DIR, 'profit_data')
INDUSTRY_CLASSIFIED_DIR = os.path.join(DATA_DIR, 'industry_classified')
HISTORY_DATA_DIR = os.path.join(DATA_DIR, 'history_data')
STOCK_ID_DIR = os.path.join(DATA_DIR, 'stock_id')
DIVIDEND_PLAN_DIR = os.path.join(DATA_DIR, 'dividend_plan')
FUND_HOLDINGS_DIR = os.path.join(DATA_DIR, 'fund_holdings')


# 获取沪深上市公司基本情况

def get_stock_basics():
    # if folder doest exists, then create.
    # todo: check if the data is the latest, no need to insert, otherwise insert or update.
    # todo: Exception
    try:
        if os.path.exists(STOCK_BASICS_DIR) is False:
            os.makedirs(STOCK_BASICS_DIR)
        df = ts.get_stock_basics()
        df['createDate'] = '{yyyy}{mm}{dd}'.format(yyyy=str(now.year),
                                                   mm=str(now.strftime('%m')),
                                                   dd=str(now.strftime('%d')))
        df.to_csv(os.path.join(STOCK_BASICS_DIR, '%s%s%s.csv' % (str(now.year),
                                                                 str(now.strftime('%m')),
                                                                 str(now.strftime('%d')))))
        engine = connection.create_db_engine()
        df.to_sql('stock_basics', engine, if_exists='append', index=True)  # append, to avoid modifying field type.
    except IntegrityError as error:
        print(error)
    else:
        print('Success: Stock basics downloaded.')


# 获取某年某季度的业绩报表数据

def get_report_data(year, quarter):
    # todo: to check if the result exist, don't download.
    try:
        if os.path.exists(REPORT_DATA_DIR) is False:
            os.makedirs(REPORT_DATA_DIR)
        df = ts.get_report_data(year, quarter)
        df['report_y_q'] = int('{yyyy}{q}'.format(yyyy=year, q=quarter))
        df = df.iloc[:, 0: 12]
        df.to_csv(os.path.join(REPORT_DATA_DIR, '%s_%s.csv' % (str(year), str(quarter))))
        engine = connection.create_db_engine()
        pd.DataFrame.to_sql(df, 'report_data', engine, if_exists='append', index=False)
    except IntegrityError as error:
        print(error)
    else:
        print('\nSuccess: %s year %s quarter report data report downloaded.' % (str(year), str(quarter)))


def get_report_data_range(from_year, to_year):
    for y in np.arange(from_year, to_year+1):
        for q in np.arange(1, 4+1):
            get_report_data(y, q)


# 获取某年某季度的盈利能力数据

def get_profit_data(year, quarter):
    try:
        if os.path.exists(PROFIT_DATA_DIR) is False:
            os.makedirs(PROFIT_DATA_DIR)
        df = ts.get_profit_data(year, quarter)
        df['report_y_q'] = int('{yyyy}{q}'.format(yyyy=year, q=quarter))
        df.to_csv(os.path.join(PROFIT_DATA_DIR, '%s_%s.csv' % (str(year), str(quarter))))
        engine = connection.create_db_engine()
        pd.DataFrame.to_sql(df, 'profit_data', engine, if_exists='append', index=False)
    except IntegrityError as error:
        print(error)
    else:
        print('\nSuccess: %s year %s quarter profit data report downloaded.' % (str(year), str(quarter)))


def get_profit_data_range(from_year, to_year):
    for y in np.arange(from_year, to_year+1):
        for q in np.arange(1, 4+1):
            get_profit_data(y, q)


def get_data_by_year(func):
    def wrap(from_year):
        for y in np.arange(from_year, now.year + 1):
            for q in np.arange(1, 4 + 1):
                func(y, q)
    return wrap

# 按行业分类股票代号列表

def get_industry_classified():
    try:
        if os.path.exists(INDUSTRY_CLASSIFIED_DIR) is False:
            os.makedirs(INDUSTRY_CLASSIFIED_DIR)
        df = ts.get_industry_classified()
        df.to_csv(os.path.join(INDUSTRY_CLASSIFIED_DIR, '%s%s%s.csv' % (str(now.year),
                                                                        str(now.strftime('%m')),
                                                                        str(now.strftime('%d')))))
        df['createDate'] = '{yyyy}{mm}{dd}'.format(yyyy=str(now.year),
                                                   mm=str(now.strftime('%m')),
                                                   dd=str(now.strftime('%d')))
        engine = connection.create_db_engine()
        df.to_sql('industry_classified', engine, if_exists='append', index=False)
    except IntegrityError as error:
        print(error)
    else:
        print('Success: Stock basics - industry classified downloaded.')

def get_dividend_plan(year, top=3000):
    try:
        if os.path.exists(DIVIDEND_PLAN_DIR) is False:
            os.makedirs(DIVIDEND_PLAN_DIR)
        df = ts.profit_data(year, top)
        df.to_csv(os.path.join(DIVIDEND_PLAN_DIR, '{yyyy}.csv'.format(yyyy=year)))
        # df['createDate'] = '{yyyy}{mm}{dd}'.format(yyyy=str(now.year),
        #                                            mm=str(now.strftime('%m')),
        #                                            dd=str(now.strftime('%d')))
        engine = connection.create_db_engine()
        df.to_sql('dividend_plan', engine, if_exists='append', index=False)
    except IntegrityError as error:
        print(error)
    else:
        print('Success: {yyyy} year dividend_plan downloaded.'.format(yyyy=year))


# ----- SSE top 50 -----
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


# ----- list of code with date range -----
def stock_master(date):
    sm = pd.DataFrame(pd.read_csv('./data/stock_basics/20170525.csv', encoding='gbk'))
    sm = sm[(sm['timeToMarket'] < date)]
    sm = sm.sort_values(by=['code'], ascending=True)
    print(sm['code'])


# ----- Below function use code to search -----
def query_stock_code(stock_code, to_year=2017, total_year=5):
    cur.execute("select count(code) from stock_code where code=%s", stock_code)
    exist = cur.fetchall()
    if exist[0][0]:
        print('The stock code exist already.')
    else:
        print('The stock code do NOT exist. Start to download data...')
        cur.execute("insert into stock_code (code) values (%s)", stock_code)
        get_history_data(str(stock_code).zfill(6), to_year, total_year)

    conn.commit()


# todo: update data


def query_industry(industry, to_year=2017, total_year=5):
    cur.execute("select * from industry_classified where c_name=\'{i}\'".format(i=industry))
    list_stock_codes = cur.fetchall()
    for code in list_stock_codes:
        print(code[0])
        query_stock_code(code[0], to_year, total_year)
    print('Done')


def query_stock_basics(stock_code, field):
    cur.execute("select {f} from stock_basics where code={code}".format(f=field, code=stock_code))
    f = cur.fetchall()
    return f[0][0]


def query_timeToMarket(stock_code):
    timeToMarket = query_stock_basics(stock_code, field='timeToMarket')
    # print(round(year/10000))  # to take year because data type is int
    return timeToMarket


def get_stock_info(stock_code):
    cur.execute("select * from stock_basics where code={code}".format(code = stock_code))
    f = cur.fetchall()
    print(f)
    return f

# todo: if total of year exceed 5 years, data


def get_history_data(code, to_year, total_year):
    engine = connection.create_db_engine()
    path = os.path.join(HISTORY_DATA_DIR, code)
    if os.path.exists(path) is False:
        os.makedirs(path)

    start_year = '{yyyy}{mm}{dd}'.format(yyyy=to_year - total_year, mm='01', dd='01')
    start_year_ = '{yyyy}-{mm}-{dd}'.format(yyyy=to_year - total_year, mm='01', dd='01')
    timeToMarket = query_timeToMarket(code)
    if int(start_year) <= timeToMarket:
        from_year = str(timeToMarket)
        from_year = ('{yyyy}-{mm}-{dd}'.format(yyyy=from_year[0:4],
                                                 mm=from_year[4:6],
                                                 dd=from_year[6:8]))
    else:
        from_year = start_year_

    try:
        print('Start to download from year {from_year}'.format(from_year=from_year))
        start = from_year
        end = '{yyyy}-12-31'.format(yyyy=from_year[0:4])
        df = ts.get_k_data(code, autype='qfq', start=start, end=end)
        df.to_csv(os.path.join(path, '{f}_{t}.csv'.format(f=start, t=from_year[0:4])))
        df.to_sql('history_data', engine, if_exists='append', index=False)
        print('-- completed.')

        for y in np.arange(int(from_year[0:4])+1, to_year, 1):
            print('Start to download {yyyy}'.format(yyyy=y))
            start = '{yyyy}-01-01'.format(yyyy=y)
            end = '{yyyy}-12-31'.format(yyyy=y)
            df = ts.get_k_data(code, autype='qfq', start=start, end=end)
            df.to_csv(os.path.join(path, '{yyyy}.csv'.format(yyyy=y)))
            df.to_sql('history_data', engine, if_exists='append', index=False)
            print('-- completed.')

        print('Start to download {yyyy}'.format(yyyy=to_year))
        start = '{yyyy}-01-01'.format(yyyy=to_year)
        end = str(dt.date.today())
        df = ts.get_k_data(code, autype='qfq', start=start, end=end)
        df.to_csv(os.path.join(path, '{f}_{t}.csv'.format(f=to_year, t=end)))
        df.to_sql('history_data', engine, if_exists='append', index=False)
        print('-- completed.')

    except IntegrityError as error:
        print(error)
    except:
        print("Error")

# ----- 获取每个季度基金持有上市公司股票的数据 -----
def get_fund_holdings(year, quarter):
    try:
        if os.path.exists(FUND_HOLDINGS_DIR) is False:
            os.makedirs(FUND_HOLDINGS_DIR)
        df = ts.fund_holdings(year, quarter)
        df.to_csv(os.path.join(DIVIDEND_PLAN_DIR, '{yyyy}_{q}.csv'.format(yyyy=year, q=quarter)))
        engine = connection.create_db_engine()
        df.to_sql('fund_holdings', engine, if_exists='append', index=False)
    except IntegrityError as error:
        print(error)
    else:
        print('Success: {yyyy} year {q} quarter fund_holdings downloaded.'.format(yyyy=year, q=quarter))


if __name__ == '__main__':
    get_fund_holdings(2018,3)
    # df = ts.get_k_data("000156", autype='qfq', start='2012-01-01', end='2012-03-31')
    # print(df)
    # conn.close()
    # get_stock_info('000002')
