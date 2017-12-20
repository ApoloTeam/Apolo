from sqlalchemy import exc
import pymysql
import datetime
import tushare as ts
import pandas as pd
import urllib.request
from io import StringIO as string_io
from modules.connect_database import ConnectDatabase
from modules.create_table import CreateTable


class AdminDatabase:
    connection = ConnectDatabase()
    engine = connection.create_db_engine()
    table_creator = CreateTable()
        # self.engine = connection.create_db_engine()

    @staticmethod
    def testing():
        return print(AdminDatabase.engine)

    def create_database(self, db_name):
        try:
            print('Create database: ' + db_name + ' if not exist')
            self.engine.execute("create database if not exists %s" % (db_name))
            print('apolo database created.')
        except pymysql.Warning as w:
            print("Warning:%s" % str(w))
        except pymysql.Error as e:
            print("Error %d:%s" % (e.args[0], e.args[1]))

        self.engine.dispose()  # stop all the engine connection

    def insert_to_db_no_duplicate(self, df, table_name, engine, has_index=False):

        try:
            df.to_sql(name=table_name, con=engine, if_exists='append', index=has_index)
        except exc.IntegrityError:
            print("Data duplicated, try to insert one by one")
            # df is a dataframe
            num_rows = len(df)
            # iterate one row at a time
            for i in range(num_rows):
                try:
                    # try inserting the row
                    df[i:i + 1].to_sql(name=table_name, con=engine, if_exists='append', index=has_index)
                except exc.IntegrityError:
                    # ignore duplicates
                    pass

    def update_db_k_data(self, stock_code):
        # create k_data db engine
        # engine = self.create_db_engine(self.str_db_k_data)

        # set the table name
        table_name = 'k_data_' + stock_code
        table_k_table = self.table_creator.get_table_k_data(table_name)
        table_k_table.create(self.engine, checkfirst=True)  # create table
        print("Create k_data table:%s ok!" % table_name)

        # get the start date
        result = self.engine.execute("select max(%s) from %s" % (table_k_table.c.date, table_name))
        last_date = result.fetchone()[0]
        if last_date is None:
            start_date = datetime.date(2000, 1, 1)  # default start date
        else:
            start_date = last_date + datetime.timedelta(days=1)

        # get the end date
        end_date = datetime.date.today()

        if start_date < end_date:
            str_start_date = start_date.strftime("%Y-%m-%d")
            str_end_date = end_date.strftime("%Y-%m-%d")
        else:
            str_end_date = end_date.strftime("%Y-%m-%d")
            str_start_date = str_end_date
        print('start date:' + str_start_date + ' ; end date:' + str_end_date)
        # get the k_data from Tushare
        k_data = ts.get_k_data(code=stock_code, start=str_start_date, end=str_end_date)
        # print(k_data)

        # insert data to database
        self.insert_to_db_no_duplicate(k_data, table_k_table.name, self.engine)

        # close the engine pool
        self.engine.dispose()

    def update_stock_list(self):

        # engine = self.create_db_engine(self.str_db_stock_classification)

        # update hs300(沪深300) list:
        table_hs300_list = self.table_creator.get_table_hs300_list()
        table_hs300_list.create(self.engine, checkfirst=True)
        print("Create %s list table ok!" % table_hs300_list.name)
        # get the list from Tushare
        hs300_list = ts.get_hs300s()
        print('get %s data ok!' % table_hs300_list.name)
        # insert list
        self.insert_to_db_no_duplicate(hs300_list, table_hs300_list.name, self.engine)
        print("Insert %s data ok!" % table_hs300_list.name)

        # close the engine pool
        self.engine.dispose()

    def update_db_history_data(self, stock_code):

        # create db engine
        # engine = self.create_db_engine(self.str_db_history_data)

        # set the table name
        table_name = 'history_data_' + stock_code
        table_history_table = self.table_creator.get_table_history_data(table_name)
        table_history_table.create(self.engine, checkfirst=True)  # create table
        print("Create table:%s ok!" % table_name)

        # get the start date
        result = self.engine.execute("select max(%s) from %s" % (table_history_table.c.date, table_name))
        last_date = result.fetchone()[0]
        if last_date is None:
            start_date = datetime.date(2000, 1, 1)  # default start date
        else:
            start_date = last_date + datetime.timedelta(days=1)

        # get the end date
        end_date = datetime.date.today()

        if start_date < end_date:
            str_start_date = start_date.strftime("%Y-%m-%d")
            str_end_date = end_date.strftime("%Y-%m-%d")
        else:
            str_end_date = end_date.strftime("%Y-%m-%d")
            str_start_date = str_end_date
        print('start date:' + str_start_date + ' ; end date:' + str_end_date)
        # get the history data from Tushare
        history_data = ts.get_hist_data(code=stock_code, start=str_start_date, end=str_end_date)
        # print(history_data)

        # insert data to database
        self.insert_to_db_no_duplicate(history_data, table_history_table.name, self.engine, has_index=True)

        # close the engine pool
        self.engine.dispose()

    def update_db_dividend_data(self):

        # create db engine
        # engine = self.create_db_engine(self.str_db_investment_data)

        # set the table name
        table_dividend_data = self.table_creator.get_table_dividend_data()
        table_dividend_data.create(self.engine, checkfirst=True)  # create table
        print("Create table:%s ok!" % table_dividend_data.name)

        # get the start date
        result = self.engine.execute("select max(%s) from %s" % (table_dividend_data.c.year, table_dividend_data.name))
        last_year = result.fetchone()[0]
        if last_year is None:
            start_year = 2005
        else:
            start_year = last_year + 1

        # get the end year
        end_year = datetime.datetime.now().year

        if start_year >= end_year:
            start_year = end_year
        print('start year:' + str(start_year) + ' ; end year:' + str(end_year))
        # get the profit data
        for n in range(start_year, end_year):
            dividend_data = ts.profit_data(year=n, top=4000)
            print("Dividend data at year:%s" % n)
            # print(dividend_data)
            # insert data to database
            self.insert_to_db_no_duplicate(dividend_data, table_dividend_data.name, self.engine)

        # close the engine pool
        self.engine.dispose()

    def update_db_profit_data(self):
        # set the table name
        table_profit_data = self.table_creator.get_table_profit_data()
        table_profit_data.create(self.engine, checkfirst=True)  # create table
        print("Create table:%s ok!" % table_profit_data.name)

        # get the start date
        result = self.engine.execute("select max(%s) from %s" % (table_profit_data.c.year, table_profit_data.name))
        last_year = result.fetchone()[0]
        if last_year is None:
            start_year = 2005
        else:
            start_year = last_year + 1

        # get the end year
        end_year = datetime.datetime.now().year

        if start_year >= end_year:
            start_year = end_year
        print('start year:' + str(start_year) + ' ; end year:' + str(end_year))
        # get the profit data
        for n in range(start_year, end_year):
            profit_data = ts.profit_data(year=n, top=4000)
            print("profit data at year:%s" % n)
            print(profit_data)
            # insert data to database
            self.insert_to_db_no_duplicate(profit_data, table_profit_data.name, self.engine)

        # close the engine pool
            self.engine.dispose()

    def update_db_consolidated_statement_data(self, stock_num, statement_type, statement_period):

        """
        Download the statement data from internet and upload to the mysql DB

        Input:
        stock_num: the stock number
        statement_type: 'BS' -> Balance Sheet ; 'PL' -> Profit & Loss ; 'Cash' ->  Cash
        statement_period: 'year' -> yearly statement ; 'season' -> per season statement

        """

        # set the table name
        table_name = 'stock_' + str(stock_num)

        # create db engine
        if statement_type == 'BS' and statement_period == 'year':
            # engine = self.create_db_engine(self.str_db_consolidated_bs_year)
            table_consolidated = self.table_creator.get_consolidated_bs(table_name)
            url_txt = "http://quotes.money.163.com/service/zcfzb_" + str(stock_num) + ".html?type=year"
        elif statement_type == 'BS' and statement_period == 'season':
            # engine = self.create_db_engine(self.str_db_consolidated_bs_season)
            table_consolidated = self.table_creator.get_consolidated_bs(table_name)
            url_txt = "http://quotes.money.163.com/service/zcfzb_" + str(stock_num) + ".html"
        elif statement_type == 'PL' and statement_period == 'year':
            # engine = self.create_db_engine(self.str_db_consolidated_pl_year)
            table_consolidated = self.table_creator.get_consolidated_pl(table_name)
            url_txt = "http://quotes.money.163.com/service/lrb_" + str(stock_num) + ".html?type=year"
        elif statement_type == 'PL' and statement_period == 'season':
            # engine = self.create_db_engine(self.str_db_consolidated_pl_season)
            table_consolidated = self.table_creator.get_consolidated_pl(table_name)
            url_txt = "http://quotes.money.163.com/service/lrb_" + str(stock_num) + ".html"
        elif statement_type == 'Cash' and statement_period == 'year':
            # engine = self.create_db_engine(self.str_db_consolidated_cash_year)
            table_consolidated = self.table_creator.get_consolidated_cash(table_name)
            url_txt = "http://quotes.money.163.com/service/xjllb_" + str(stock_num) + ".html?type=year"
        elif statement_type == 'Cash' and statement_period == 'season':
            # engine = self.create_db_engine(self.str_db_consolidated_cash_season)
            table_consolidated = self.table_creator.get_consolidated_cash(table_name)
            url_txt = "http://quotes.money.163.com/service/xjllb_" + str(stock_num) + ".html"

        table_consolidated.create(self.engine, checkfirst=True)  # create table
        print("Create table:%s ok!" % table_consolidated.name)

        # get data from website(网易财经)
        webPage = urllib.request.urlopen(url_txt)
        statement_data = webPage.read().decode('gbk')
        webPage.close()
        statement_File = string_io(statement_data)
        statement_list_tmp = pd.read_csv(statement_File)
        statement_list = statement_list_tmp.dropna(axis=1)
        # get the start date
        result = self.engine.execute("select max(%s) from %s" % ('报告日期', table_name))
        last_date = result.fetchone()[0]

        if last_date is not None:
            row_data = statement_list.columns[1:statement_list.columns.size - 1]  # 不包括第一和最后一列，因为第一列为报告日期，最后一列为空行
            i = 0
            for str_date in row_data:
                if last_date >= datetime.datetime.strptime(str_date, '%Y-%m-%d').date():
                    break
                i = i + 1
            if i > 0:
                statement_list = statement_list.iloc[:, 0:i + 1]
                statement_list = statement_list.T
                if statement_type == 'Cash':
                    statement_list.iloc[0, 2] = '向中央银行借款净增加额(万元)'  # Cash statement 的特殊情况

                statement_list.columns = statement_list.ix[0].str.strip()

                if statement_type == 'Cash':
                    statement_list = statement_list.drop(' 报告日期')  # Cash statement 的特殊情况
                else:
                    statement_list = statement_list.drop('报告日期')

                statement_list = statement_list.replace('--', 0, regex=True)
                statement_list.index.name = '报告日期'

                self.insert_to_db_no_duplicate(statement_list, table_name, self.engine, True)
                print("Update Consolidated statement %s %s ok!" % (statement_type, table_name))
            else:
                print("Consolidated statement %s %s is the latest!" % (statement_type, table_name))
        else:
            statement_list = statement_list.T
            if statement_type == 'Cash':
                statement_list.iloc[0, 2] = '向中央银行借款净增加额(万元)'  # Cash statement 的特殊情况

            statement_list.columns = statement_list.ix[0].str.strip()

            if statement_type == 'Cash':
                statement_list = statement_list.drop(' 报告日期')
                statement_list = statement_list.drop(' ')  # Cash statement 的特殊情况
            else:
                statement_list = statement_list.drop('报告日期')

            statement_list = statement_list.replace('--', 0, regex=True)  # 原始数据中没有的数据以'--'表示
            statement_list.index.name = '报告日期'
            self.insert_to_db_no_duplicate(statement_list, table_name, self.engine, True)

            if statement_period == 'year':
                print("Create consolidated statement(%s year) %s ok!" % (statement_type, table_name))
            else:
                print("Create consolidated statement(%s season) %s ok!" % (statement_type, table_name))

        # close the engine pool
        self.engine.dispose()

    # ----------------------------------------------------------------------------
    def get_table_data(self, table_name, select_column=None):
        """
        get the table data
        """
        # engine = self.create_db_engine(db_name)
        result = pd.read_sql_table(table_name, self.engine, columns=select_column)
        self.engine.dispose()
        return result

    # def select_table_data(self,db_name):
    # engine = self.create_db_engine(db_name)
#
if __name__ == '__main__':
    # test = AdminDatabase()
    AdminDatabase.testing()
