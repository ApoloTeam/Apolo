import tushare as ts
import os
import datetime
import pandas as pd

print('version: ' + ts.__version__)
now = datetime.datetime.now()
# print(now.strftime('%Y''%m''%d'))


# 获取沪深上市公司基本情况
def get_stock_basics():
    # if folder doest exists, then create.
    if os.path.exists('./data/stock_basics') is False:
        os.makedirs('./data/stock_basics')
    df = ts.get_stock_basics()
    df.to_csv('./data/stock_basics/%s%s%s.csv' % (str(now.year), str(now.strftime('%m')), str(now.strftime('%d'))))
    print('Stock basics downloaded.')


# 获取某年某季度的业绩报表数据
def get_report_data(year, quarter):
    if os.path.exists('./data/report_data') is False:
        os.makedirs('./data/report_data')
    df = ts.get_report_data(year, quarter)
    df.to_csv('./data/report_data/%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter report data report downloaded.' % (str(year), str(quarter)))


# 获取某年某季度的盈利能力数据
def get_profit_data(year, quarter):
    if os.path.exists('./data/profit_data') is False:
        os.makedirs('./data/profit_data')
    df = ts.get_profit_data(year, quarter)
    df.to_csv('./data/profit_data/%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter profit data report downloaded.' % (str(year), str(quarter)))


# 获取某年某季度的营运能力数据
def get_operation_data(year, quarter):
    if os.path.exists('./data/operation_data') is False:
        os.makedirs('./data/operation_data')
    df = ts.get_operation_data(year, quarter)
    df.to_csv('./data/operation_data/%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter operation data report downloaded.' % (str(year), str(quarter)))


# 获取某年某季度的成长能力数据
def get_growth_data(year, quarter):
    if os.path.exists('./data/growth_data') is False:
        os.makedirs('./data/growth_data')
    df = ts.get_growth_data(year, quarter)
    df.to_csv('./data/growth_data/%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter growth data report downloaded.' % (str(year), str(quarter)))


# 获取某年某季度的偿债能力数据
def get_debtpaying_data(year, quarter):
    if os.path.exists('./data/debtpaying_data') is False:
        os.makedirs('./data/debtpaying_data')
    df = ts.get_debtpaying_data(year, quarter)
    df.to_csv('./data/debtpaying_data/%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter debtpaying data report downloaded.' % (str(year), str(quarter)))


# 获取某年某季度的现金流量数据
def get_cashflow_data(year, quarter):
    if os.path.exists('./data/cashflow_data') is False:
        os.makedirs('./data/cashflow_data')
    df = ts.get_cashflow_data(year, quarter)
    df.to_csv('./data/cashflow_data/%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter cashflow data report downloaded.' % (str(year), str(quarter)))


def get_sse50(year, quarter):
    if os.path.exists('./data/sse50') is False:
        os.makedirs('./data/sse50')
    df = ts.get_sz50s()
    df.to_csv('./data/sse50/%s_%s.csv' % (str(year), str(quarter)))
    print('\n%s year %s quarter sse50 downloaded.' % (str(year), str(quarter)))


# 获取某年某季度的所有数据
def get_data(year, quarter):
    get_stock_basics()
    get_report_data(year, quarter)
    get_profit_data(year, quarter)
    get_operation_data(year, quarter)
    get_growth_data(year, quarter)
    get_debtpaying_data(year, quarter)
    get_cashflow_data(year, quarter)


def stock_master(date):
    sm = pd.DataFrame(pd.read_csv('./data/stock_basics/20170525.csv', encoding='gbk'))
    sm = sm[(sm['timeToMarket'] < date)]
    sm = sm.sort_values(by=['code'], ascending=True)
    print(sm.head(10))
    print(type(sm['code']))
    print(sm['code'])

    # print(sm.head(10))


if __name__ == '__main__':
    # get_report_data(2016, 1)
    # get_report_data(2016, 2)
    # get_report_data(2016, 3)
    # get_report_data(2016, 4)
    # get_stock_basics()
    # stock_master(20120101)
    # print('\nTesting')
    get_sse50(2017, 2)

