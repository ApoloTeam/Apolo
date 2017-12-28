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

    @staticmethod
    def testing():
        return print(AdminDatabase.engine)

    @classmethod
    def create_database(cls, db_name):
        try:
            print('Create database: ' + db_name + ' if not exist')
            cls.engine.execute("create database if not exists %s" % db_name)
            print('apolo database created.')
        except pymysql.Warning as w:
            print("Warning:%s" % str(w))
        except pymysql.Error as e:
            print("Error %d:%s" % (e.args[0], e.args[1]))

        cls.engine.dispose()  # stop all the engine connection

    @classmethod
    def insert_to_db_no_duplicate(cls, df, table_name, has_index=False):

        try:
            df.to_sql(name=table_name, con=cls.engine, if_exists='append', index=has_index)
        except exc.IntegrityError:
            print("Data duplicated, try to insert one by one")
            # df is a dataframe
            num_rows = len(df)
            # iterate one row at a time
            for i in range(num_rows):
                try:
                    # try inserting the row
                    df[i:i + 1].to_sql(name=table_name, con=cls.engine, if_exists='append', index=has_index)
                except exc.IntegrityError:
                    # ignore duplicates
                    pass

    @classmethod
    def update_db_k_data(cls, stock_code):
        print('k_data, start to update %s' % stock_code)
        # set the table name
        tbl_k_data = 'k_data'
        # get the start date
        result = cls.engine.execute("select max(date) from %s where code=\'%s\'" % (tbl_k_data, stock_code))
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

        # insert data to database
        cls.insert_to_db_no_duplicate(k_data, tbl_k_data)
        print('%s updated, done' % stock_code)
        # close the engine pool
        cls.engine.dispose()

    # TODO: Only hs300, sz50,zz500 left including create table and update data function
    # TODO: 2017-12-24 hs300 api doesn't work
    @classmethod
    def update_hs300_list(cls):
        # update hs300(沪深300) list:
        tbl_hs300_list = 'hs300_list'
        # get the list from Tushare
        hs300_list = ts.get_hs300s()
        print('get hs300_list data ok!')
        print(hs300_list)
        # insert list
        # cls.insert_to_db_no_duplicate(hs300_list, tbl_hs300_list, cls.engine)
        print("Insert hs300_list data ok!")

        # close the engine pool
        cls.engine.dispose()

    @classmethod
    def update_sz50_list(cls):
        # update hs300(沪深300) list:
        tbl_sz50_list = 'sz50_list'
        # get the list from Tushare
        # TODO: API has issue
        sz50_list = ts.get_sz50s()
        print('get sz50_list data ok!')
        print(sz50_list)
        # insert list
        cls.insert_to_db_no_duplicate(sz50_list, tbl_sz50_list, cls.engine)
        print("Insert sz50_list data ok!")

        # close the engine pool
        cls.engine.dispose()

    # TODO: Update "code" column. raw data EXCLUDE code so that need to update independently
    # 旧接口 - 历史数据
    @classmethod
    def update_db_history_data(cls, stock_code):
        tbl_history_data = 'history_data'
        # get the start date
        result = cls.engine.execute("select max(date) from %s where" % tbl_history_data)
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
        cls.insert_to_db_no_duplicate(history_data, tbl_history_data, has_index=True)

        # close the engine pool
        cls.engine.dispose()

    @classmethod
    def update_db_dividend_data(cls):
        tbl_dividend_data = 'dividend_data'

        # get the start date
        result = cls.engine.execute("select max(year) from %s" % tbl_dividend_data)
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
            cls.insert_to_db_no_duplicate(dividend_data, tbl_dividend_data)

        print("Updated, done")
        # close the engine pool
        cls.engine.dispose()

    @classmethod
    def update_db_consolidated_statement_data(cls, stock_code, statement_type):
        """
        Download the statement data from internet and upload to the mysql DB

        Input:
        stock_num: the stock number
        statement_type: 'BS' -> Balance Sheet ; 'PL' -> Profit & Loss ; 'Cash' ->  Cash
        statement_period: 'year' -> yearly statement ; 'season' -> per season statement

        Note: if only get year data, can use below link
        "http://quotes.money.163.com/service/zcfzb_" + str(stock_num) + ".html?type=year"
        """
        # set the table name
        table_name = ''
        url_txt = ''

        if statement_type == 'BS':
            url_txt = "http://quotes.money.163.com/service/zcfzb_" + str(stock_code) + ".html"
            table_name = 'con_bs_season'

        elif statement_type == 'PL':
            url_txt = "http://quotes.money.163.com/service/lrb_" + str(stock_code) + ".html"
            table_name = 'con_pl_season'

        elif statement_type == 'Cash':
            url_txt = "http://quotes.money.163.com/service/xjllb_" + str(stock_code) + ".html"
            table_name = 'con_cash_season'

        # get data from website(网易财经)
        web_page = urllib.request.urlopen(url_txt)
        statement_data = web_page.read().decode('gbk')
        web_page.close()
        statement_file = string_io(statement_data)
        statement_list_tmp = pd.read_csv(statement_file)
        statement_list = statement_list_tmp.dropna(axis=1)
        # get the start date
        result = cls.engine.execute("select max(%s) from %s where code=\'%s\'" % ('报告日期', table_name, stock_code))
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
                statement_list['code'] = stock_code
                cls.insert_to_db_no_duplicate(statement_list, table_name, True)
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
            statement_list['code'] = stock_code
            cls.insert_to_db_no_duplicate(statement_list, table_name, True)

            print("Create consolidated statement(%s season) %s ok!" % (statement_type, table_name))

        # close the engine pool
        cls.engine.dispose()

    # ----------------------------------------------------------------------------
    @classmethod
    def get_table_data(cls, table_name, select_column=None):
        """
        get the table data
        """
        result = pd.read_sql_table(table_name, cls.engine, columns=select_column)
        # result = pd.read_sql('select {col} from {tbl}'.format(col=select_column, tbl=table_name), cls.engine)
        cls.engine.dispose()
        return result


if __name__ == '__main__':
    AdminDatabase.update_db_consolidated_statement_data('000004','Cash')
