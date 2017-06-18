import csv as csv
import numpy as np
import pandas as pd

# df = pd.read_csv('./data/stock_basics/20170430.csv', encoding='gbk')
#
# print(df.head())
# print('---------------')
# print(df[['code', 'area']])
# dd = pd.read_csv('./data/report_data/2016_4.csv', encoding='gbk')
# print(dd.head())
# print('---------------')
# print(dd[['code', 'eps']])
#
# data = pd.merge(df, dd, on=['code'], how='left')
# data = data[['code', 'area', 'eps']]
# data = pd.DataFrame(data)
# data.to_csv('./merge/test.csv')


def balance_sheet():
    stock_basics = pd.read_csv('./data/stock_basics/20170430.csv', encoding='gbk')
    # Type is float64

    cashflow = pd.read_csv('./data/cashflow_data/2016_4.csv', encoding='gbk')
    # Type is float64

    debtpaying = pd.read_csv('./data/debtpaying_data/2016_4.csv', encoding='gbk')
    # print(type(currentratio['currentratio'][0])) #  Type is string, need to fix later.

    growth = pd.read_csv('./data/growth_data/2016_4.csv', encoding='gbk')
    # Type is float64

    operation = pd.read_csv('./data/operation_data/2016_4.csv', encoding='gbk')
    # Type is float64

    profit = pd.read_csv('./data/profit_data/2016_4.csv', encoding='gbk')
    # Type is float64

    report = pd.read_csv('./data/report_data/2016_4.csv', encoding='gbk')
    # Type is float64

    data = pd.merge(stock_basics, cashflow, on=['code'], how='left')
    data = pd.merge(data, debtpaying, on=['code'], how='left')
    data = pd.merge(data, growth, on=['code'], how='left')
    data = pd.merge(data, operation, on=['code'], how='left')
    data = pd.merge(data, profit, on=['code'], how='left')
    data = pd.merge(data, report, on=['code'], how='left')


    # data = data[['code', 'outstanding', 'totals', 'totalAssets', 'liquidAssets', 'fixedAssets',
    #              'eps','bvps','roe','net_profits','currentratio', 'arturnover', 'arturndays',
    #            'inventory_turnover','inventory_days','currentasset_turnover','currentasset_days',
    #           'quickratio','cashratio','cf_nm','cf_sales']]

    # data['liquidLiabilities'] = data['liquidAssets'] / data['currentratio']
    # data.to_csv('./merge/test.csv')

def net_assets():  # Same as stockholder equity
    # report = pd.read_csv('./data/report_data/2016_4.csv', encoding='gbk')
    stock_basics = pd.read_csv('./data/stock_basics/20170430.csv', encoding='gbk')
    # data = pd.merge(stock_basics, report, on=['code'], how='left')
    data = stock_basics[['code', 'bvps', 'totals']]
    data.insert(3, 'net_assets', data.loc[:,('bvps')] * data.loc[:, ('totals')])
    print(data.head())
    return data


def liquid_liabilities():
    debtpaying = pd.read_csv('./data/debtpaying_data/2016_4.csv', encoding='gbk')
    print(type(debtpaying['currentratio'][0]))


def operating_cash_flow():
    cashflow = pd.read_csv('./data/cashflow_data/2016_4.csv', encoding='gbk')
    stock_basics = pd.read_csv('./data/stock_basics/20170430.csv', encoding='gbk')
    data = pd.merge(stock_basics, cashflow, on=['code'], how='left')
    data = data[['code', 'totalAssets', 'rateofreturn']]
    data.insert(3, 'oper_cash_flow', data.loc[:,('totalAssets')] * data.loc[:, ('rateofreturn')]*10000)
    # print(data.head())
    data.to_csv('./merge/oper_cash_flow.csv')


def operating_cash_flow_2():
    cashflow = pd.read_csv('./data/cashflow_data/2016_4.csv', encoding='gbk')
    profits = pd.read_csv('./data/profit_data/2016_4.csv', encoding='gbk')
    data = pd.merge(profits, cashflow, on=['code'], how='left')
    data = data[['code', 'net_profits', 'cf_nm']]
    data.insert(3, 'oper_cash_flow', data.loc[:,('net_profits')] * 100 * data.loc[:, ('cf_nm')])
    # print(data.head())
    data.to_csv('./merge/oper_cash_flow_2.csv')


def operating_cash_flow_3():
    cashflow = pd.read_csv('./data/cashflow_data/2016_4.csv', encoding='gbk')
    profits = pd.read_csv('./data/profit_data/2016_4.csv', encoding='gbk')
    data = pd.merge(profits, cashflow, on=['code'], how='left')
    data = data[['code', 'business_income', 'cf_sales']]
    data.insert(3, 'oper_cash_flow', data.loc[:,('business_income')] * data.loc[:, ('cf_sales')])
    # print(data.head())
    data.to_csv('./merge/oper_cash_flow_3.csv')


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
    # balance_sheet()
    # net_assets()
    # liquid_liabilities()
    # operating_cash_flow()
    # operating_cash_flow_2()
    # operating_cash_flow_3()
    filter_stock_list_sse50(20120101)
