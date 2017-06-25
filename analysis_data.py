import pandas as pd
import os
import glob
import numpy as np, matplotlib.pyplot as plt, scipy

def plot_total_asset():
    result = pd.DataFrame(pd.read_csv('./data/600030/fzb_2015_2016.csv', encoding='gbk'))
    result = result['资产总计']
    result = pd.DataFrame(result)
    print(result)
    result.plot(kind='line',title=600030, use_index=True, label=range(10,17,1), grid=True, xticks=range(0,7,1))
    plt.legend('fzb', loc='upper left')
    plt.show()

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
    ttl_asset = pd.DataFrame(pd.read_csv('./data/600030/fzb_2015_2016.csv', encoding='gbk'))
    ttl_asset = ttl_asset[['Unnamed: 0','Unnamed: 1','资产总计']]
    prf_ratio = pd.DataFrame(pd.read_csv('./data/600030/llb_2015_2016.csv', encoding='gbk'))
    prf_ratio = prf_ratio[['Unnamed: 0','Unnamed: 1','净利润']]
    prf_ratio = prf_ratio.fillna(0)
    combined_result = pd.merge(prf_ratio, ttl_asset, on=['Unnamed: 0','Unnamed: 1'], how='left')
    combined_result.insert(4, 'roa', combined_result.loc[:,('净利润')] / combined_result.loc[:, ('资产总计')])
    combined_result = pd.DataFrame(combined_result).drop_duplicates('roa')
    print(combined_result)
    combined_result[['roa']].plot(kind='line',title=600030, use_index=True, grid=True)
    plt.legend('l', loc='upper left')
    plt.show()


# idx = pd.date_range('2015-01-01', periods=8,freq='QS')
# print(idx)

if __name__=='__main__':
    # plot_total_asset()
    # plot_profit_ratio()
    roa()