import pandas as pd
import os
import glob
import numpy as np, matplotlib.pyplot as plt, scipy


class Ratios:
    def get_field_data(self, path, field):
        result = pd.DataFrame(pd.read_csv(path, encoding='gbk'))
        result = result[['Unnamed: 0','Unnamed: 1', field]]
        return result

    def liquidity_ratio(self, path, curr_assets, curr_liability):
        curr_assets = self.get_field_data(path, curr_assets)
        curr_liabilities = self.get_field_data(path, curr_liability)
        print(curr_liabilities[['Unnamed: 0']])
        merged_result = pd.merge(curr_assets, curr_liabilities, on=['Unnamed: 0','Unnamed: 1'], how='inner')
        merged_result.insert(4,'liquidity_ratio', merged_result.loc[:,('流动资产合计')] / merged_result.loc[:,('流动负债合计')])
        merged_result = pd.DataFrame(merged_result)
        print(merged_result.sort_values(by=['Unnamed: 1']))


    def plot_total_asset(self, path, assets):
        result = self.get_field_data(path, assets)
        result = result['资产总计']
        result = pd.DataFrame(result)
        # print(result)
        # result.plot(kind='line',title=600030, use_index=True, label=range(10,17,1), grid=True, xticks=range(0,7,1))
        # plt.legend('fzb', loc='upper left')
        # plt.show()

def plot_profit_ratio():
    result = pd.DataFrame(pd.read_csv('./data/600030/llb_2015_2016.csv', encoding='gbk'))
    result = result['净利润']
    result = result.fillna(0)
    result = pd.DataFrame(result.drop_duplicates(result[0]))
    print(result)
    # result.plot(kind='line',title=600030, use_index=True, label=range(10,17,1), grid=True, xticks=range(0,7,1))
    # plt.legend('l', loc='upper left')
    # plt.show()

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

def roe():
    prf_ratio = pd.DataFrame(pd.read_csv('./data/000338/lrb_2014_2016.csv', encoding='gbk'))
    prf_ratio = prf_ratio[['Unnamed: 0','Unnamed: 1','五、净利润']]
    ttl_equity = pd.DataFrame(pd.read_csv('./data/000338/fzb_2014_2016.csv', encoding='gbk'))
    ttl_equity = ttl_equity[['Unnamed: 0','Unnamed: 1','所有者权益（或股东权益）合计']]
    combined_result = pd.merge(prf_ratio, ttl_equity, on=['Unnamed: 0','Unnamed: 1'], how='left')
    combined_result.insert(4, 'roe', combined_result.loc[:,('五、净利润')] / combined_result.loc[:, ('所有者权益（或股东权益）合计')])
    # combined_result = pd.DataFrame(combined_result).drop_duplicates('roe')
    print(round(combined_result[['roe']].pct_change()*100, 2))
    print(combined_result)


# idx = pd.date_range('2015-01-01', periods=8,freq='QS')
# print(idx)

if __name__=='__main__':
    # plot_total_asset()
    # plot_profit_ratio()
    # roe()
    test = Ratios()
    test.liquidity_ratio('./data/000338/fzb_2014_2016.csv','流动资产合计','流动负债合计')
