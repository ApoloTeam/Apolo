import pandas as pd
import os
import glob
import numpy as np, matplotlib.pyplot as plt, scipy


class Ratios:
    def get_field_data(self, path, field):
        result = pd.DataFrame(pd.read_csv(path, encoding='gbk'))
        result.rename(columns={'Unnamed: 0': 'year','Unnamed: 1': 'quarter'},inplace=True)
        result = result[['year','quarter', field]]
        result = pd.DataFrame(result)
        return result

    def display_pivot_table(self, dataset, column):
        result = pd.pivot_table(dataset, index=['year', 'quarter'], values=column)
        result = pd.DataFrame(result)
        result = round(result.query('quarter == 3').pct_change(periods=1)*100, 3)
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




    def plot_total_asset(self, path, assets):
        result = self.get_field_data(path, assets)
        result = result['资产总计']
        result = pd.DataFrame(result)
        # print(result)
        # result.plot(kind='line',title=600030, use_index=True, label=range(10,17,1), grid=True, xticks=range(0,7,1))
        # plt.legend('fzb', loc='upper left')
        # plt.show()

    def plot_profit_ratio(self):
        result = pd.DataFrame(pd.read_csv('./data/600030/llb_2015_2016.csv', encoding='gbk'))
        result = result['净利润']
        result = result.fillna(0)
        result = pd.DataFrame(result.drop_duplicates(result[0]))
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
    test.total_profit('./data/000338/lrb_2014_2016.csv', 2014, 2016)
