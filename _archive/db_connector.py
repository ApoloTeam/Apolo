#encoding:utf-8

#from sqlalchemy import Table,Column,Integer,DECIMAL,String,Date,MetaData,ForeignKey
#from sqlalchemy import select
#from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy import exc
#from config import Config
from modules.config import Config
from _archive.table_creator import Table_creator
import datetime
import tushare as ts
import pandas as pd
import urllib
#from StringIO import StringIO
from io import StringIO

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
        
        #consolidated bs (year) database
        self.str_db_consolidated_bs_year = 'db_consolidated_bs_year'
        self.create_db(self.str_db_consolidated_bs_year)
        
        #consolidated bs (season) database
        self.str_db_consolidated_bs_season= 'db_consolidated_bs_season'
        self.create_db(self.str_db_consolidated_bs_season)
           
        #consolidated pl(year) database
        self.str_db_consolidated_pl_year = 'db_consolidated_pl_year'
        self.create_db(self.str_db_consolidated_pl_year)
        
        #consolidated pl(season) database
        self.str_db_consolidated_pl_season = 'db_consolidated_pl_season'
        self.create_db(self.str_db_consolidated_pl_season)        
        
        #consolidated cash(year) database
        self.str_db_consolidated_cash_year= 'db_consolidated_cash_year'
        self.create_db(self.str_db_consolidated_cash_year)        
        
        #consolidated cash(season) database
        self.str_db_consolidated_cash_season= 'db_consolidated_cash_season'
        self.create_db(self.str_db_consolidated_cash_season)        
        
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
        
        
    #def update_db_consolidated_bs_year_data(self,stock_num):
        
        ##create db engine
        #engine = self.create_db_engine(self.str_db_consolidated_bs_year)
        
        ##set the table name
        #table_name = 'stock_'+str(stock_num)
        #table_consolidated_bs_year= self.table_creator.get_consolidated_bs_year(table_name) 
        #table_consolidated_bs_year.create(engine,checkfirst=True)   #create table
        #print("Create table:%s ok!"%(table_consolidated_bs_year.name))
        
        ##get data from website(网易财经)
        #url_txt = "http://quotes.money.163.com/service/zcfzb_"+str(stock_num)+".html?type=year"
        #webPage =  urllib.urlopen(url_txt)
        #bs_data = webPage.read().decode('gbk')
        #webPage.close()
        #bs_File = StringIO(bs_data)
        #bs_list_tmp = pd.read_csv(bs_File)
        #bs_list = bs_list_tmp.dropna(axis=1) #drop the nan value
        ##get the start date
        #result = engine.execute("select max(%s) from %s"%('报告日期',table_name))
        #last_date = result.fetchone()[0]
        
        #if last_date != None:
            #row_data = bs_list.columns[1:bs_list.columns.size-1]
            #i = 0
            #for str_date in row_data:
                #if last_date >= datetime.datetime.strptime(str_date,'%Y-%m-%d').date():
                    #break
                #i = i+1
            #if i>0:
                #bs_list = bs_list.iloc[:,0:i+1]
                #bs_list = bs_list.T    
                #bs_list.columns = bs_list.ix[0]
                #bs_list = bs_list.drop('报告日期')
                #bs_list = bs_list.replace('--',0,regex=True)
                #bs_list.index.name = '报告日期'
        
                #self.insert_to_db_no_duplicate(bs_list,table_name, engine,True)
                #print("Update Consolidated BS(year) %s ok!"%table_name)
            #else:
                #print("Consolidated BS(year) %s is the latest!"%table_name)
        #else:
            #bs_list = bs_list.T    
            #bs_list.columns = bs_list.ix[0]
            #bs_list = bs_list.drop('报告日期')
            #bs_list = bs_list.replace('--',0,regex=True)
            #bs_list.index.name = '报告日期'
            #self.insert_to_db_no_duplicate(bs_list,table_name, engine,True)
            #print("Create consolidated BS(year) %s ok!"%table_name)
            
        
        ##close the engine pool
        #engine.dispose()
 ##-------------------------------------------------------------------------------------------  
    #def update_db_consolidated_bs_season_data(self,stock_num):
        
        ##create db engine
        #engine = self.create_db_engine(self.str_db_consolidated_bs_season)
        
        ##set the table name
        #table_name = 'stock_'+str(stock_num)
        #table_consolidated_bs_season= self.table_creator.get_consolidated_bs_season(table_name) 
        #table_consolidated_bs_season.create(engine,checkfirst=True)   #create table
        #print("Create table:%s ok!"%(table_consolidated_bs_season.name))
        
        ##get data from website(网易财经)
        #url_txt = "http://quotes.money.163.com/service/zcfzb_"+str(stock_num)+".html"
        #webPage =  urllib.urlopen(url_txt)
        #bs_data = webPage.read().decode('gbk')
        #webPage.close()
        #bs_File = StringIO(bs_data)
        #bs_list_tmp = pd.read_csv(bs_File)
        #bs_list = bs_list_tmp.dropna(axis=1) #drop the nan value
        ##get the start date
        #result = engine.execute("select max(%s) from %s"%('报告日期',table_name))
        #last_date = result.fetchone()[0]
        
        #if last_date != None:
            #row_data = bs_list.columns[1:bs_list.columns.size-1]
            #i = 0
            #for str_date in row_data:
                #if last_date >= datetime.datetime.strptime(str_date,'%Y-%m-%d').date():
                    #break
                #i = i+1
            #if i>0:
                #bs_list = bs_list.iloc[:,0:i+1]
                #bs_list = bs_list.T    
                #bs_list.columns = bs_list.ix[0]
                #bs_list = bs_list.drop('报告日期')
                #bs_list = bs_list.replace('--',0,regex=True)
                #bs_list.index.name = '报告日期'
        
                #self.insert_to_db_no_duplicate(bs_list,table_name, engine,True)
                #print("Update Consolidated BS(season) %s ok!"%table_name)
            #else:
                #print("Consolidated BS(season) %s is the latest!"%table_name)
        #else:
            #bs_list = bs_list.T    
            #bs_list.columns = bs_list.ix[0]
            #bs_list = bs_list.drop('报告日期')
            #bs_list = bs_list.replace('--',0,regex=True)
            #bs_list.index.name = '报告日期'
            #self.insert_to_db_no_duplicate(bs_list,table_name, engine,True)
            #print("Create consolidated BS(season) %s ok!"%table_name)
            
        
         ##close the engine pool
        #engine.dispose()
