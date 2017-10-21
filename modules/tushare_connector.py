#encoding:utf-8
import tushare as ts
import os
import pandas as pd
import numpy as np

class Tushar_connector:
    '''
    This class is for user to use the Tushare api to get the stock data from internet
    '''
    def get_k_data(self,code,start,end,ktype,autype,index=False):
        '''
        获取日周月的低频数据，也可以获取5、15、30和60分钟相对高频的数据。
        同时，上市以来的前后复权数据也能在一行代码中轻松获得，当然，您也可以选择不复权。
        \n输入参数说明:
        \n- code:证券代码：支持沪深A、B股 支持全部指数 支持ETF基金
        \n- ktype:数据类型：默认为D日线数据 D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟
        \n- autype:复权类型：qfq-前复权 hfq-后复权 None-不复权，默认为qfq
        \n- index:是否为指数：默认为False 设定为True时认为code为指数代码
        \n- start:开始日期  format：YYYY-MM-DD 为空时取当前日
        \n- end: 结束日期 ：format：YYYY-MM-DD 
        
        \n输出说明:
        \n- date:日期和时间 低频数据时为：YYYY-MM-DD 高频数为：YYYY-MM-DD HH:MM
        \n- open:开盘价
        \n- close:收盘价
        \n- high:最高价
        \n- low:最低价
        \n- volumn:成交量
        \n- code:证券代码
        '''        
        data = ts.get_k_data()