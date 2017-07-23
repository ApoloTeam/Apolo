import math
import pandas as pd
import os
import glob
import csv
import numpy as np, matplotlib.pyplot as plt, scipy


class Ratios:
    def convert_billion(self, x):
        y = x.split('.')
        y = y[0]
        return y[:-8] # 100,000,000 - billion

    def get_field_data(self, path, field):
        # result = pd.DataFrame(pd.read_csv(path, encoding='gbk', dtype={field: np.float32}))
        result = pd.DataFrame(pd.read_table(path, encoding='gbk', sep=',',dtype={field: np.str}))
        result.rename(columns={'Unnamed: 0': 'year','Unnamed: 1': 'quarter'},inplace=True)
        result = result[['year','quarter', field]]
        result = pd.DataFrame(result)
        result[field] = result[field].apply(self.convert_billion).astype(np.int16)
        # print(result)
        # str = '0123456789'
        # print(str[0:3]) #截取第一位到第三位的字符
        # print(str[:]) #截取字符串的全部字符
        # print(str[6:]) #截取第七个字符到结尾
        # print(str[:-5]) #截取从头开始到倒数第三个字符之前
        # print(str[-1]) #截取倒数第一个字符
        # print(str[::-1]) #创造一个与原字符串顺序相反的字符串
        # print(str[-3:-1]) #截取倒数第三位与倒数第一位之前的字符
        # print(str[-3:]) #截取倒数第三位到结尾
        # print(str[:-5:-3]) #逆序截取，具体啥意思没搞明白？
        return result

    def get_growth_rate(self, dataset):
        rate = round(dataset.query('quarter == 3').pct_change(periods=1)*100, 3)
        return rate

    def display_pivot_table(self, dataset, column):
        result = pd.pivot_table(dataset, index=['year', 'quarter'], values=column)
        result = pd.DataFrame(result)
        result = self.get_growh_rate(result)
        return result

    def get_ann_value(self, dataset):
        # result = self.get_field_data(path, field)
        result = pd.DataFrame(dataset)
        result = result.query('quarter == 3')
        return result

    def liquidity_ratio(self, path, curr_asset, curr_liability):
        curr_assets = self.get_field_data(path, curr_asset)
        curr_liabilities = self.get_field_data(path, curr_liability)
        merged_result = pd.merge(curr_assets, curr_liabilities, on=['year','quarter'], how='inner')
        merged_result.insert(4,'liquidity_ratio', merged_result.loc[:,('流动资产合计')] / \
                             merged_result.loc[:,('流动负债合计')])
        merged_result = pd.DataFrame(merged_result)
        # print(self.display_pivot_table(merged_result, 'liquidity_ratio'))


    def quick_ratio(self, path, curr_asset, curr_liability, inventory):
        curr_assets = self.get_field_data(path, curr_asset)
        curr_liabilities = self.get_field_data(path, curr_liability)
        inventories = self.get_field_data(path, inventory)

        merged_result = pd.merge(curr_assets, curr_liabilities, on=['year','quarter'], how='inner')
        merged_result = pd.merge(merged_result, inventories, on=['year','quarter'], how='inner')
        print(merged_result)
        merged_result.insert(5,'quick_ratio', (merged_result.loc[:,('流动资产合计')] - merged_result.loc[:,('存货')]) / \
                             merged_result.loc[:,('流动负债合计')])
        # print(self.display_pivot_table(merged_result, 'quick_ratio'))

    def cash_ratio(self, path, cash, curr_liability):
        curr_liabilities = self.get_field_data(path, curr_liability)
        cashes = self.get_field_data(path, cash)
        merged_result = pd.merge(cashes, curr_liabilities, on=['year','quarter'], how='inner')
        merged_result.insert(4,'cash_ratio', (merged_result.loc[:,('货币资金（元）')]  / merged_result.loc[:,('流动负债合计')]))
        # print(self.display_pivot_table(merged_result, 'cash_ratio'))


    def operating_income(self, path, from_year, to_year, min_income, max_income):
        oper_income = self.get_field_data(path, '一、营业总收入')
        annual_income = self.display_pivot_table(oper_income, '一、营业总收入')
        min_annual_income = annual_income.min()
        print(min_annual_income)
        if min_annual_income[0] < 0:
            print('one year is negative, ignore the stock.')
        else:
            print('continue')
            print(annual_income)
            for y in np.arange(from_year+1,to_year+1):
                tmp = annual_income.query('year=='+str(y))
                if min_income <= any(tmp) <= max_income:
                    print('%d year is ok' % y)
                else:
                    print('%d year is out of the range, Ignore the stock.' % y)
                    break

    def total_profit(self, path, from_year, to_year):
        ttl_profit = self.get_field_data(path, '四、利润总额')
        annual_ttl_profit = self.display_pivot_table(ttl_profit, '四、利润总额')
        min_annual_ttl_profit = annual_ttl_profit.min()
        print(min_annual_ttl_profit)
        if min_annual_ttl_profit[0] < 0:
            print('one year is %f, negative, ignore the stock.' % min_annual_ttl_profit[0])
        else:
            print(annual_ttl_profit)

    def operating_profit(self, path, from_year, to_year):
        oper_profit = self.get_field_data(path, '三、营业利润')
        annual_oper_profit = self.display_pivot_table(oper_profit, '三、营业利润')
        min_annual_oper_profit = annual_oper_profit.min()
        print(min_annual_oper_profit)
        if min_annual_oper_profit[0] < 0:
            print('one year is %f, negative, ignore the stock.' % min_annual_oper_profit[0])
        else:
            print(annual_oper_profit)

    def total_asset(self, path):
        result = self.get_field_data(path, '资产总计')
        ann_assets = self.display_pivot_table(result, '资产总计')
        min_ann_assets = ann_assets.min()
        print(min_ann_assets)
        if min_ann_assets[0] < 0:
            print('one year is %f, negative, ignore the stock.' % min_ann_assets[0])
        else:
            print(ann_assets)

            # result.plot(kind='line',title=600030, use_index=True, label=range(10,17,1), grid=True, xticks=range(0,7,1))
            # plt.legend('fzb', loc='upper left')
            # plt.show()

    def total_liabilities(self, path):
        result = self.get_field_data(path, '负债合计')
        print(result)
        ann_liabilities = self.display_pivot_table(result, '负债合计')
        print(ann_liabilities)


    def total_equity(self, path):
        result = self.get_field_data(path, '所有者权益（或股东权益）合计')
        print(result)
        ann_equity = self.display_pivot_table(result, '所有者权益（或股东权益）合计')
        print(ann_equity)

    def net_cash_flow_by_oper_activities(self, path, column_name = '经营活动产生的现金流量净额'):
        result = self.get_field_data(path, column_name)
        result.rename(columns={column_name: 'oper'}, inplace=True)
        # result = self.display_pivot_table(result, '经营活动产生的现金流量净额')
        # print(result)
        return result

    def net_cash_flow_by_invest_activities(self, path, column_name = '投资活动产生的现金流量净额'):
        result = self.get_field_data(path, column_name)
        result.rename(columns={column_name: 'inv'}, inplace=True)
        # result = self.display_pivot_table(result, '投资活动产生的现金流量净额')
        return result

    def net_cash_flow_by_fundraising_activities(self, path, column_name = '筹资活动产生的现金流量净额'):
        result = self.get_field_data(path, column_name)
        result.rename(columns={column_name: 'fund'}, inplace=True)
        # result = self.display_pivot_table(result, '筹资活动产生的现金流量净额')
        return result

    def net_cash_flow(self, path, column_name = '五、现金及现金等价物净增加额'):
        result = self.get_field_data(path, column_name)
        result.rename(columns={column_name: 'cash_flow'}, inplace=True)
        # result = self.display_pivot_table(result, '五、现金及现金等价物净增加额')
        return result

    def net_cash_flow_ratio(self):
        pd.set_option('display.precision', 4)
        oper = self.net_cash_flow_by_oper_activities( './data/000338/llb_2014_2016.csv')
        inv = self.net_cash_flow_by_invest_activities( './data/000338/llb_2014_2016.csv')
        fund = self.net_cash_flow_by_fundraising_activities( './data/000338/llb_2014_2016.csv')
        cash_flow = self.net_cash_flow('./data/000338/llb_2014_2016.csv')
        print(type(oper))

        merge_1 = pd.merge(oper, inv, on=['year','quarter'], how='left')
        merge_2 = pd.merge(merge_1, fund, on=['year', 'quarter'], how='left')
        merge_3 = pd.merge(merge_2, cash_flow, on=['year', 'quarter'], how='left')
        merge_3 = merge_3.query('quarter==3')
        # bs_cash_flow = merge_3[['year', 'quarter','oper','inv','fund','ttl']]
        merge_3.insert(3, 'ratio_oper', merge_3.loc[:,('oper')] / merge_3.loc[:, ('cash_flow')])
        merge_3.insert(5, 'ratio_inv', merge_3.loc[:,('inv')] / merge_3.loc[:, ('cash_flow')])
        merge_3.insert(7, 'ratio_fund', merge_3.loc[:,('fund')] / merge_3.loc[:, ('cash_flow')])
        merge_3.insert(9, 'ttl', merge_3.loc[:,('oper')] + merge_3.loc[:, ('inv')] + merge_3.loc[:, ('fund')])
        return merge_3

    def net_profit(self, path):
        result = self.get_field_data(path, '五、净利润')
        result = self.display_pivot_table(result, '五、净利润')
        print(result)
        # result.plot(kind='line',title=600030, use_index=True, label=range(10,17,1), grid=True, xticks=range(0,7,1))
        # plt.legend('l', loc='upper left')
        # plt.show()

    def roe(self):
        prf_ratio = pd.DataFrame(pd.read_csv('./data/000338/lrb_2014_2016.csv', encoding='gbk'))
        prf_ratio = prf_ratio[['Unnamed: 0','Unnamed: 1','五、净利润']]
        ttl_equity = pd.DataFrame(pd.read_csv('./data/000338/fzb_2014_2016.csv', encoding='gbk'))
        ttl_equity = ttl_equity[['Unnamed: 0','Unnamed: 1','所有者权益（或股东权益）合计']]
        combined_result = pd.merge(prf_ratio, ttl_equity, on=['Unnamed: 0','Unnamed: 1'], how='left')
        combined_result.insert(4, 'roe', combined_result.loc[:,('五、净利润')] / combined_result.loc[:, ('所有者权益（或股东权益）合计')])
        # combined_result = pd.DataFrame(combined_result).drop_duplicates('roe')
        print(round(combined_result[['roe']].pct_change()*100, 2))
        print(combined_result)


    def plot(self):
        size = 2014
        t = 3
        result = self.net_cash_flow_ratio()
        oper = result[['year','oper']]
        inv = result[['year','inv']]
        fund = result[['year','fund']]
        oper = oper.iloc[:, 1]
        inv = inv.iloc[:, 1]
        fund = fund.iloc[:, 1]
        date_index = np.arange(size,2017, step=1)
        array_oper = []
        array_inv = []
        array_fund = []
        for year in np.arange(0,3):
            array_oper.append(oper.iloc[year])
            array_inv.append(inv.iloc[year])
            array_fund.append(fund.iloc[year])

        oper = pd.Series(data=array_oper, index=date_index)
        inv = pd.Series(data=array_inv, index=date_index)
        fund = pd.Series(data=array_fund, index=date_index)
        print(result[['year','oper','inv','fund', 'ttl', 'cash_flow']])
        plt.bar(oper.index, array_oper, label='oper')
        plt.bar(inv.index, array_inv, bottom=array_oper, label='inv')
        plt.bar(fund.index, array_fund, bottom=array_inv, label='fund')
        plt.legend()
        plt.show()



