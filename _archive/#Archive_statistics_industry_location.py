# -*- coding:utf-8 -*-
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# reload(sys)
# sys.setdefaultencoding("utf-8")  # Set system default encoding as UTF-8
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
sns.set_style("darkgrid", {"font.sans-serif":['simhei', 'Arial']})

stock_list = pd.DataFrame(pd.read_csv('./data/stock_basics/20170601.csv', encoding='gbk'))
count_industry = stock_list['industry'].value_counts()
# print(type(count_industry))
industry = pd.DataFrame(count_industry, index=None)
# print(type(industry))
# industry.plot.pie(subplots=True, table=True, figsize=(6, 6),title='abc')
# plt.pie(count_industry)


count_location = stock_list['area'].value_counts()
area = pd.DataFrame(count_location, index=None)
area.plot.pie(subplots=True, table=False, figsize=(6, 6), title='location', labels=stock_list['area'].tolist(),)
# print(area['area'])
# print(area.get_values())
location = stock_list['area'].get_values()
# print(stock_list['area'].duplicated)
location = pd.DataFrame(location)
print(location.duplicated)
# print(location[0].drop_duplicates[0])
print(type(location))
# print(type(stock_list['area'].tolist()))


# plt.show()
# stock_list.plot.pie(subplots=True, table=True, figsize=(6, 6), title='abc')
# all_price = pd.DataFrame(count_price, index=None)
# plt_price.plot.bar()  # plt_price.plot(kind='bar')
# all_price.plot.pie(subplots=True, table=True, figsize=(6, 6),title='abc', legend=True, labels=['<1000', '>=1000'])
# figsize is the size of shape
# legend is to display legend on subplot
# table is to use passed data from DataFrame to draw a table