##----------------------------------------------------------------------------
    #def update_db_consolidated_pl_year_data(self,stock_num):
        
        ##create db engine
        #engine = self.create_db_engine(self.str_db_consolidated_pl_year)
        
        ##set the table name
        #table_name = 'stock_'+str(stock_num)
        #table_consolidated_pl_year= self.table_creator.get_consolidated_pl_year(table_name) 
        #table_consolidated_pl_year.create(engine,checkfirst=True)   #create table
        #print("Create table:%s ok!"%(table_consolidated_pl_year.name))
        
        ##get data from website(网易财经)
        #url_txt = "http://quotes.money.163.com/service/lrb_"+str(stock_num)+".html?type=year"
        #webPage =  urllib.urlopen(url_txt)
        #pl_data = webPage.read().decode('gbk')
        #webPage.close()
        #pl_File = StringIO(pl_data)
        #pl_list_tmp = pd.read_csv(pl_File)
        #pl_list = pl_list_tmp.dropna(axis=1) #drop the nan value
        ##get the start date
        #result = engine.execute("select max(%s) from %s"%('报告日期',table_name))
        #last_date = result.fetchone()[0]
        
        #if last_date != None:
            #row_data = pl_list.columns[1:pl_list.columns.size-1]
            #i = 0
            #for str_date in row_data:
                #if last_date >= datetime.datetime.strptime(str_date,'%Y-%m-%d').date():
                    #break
                #i = i+1
            #if i>0:
                #pl_list = pl_list.iloc[:,0:i+1]
                #pl_list = pl_list.T    
                #pl_list.columns = pl_list.ix[0]
                #pl_list = pl_list.drop('报告日期')
                #pl_list = pl_list.replace('--',0,regex=True)
                #pl_list.index.name = '报告日期'
        
                #self.insert_to_db_no_duplicate(pl_list,table_name, engine,True)
                #print("Update Consolidated pl(year) %s ok!"%table_name)
            #else:
                #print("Consolidated PL(year) %s is the latest!"%table_name)
        #else:
            #pl_list = pl_list.T    
            #pl_list.columns = pl_list.ix[0]
            #pl_list = pl_list.drop('报告日期')
            #pl_list = pl_list.replace('--',0,regex=True)
            #pl_list.index.name = '报告日期'
            #self.insert_to_db_no_duplicate(pl_list,table_name, engine,True)
            #print("Create consolidated PL(year) %s ok!"%table_name)
            
        
        ##close the engine pool
        #engine.dispose()
