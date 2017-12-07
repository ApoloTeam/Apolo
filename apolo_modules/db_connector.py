#encoding:utf-8

#from sqlalchemy import Table,Column,Integer,DECIMAL,String,Date,MetaData,ForeignKey
#from sqlalchemy import select
#from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy import exc
from config import Config
from table_creator import Table_creator
import datetime
import tushare as ts
import pandas as pd
import urllib
from StringIO import StringIO

class Db_connector:
    '''
    This class is used to connect to mysql server and 
    select, insert, delete data 
    '''
    def __init__(self):
        #get the user configuration of db info:
        user_config = Config()
        user_db_param = user_config.get_config_db_info()
        self.db_host = user_db_param['host']
        self.db_port = user_db_param['port']
        self.db_user = user_db_param['user']
        self.db_pass = user_db_param['pass']
        
        
        #create db if not exists
        self.str_db_k_data = 'db_k_data' #k_data database
        self.create_db(self.str_db_k_data)
        
        self.str_db_history_data = 'db_history_data' #history_data database
        self.create_db(self.str_db_history_data)
        
        self.str_db_investment_data= 'db_investment_data' #investment database
        self.create_db(self.str_db_investment_data)
        
        #stock classification database
        self.str_db_stock_classification = 'db_stock_class' #stock classification database
        self.create_db(self.str_db_stock_classification)
        
        #consolidated statement (year) database
        self.str_db_consolidated_statement_year = 'db_consolidated_statement_year'
        self.create_db(self.str_db_consolidated_statement_year)
           
        #create table
        self.table_creator = Table_creator()
        
    def create_db(self,db_name):
        #connect engine
        engine = self.create_db_engine() #the main engin
        #create db if not exists
        engine.execute("create database if not exists %s"%(db_name)) #create database
        print('Create db: '+db_name+' if not exist')
        engine.dispose() #stop all the engine connection
        
    def create_db_engine(self,db_name=''):
        #connect to mysql server
        engine=create_engine('mysql+pymysql://'+self.db_user\
                                 +':'+self.db_pass\
                                 +'@'+self.db_host\
                                 +':'+self.db_port\
                                 +'/'+db_name\
                                 +'?charset=utf8') #use mysqlconnector to connect db
        print("engine:"+db_name+' OK')
        return engine
        
    def insert_to_db_no_duplicate(self,df,table_name,engine,has_index=False):
        
        try:
            df.to_sql(name=table_name,con=engine,if_exists='append',index=has_index)
        except exc.IntegrityError:
            print("Data duplicated, try to insert one by one")
            #df is a dataframe
            num_rows =  len(df)
            #iterate one row at a time
            for i in range(num_rows):
                try:
                    #try inserting the row
                    df[i:i+1].to_sql(name=table_name,con=engine,if_exists='append',index=has_index)
                except exc.IntegrityError:
                    #ignore duplicates
                    pass
        
    def update_db_k_data(self,stock_code):
        
        #create k_data db engine
        engine = self.create_db_engine(self.str_db_k_data)
        
        #set the table name
        table_name = 'k_data_'+stock_code
        table_k_table = self.table_creator.get_table_k_data(table_name) 
        table_k_table.create(engine,checkfirst=True)   #create table
        print("Create k_data table:%s ok!"%(table_name))
        
        #get the start date 
        result = engine.execute("select max(%s) from %s"%(table_k_table.c.date,table_name))
        last_date = result.fetchone()[0]
        if last_date==None:
            start_date = datetime.date(2000,1,1) #default start date
        else:
            start_date=last_date+datetime.timedelta(days=1)
            
        #get the end date
        end_date = datetime.date.today()
        
        if(start_date<end_date):
            str_start_date = start_date.strftime("%Y-%m-%d")
            str_end_date = end_date.strftime("%Y-%m-%d")
        else:
            str_end_date = end_date.strftime("%Y-%m-%d")
            str_start_date = str_end_date
        print('start date:'+str_start_date+' ; end date:'+str_end_date)
        #get the k_data from Tushare
        k_data= ts.get_k_data(code=stock_code,start=str_start_date,end=str_end_date)
        #print(k_data)
        
        #insert data to database
        self.insert_to_db_no_duplicate(k_data,table_k_table.name,engine)
        
        #close the engine pool
        engine.dispose()
        
    def update_stock_list(self):
        
        engine = self.create_db_engine(self.str_db_stock_classification)
        
        #update hs300(沪深300) list:
        table_hs300_list = self.table_creator.get_table_hs300_list()
        table_hs300_list.create(engine,checkfirst=True)
        print("Create %s list table ok!"%table_hs300_list.name)
        #get the list from Tushare
        hs300_list = ts.get_hs300s()
        print('get %s data ok!'%table_hs300_list.name)
        #insert list 
        self.insert_to_db_no_duplicate(hs300_list,table_hs300_list.name,engine)
        print("Insert %s data ok!"%table_hs300_list.name)
        
        #close the engine pool
        engine.dispose()
    
    def update_db_history_data(self,stock_code):
        
        #create db engine
        engine = self.create_db_engine(self.str_db_history_data)
        
        #set the table name
        table_name = 'history_data_'+stock_code
        table_history_table = self.table_creator.get_table_history_data(table_name) 
        table_history_table.create(engine,checkfirst=True)   #create table
        print("Create table:%s ok!"%(table_name))
        
        #get the start date 
        result = engine.execute("select max(%s) from %s"%(table_history_table.c.date,table_name))
        last_date = result.fetchone()[0]
        if last_date==None:
            start_date = datetime.date(2000,1,1) #default start date
        else:
            start_date=last_date+datetime.timedelta(days=1)
            
        #get the end date
        end_date = datetime.date.today()
        
        if(start_date<end_date):
            str_start_date = start_date.strftime("%Y-%m-%d")
            str_end_date = end_date.strftime("%Y-%m-%d")
        else:
            str_end_date = end_date.strftime("%Y-%m-%d")
            str_start_date = str_end_date
        print('start date:'+str_start_date+' ; end date:'+str_end_date)
        #get the history data from Tushare
        history_data= ts.get_hist_data(code=stock_code,start=str_start_date,end=str_end_date)
        #print(history_data)
        
        #insert data to database
        self.insert_to_db_no_duplicate(history_data,table_history_table.name,engine,has_index=True)
        
        #close the engine pool
        engine.dispose()
     
    def update_db_dividend_data(self):
        
        #create db engine
        engine = self.create_db_engine(self.str_db_investment_data)
        
        #set the table name
        table_dividend_data= self.table_creator.get_table_dividend_data() 
        table_dividend_data.create(engine,checkfirst=True)   #create table
        print("Create table:%s ok!"%(table_dividend_data.name))
        
        #get the start date 
        result = engine.execute("select max(%s) from %s"%(table_dividend_data.c.year,table_dividend_data.name))
        last_year= result.fetchone()[0]
        if last_year==None:
            start_year= 2005 
        else:
            start_year= last_year+1
            
        #get the end year
        end_year= datetime.datetime.now().year
        
        if(start_year>=end_year):
            start_year = end_year
        print('start year:'+str(start_year)+' ; end year:'+str(end_year))
        #get the profit data
        for n in range(start_year,end_year):
            dividend_data = ts.profit_data(year=n,top=4000)
            print("Dividend data at year:%s"%n)
            #print(dividend_data)
            #insert data to database
            self.insert_to_db_no_duplicate(dividend_data,table_dividend_data.name, engine)
        
        #close the engine pool
        engine.dispose()
        
        
    def update_db_consolidated_statement_year_data(self,stock_num):
        
        #create db engine
        engine = self.create_db_engine(self.str_db_consolidated_statement_year)
        
        #set the table name
        table_name = 'stock_'+str(stock_num)
        table_consolidated_statement_year= self.table_creator.get_consolidated_statement_year(table_name) 
        table_consolidated_statement_year.create(engine,checkfirst=True)   #create table
        print("Create table:%s ok!"%(table_consolidated_statement_year.name))
        
        #get data from website(网易财经)
        url_txt = "http://quotes.money.163.com/service/zcfzb_"+str(stock_num)+".html?type=year"
        webPage =  urllib.urlopen(url_txt)
        statement_data = webPage.read().decode('gbk')
        webPage.close()
        statement_File = StringIO(statement_data)
        statement_list_tmp = pd.read_csv(statement_File).T
        statement_list = statement_list_tmp.dropna(axis=0)
        statement_list.columns = statement_list_tmp.ix[0]
        statement_list = statement_list.drop('报告日期')
        statement_list = statement_list.replace('--',0,regex=True)
        statement_list.index.name = '报告日期'
        
        self.insert_to_db_no_duplicate(statement_list,table_name, engine,True)
        print(statement_list)        
        
        ##get the start date 
        #result = engine.execute("select max(%s) from %s"%(table_dividend_data.c.year,table_dividend_data.name))
        #last_year= result.fetchone()[0]
        #if last_year==None:
            #start_year= 2005 
        #else:
            #start_year= last_year+1
            
        ##get the end year
        #end_year= datetime.datetime.now().year
        
        #if(start_year>=end_year):
            #start_year = end_year
        #print('start year:'+str(start_year)+' ; end year:'+str(end_year))
        ##get the profit data
        #for n in range(start_year,end_year):
            #dividend_data = ts.profit_data(year=n,top=4000)
            #print("Dividend data at year:%s"%n)
            ##print(dividend_data)
            ##insert data to database
            #self.insert_to_db_no_duplicate(dividend_data,table_dividend_data.name, engine)
        
        #close the engine pool
        engine.dispose()
 #-------------------------------------------------------------------------------------------  
    def get_table_data(self,db_name,table_name,select_column=None):
        '''
        get the table data
        '''
        engine = self.create_db_engine(db_name)
        result = pd.read_sql_table(table_name,engine,columns=select_column)
        engine.dispose()
        return result
    
    #def select_table_data(self,db_name):
        #engine = self.create_db_engine(db_name)
    
if __name__=='__main__':
    test=Db_connector()
    #test.update_db_k_data('000002')
    #test.update_db_history_data('000002')
    #test.update_stock_list()
    
    ##get hs300 list
    #hs300_list_table = test.table_creator.get_table_hs300_list()
    #hs300_list_code = test.get_table_data(test.str_db_stock_classification,hs300_list_table.name,
                                          #[hs300_list_table.c.code.name])
    #print(hs300_list_code)
    
    #for record in hs300_list_code[hs300_list_table.c.code.name]:
        #test.update_db_history_data(record)
        #print("update :%s OK"%record)
        
    ##update the profit data    
    #test.update_db_dividend_data()
    
    #test the consolidated statement year data
    test.update_db_consolidated_statement_year_data('000002')
    
    
    print("Complete ok")
    