def roa():
    ttl_asset = pd.DataFrame(pd.read_csv('./data/000338/fzb_2014_2016.csv', encoding='gbk'))
    ttl_asset = ttl_asset[['Unnamed: 0','Unnamed: 1','资产总计']]
    prf_ratio = pd.DataFrame(pd.read_csv('./data/000338/lrb_2014_2016.csv', encoding='gbk'))
    prf_ratio = prf_ratio[['Unnamed: 0','Unnamed: 1','五、净利润']]
    prf_ratio = prf_ratio.fillna(0)
    combined_result = pd.merge(prf_ratio, ttl_asset, on=['Unnamed: 0','Unnamed: 1'], how='left')
    combined_result.insert(4, 'roa', combined_result.loc[:,('五、净利润')] / combined_result.loc[:, ('资产总计')])
    combined_result = pd.DataFrame(combined_result).drop_duplicates('roa')
    print(combined_result[['roa']])
    # combined_result[['roa']].plot(kind='line',title=600030, use_index=True, grid=True)
    # plt.legend('l', loc='upper left')
    # plt.show()
    print(round(combined_result[['roa']].pct_change()*100, 2))


# idx = pd.date_range('2015-01-01', periods=8,freq='QS')
# print(idx)

if __name__=='__main__':
    # plot_total_asset()
    # plot_profit_ratio()
    # roe()
    test = Ratios()
    # test.liquidity_ratio('./data/000338/fzb_2014_2016.csv','流动资产合计','流动负债合计')
    # test.quick_ratio('./data/000338/fzb_2014_2016.csv','流动资产合计','流动负债合计', '存货')
    # test.cash_ratio('./data/000338/fzb_2014_2016.csv','货币资金（元）','流动负债合计')
    # test.operating_income('./data/000338/lrb_2014_2016.csv', 2014, 2016, 8, 20)
    # test.total_profit('./data/000338/lrb_2014_2016.csv', 2014, 2016)
    # test.operating_profit('./data/000338/lrb_2014_2016.csv', 2014, 2016)
    # test.total_asset('./data/000338/fzb_2014_2016.csv')
    # test.total_liabilities('./data/000338/fzb_2014_2016.csv')
    # test.total_equity('./data/000338/fzb_2014_2016.csv')
    # test.net_cash_flow_by_oper_activities('./data/000338/llb_2014_2016.csv')
    # test.net_cash_flow_by_invest_activities('./data/000338/llb_2014_2016.csv')
    # test.net_cash_flow_by_fundraising_activities('./data/000338/llb_2014_2016.csv')
    # test.net_profit('./data/000338/lrb_2014_2016.csv')
    # test.net_cash_flow('./data/000338/llb_2014_2016.csv')
    test.plot()
    # test.net_cash_flow_ratio()