##----------------------------------------------------------------------------
    #def update_db_consolidated_pl_season_data(self,stock_num):
            
        ##create db engine
        #engine = self.create_db_engine(self.str_db_consolidated_pl_season)
            
        ##set the table name
        #table_name = 'stock_'+str(stock_num)
        #table_consolidated_pl_season= self.table_creator.get_consolidated_pl_season(table_name) 
        #table_consolidated_pl_season.create(engine,checkfirst=True)   #create table
        #print("Create table:%s ok!"%(table_consolidated_pl_season.name))
            
        ##get data from website(网易财经)
        #url_txt = "http://quotes.money.163.com/service/lrb_"+str(stock_num)+".html"
        #webPage =  urllib.urlopen(url_txt)
        #pl_data = webPage.read().decode('gbk')
        #webPage.close()
        #pl_File = StringIO(pl_data)
        #pl_list_tmp = pd.read_csv(pl_File)
        #pl_list = pl_list_tmp.dropna(axis=1) #drop the nan value
        ##get the start date
        #result = engine.execute("select max(%s) from %s"%('报告日期',table_name))
        #last_date = result.fetchone()[0]
            
        #if last_date != None:
            #row_data = pl_list.columns[1:pl_list.columns.size-1]
            #i = 0
            #for str_date in row_data:
                #if last_date >= datetime.datetime.strptime(str_date,'%Y-%m-%d').date():
                    #break
                #i = i+1
            #if i>0:
                #pl_list = pl_list.iloc[:,0:i+1]
                #pl_list = pl_list.T    
                #pl_list.columns = pl_list.ix[0]
                #pl_list = pl_list.drop('报告日期')
                #pl_list = pl_list.replace('--',0,regex=True)
                #pl_list.index.name = '报告日期'
            
                #self.insert_to_db_no_duplicate(pl_list,table_name, engine,True)
                #print("Update Consolidated pl(season) %s ok!"%table_name)
            #else:
                #print("Consolidated PL(season) %s is the latest!"%table_name)
        #else:
            #pl_list = pl_list.T    
            #pl_list.columns = pl_list.ix[0]
            #pl_list = pl_list.drop('报告日期')
            #pl_list = pl_list.replace('--',0,regex=True)
            #pl_list.index.name = '报告日期'
            #self.insert_to_db_no_duplicate(pl_list,table_name, engine,True)
            #print("Create consolidated PL(season) %s ok!"%table_name)
                
            
        ##close the engine pool
        #engine.dispose()
    ##----------------------------------------------------------------------------
    #def update_db_consolidated_cash_year_data(self,stock_num):
            
            ##create db engine
            #engine = self.create_db_engine(self.str_db_consolidated_cash_year)
            
            ##set the table name
            #table_name = 'stock_'+str(stock_num)
            #table_consolidated_cash_year= self.table_creator.get_consolidated_cash(table_name) 
            #table_consolidated_cash_year.create(engine,checkfirst=True)   #create table
            #print("Create table:%s ok!"%(table_consolidated_cash_year.name))
            
            ##get data from website(网易财经)
            #url_txt = "http://quotes.money.163.com/service/xjllb_"+str(stock_num)+".html?type=year"
            #webPage =  urllib.urlopen(url_txt)
            #cash_data = webPage.read().decode('gbk')
            #webPage.close()
            #cash_File = StringIO(cash_data)
            #cash_list_tmp = pd.read_csv(cash_File)
            #cash_list = cash_list_tmp.dropna(axis=1)
            ##get the start date
            #result = engine.execute("select max(%s) from %s"%('报告日期',table_name))
            #last_date = result.fetchone()[0]
            
            #if last_date != None:
                #row_data = cash_list.columns[1:cash_list.columns.size-1]#不包括第一和最后一行，因为第一行为报告日期，最后一行为空行
                #i = 0
                #for str_date in row_data:
                    #if last_date >= datetime.datetime.strptime(str_date,'%Y-%m-%d').date():
                        #break
                    #i = i+1
                #if i>0:
                    #cash_list = cash_list.iloc[:,0:i+1]
                    #cash_list = cash_list.T    
                    #cash_list.iloc[0,2]='向中央银行借款净增加额(万元)'
                    #cash_list.columns = cash_list.ix[0].str.strip()
                    #cash_list = cash_list.drop(' 报告日期')
                    #cash_list = cash_list.replace('--',0,regex=True)
                    #cash_list.index.name = '报告日期'
            
                    #self.insert_to_db_no_duplicate(cash_list,table_name, engine,True)
                    #print("Update Consolidated cash(year) %s ok!"%table_name)
                #else:
                    #print("Consolidated cash(year) %s is the latest!"%table_name)
            #else:
                #cash_list = cash_list.T    
                #cash_list.iloc[0,2]='向中央银行借款净增加额(万元)'
                #cash_list.columns = cash_list.ix[0].str.strip()
                #cash_list = cash_list.drop(' 报告日期')
                #cash_list = cash_list.drop(' ')
                #cash_list = cash_list.replace('--',0,regex=True)
                #cash_list.index.name = '报告日期'
                #self.insert_to_db_no_duplicate(cash_list,table_name, engine,True)
                #print("Create consolidated cash(year) %s ok!"%table_name)
                
            
            ##close the engine pool
            #engine.dispose()
    ##----------------------------------------------------------------------------
    #----------------------------------------------------------------------------
    def update_db_consolidated_statement_data(self,stock_num,statement_type,statement_period):

        """
        Download the statement data from internet and upload to the mysql DB
        
        Input:
        stock_num: the stock number
        statement_type: 'BS' -> Balance Sheet ; 'PL' -> Profit & Loss ; 'Cash' ->  Cash
        statement_period: 'year' -> yearly statement ; 'season' -> per season statement
        
        """
        
        #set the table name
        table_name = 'stock_'+str(stock_num)
        
        #create db engine
        if statement_type == 'BS' and statement_period == 'year':
            engine = self.create_db_engine(self.str_db_consolidated_bs_year)
            table_consolidated = self.table_creator.get_consolidated_bs(table_name) 
            url_txt = "http://quotes.money.163.com/service/zcfzb_"+str(stock_num)+".html?type=year"
        elif statement_type == 'BS' and statement_period == 'season':
            engine = self.create_db_engine(self.str_db_consolidated_bs_season)
            table_consolidated = self.table_creator.get_consolidated_bs(table_name) 
            url_txt = "http://quotes.money.163.com/service/zcfzb_"+str(stock_num)+".html"
        elif statement_type == 'PL' and statement_period == 'year':
            engine = self.create_db_engine(self.str_db_consolidated_pl_year)
            table_consolidated = self.table_creator.get_consolidated_pl(table_name) 
            url_txt = "http://quotes.money.163.com/service/lrb_"+str(stock_num)+".html?type=year"
        elif statement_type == 'PL' and statement_period == 'season':
            engine = self.create_db_engine(self.str_db_consolidated_pl_season)
            table_consolidated = self.table_creator.get_consolidated_pl(table_name) 
            url_txt = "http://quotes.money.163.com/service/lrb_"+str(stock_num)+".html"
        elif statement_type == 'Cash' and statement_period == 'year':
            engine = self.create_db_engine(self.str_db_consolidated_cash_year)
            table_consolidated = self.table_creator.get_consolidated_cash(table_name) 
            url_txt = "http://quotes.money.163.com/service/xjllb_"+str(stock_num)+".html?type=year"
        elif statement_type == 'Cash' and statement_period == 'season':
            engine = self.create_db_engine(self.str_db_consolidated_cash_season)
            table_consolidated = self.table_creator.get_consolidated_cash(table_name) 
            url_txt = "http://quotes.money.163.com/service/xjllb_"+str(stock_num)+".html"
        
        table_consolidated.create(engine,checkfirst=True)   #create table
        print("Create table:%s ok!"%(table_consolidated.name))

        #get data from website(网易财经)
        #webPage =  urllib.urlopen(url_txt)
        webPage =  urllib.request.urlopen(url_txt)
        statement_data = webPage.read().decode('gbk')
        webPage.close()
        statement_File = StringIO(statement_data)
        statement_list_tmp = pd.read_csv(statement_File)
        statement_list = statement_list_tmp.dropna(axis=1)
        #get the start date
        result = engine.execute("select max(%s) from %s"%('报告日期',table_name))
        last_date = result.fetchone()[0]

        if last_date != None:
            row_data = statement_list.columns[1:statement_list.columns.size-1]#不包括第一和最后一列，因为第一列为报告日期，最后一列为空行
            i = 0
            for str_date in row_data:
                if last_date >= datetime.datetime.strptime(str_date,'%Y-%m-%d').date():
                    break
                i = i+1
            if i>0:
                statement_list = statement_list.iloc[:,0:i+1]
                statement_list = statement_list.T    
                if statement_type == 'Cash':
                    statement_list.iloc[0,2]='向中央银行借款净增加额(万元)'#Cash statement 的特殊情况
                    
                statement_list.columns = statement_list.ix[0].str.strip()
                
                if statement_type == 'Cash':
                    statement_list = statement_list.drop(' 报告日期')#Cash statement 的特殊情况
                else:
                    statement_list = statement_list.drop('报告日期')
                    
                statement_list = statement_list.replace('--',0,regex=True)
                statement_list.index.name = '报告日期'

                self.insert_to_db_no_duplicate(statement_list,table_name, engine,True)
                print("Update Consolidated statement %s %s ok!"%(statement_type,table_name))
            else:
                print("Consolidated statement %s %s is the latest!"%(statement_type,table_name))
        else:
            statement_list = statement_list.T  
            if statement_type == 'Cash':
                statement_list.iloc[0,2]='向中央银行借款净增加额(万元)'#Cash statement 的特殊情况
                
            statement_list.columns = statement_list.ix[0].str.strip()
            
            if statement_type == 'Cash':
                statement_list = statement_list.drop(' 报告日期')
                statement_list = statement_list.drop(' ')#Cash statement 的特殊情况
            else:
                statement_list = statement_list.drop('报告日期')
                
            statement_list = statement_list.replace('--',0,regex=True)#原始数据中没有的数据以'--'表示
            statement_list.index.name = '报告日期'
            self.insert_to_db_no_duplicate(statement_list,table_name, engine,True)
            
            if statement_period == 'year':
                print("Create consolidated statement(%s year) %s ok!"%(statement_type,table_name))
            else:
                print("Create consolidated statement(%s season) %s ok!"%(statement_type,table_name))

        #close the engine pool
        engine.dispose()
    #----------------------------------------------------------------------------
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
    
    
    #test the consolidated statement data
    test.update_db_consolidated_statement_data('000002','Cash','year')
    
    print("Complete ok")
    