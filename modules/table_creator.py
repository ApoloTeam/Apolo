#encoding:utf-8

from sqlalchemy import Table,Column,Integer,DECIMAL,String,Date,MetaData,ForeignKey

class Table_creator:
    '''
    This class is for user to customize the tables
    '''
    metadata = MetaData()
    
    def get_table_k_data(self,table_name):
        table_k_data = Table(table_name,self.metadata,
            Column('date',Date(),primary_key=True),     #时间和日期 低频数据时为：YYYY-MM-DD 高频数为：YYYY-MM-DD HH:MM
            Column('open',DECIMAL(10,4)),  #开盘价
            Column('close',DECIMAL(10,4)), #收盘价
            Column('high',DECIMAL(10,4)),  #最高价
            Column('low',DECIMAL(10,4)),   #最低价
            Column('volume',DECIMAL(20,4)),#成交量
            Column('code',String(100))    #证券代码
            )
        return table_k_data
    
    #历史数据
    def get_table_history_data(self,table_name):
        table_history_data = Table(table_name,self.metadata,
            Column('date',Date(),primary_key=True),     #时间和日期 低频数据时为：YYYY-MM-DD 高频数为：YYYY-MM-DD HH:MM
            Column('open',DECIMAL(10,4)),  #开盘价
            Column('high',DECIMAL(10,4)),  #最高价
            Column('close',DECIMAL(10,4)), #收盘价
            Column('low',DECIMAL(10,4)),   #最低价
            Column('volume',DECIMAL(20,4)),#成交量
            Column('price_change',DECIMAL(20,4)),#价格变动
            Column('p_change',DECIMAL(20,4)),#涨跌幅
            Column('ma5',DECIMAL(20,4)),#5日均价
            Column('ma10',DECIMAL(20,4)),#10日均价
            Column('ma20',DECIMAL(20,4)),#20日均价
            Column('v_ma5',DECIMAL(20,4)),#5日均量
            Column('v_ma10',DECIMAL(20,4)),#10日均量
            Column('v_ma20',DECIMAL(20,4)),#20日均量
            Column('turnover',DECIMAL(20,4)),#换手率
            )
        return table_history_data
                
    #上证50
    def get_table_sz50_list(self):
        table_sz50_list = Table('sz50_list',self.metadata,
                              Column('code',String(100),primary_key=True),
                              Column('name',String(100))
                              )
        return table_sz50_list
    
    #中证500
    def get_table_zz500_list(self):
        table_zz500_list = Table('zz500_list',self.metadata,
                              Column('code',String(100),primary_key=True),
                              Column('name',String(100)),
                              Column('date',Date()),
                              Column('weight',DECIMAL(10,4))
                              )
        return table_zz500_list
    
    #沪深300
    def get_table_hs300_list(self):
        table_hs300_list = Table('hs300_list',self.metadata,
                              Column('code',String(100),primary_key=True),
                              Column('name',String(100)),
                              Column('date',Date()),
                              Column('weight',DECIMAL(10,4))
                              )
        return table_hs300_list