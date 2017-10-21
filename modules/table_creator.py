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
        