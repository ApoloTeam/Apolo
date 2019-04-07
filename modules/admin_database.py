from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
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
    con, cur = connection.connect_server()
    db_session = sessionmaker(bind=engine)
    Session = db_session()

    @classmethod
    def testing(cls):
        return print(cls.engine)

    # @classmethod
    # def create_database(cls, db_name):
    #     try:
    #         print('Create database: ' + db_name + ' if not exist')
    #         cls.engine.execute("create database if not exists %s" % db_name)
    #         print('apolo database created.')
    #     except pymysql.Warning as w:
    #         print("Warning:%s" % str(w))
    #     except pymysql.Error as e:
    #         print("Error %d:%s" % (e.args[0], e.args[1]))
    #
    #     cls.engine.dispose()  # stop all the engine connection

    @classmethod
    def get_table_data(cls, table_name, select_column=None):
        """
        get the table data
        """
        result = pd.read_sql_table(table_name, cls.engine, columns=select_column)
        # result = pd.read_sql('select {col} from {tbl}'.format(col=select_column, tbl=table_name), cls.engine)
        cls.engine.dispose()
        return result

    @classmethod
    def get_field_data_stock_basics(cls, stock_code, field):
        cls.cur.execute("select {f} from stock_basics where code={code}".format(f=field, code=stock_code))
        f = cls.cur.fetchall()
        return f[0][0]

    @classmethod
    def get_timeToMarket(cls, stock_code):
        timeToMarket = str(cls.get_field_data_stock_basics(stock_code, field='timeToMarket'))
        timeToMarket = datetime.date(int(timeToMarket[0:4]), int(timeToMarket[4:6]), int(timeToMarket[6:8]))
        return timeToMarket

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
            start_date = cls.get_timeToMarket(stock_code)
        else:
            start_date = last_date + datetime.timedelta(days=1)
        # get today as the end date
        end_date = datetime.date.today()

        diff = end_date - start_date
        if diff.days > 365:
            print("Exceed one year")
            print("Updating this year")
            str_last_year_start_date = datetime.date(end_date.year, 1, 1).strftime("%Y-%m-%d")
            str_end_date = end_date.strftime("%Y-%m-%d")
            # get the k_data from Tushare
            k_data = ts.get_k_data(code=stock_code, start=str_last_year_start_date, end=str_end_date)
            # insert data to database
            cls.insert_to_db_no_duplicate(k_data, tbl_k_data)
            print("Updated this year %s, done!" % stock_code)

            print("Update the period")
            for y in range(start_date.year+1, end_date.year):
                str_period_start_date = datetime.date(y, 1, 1).strftime("%Y-%m-%d")
                str_period_end_date = datetime.date(y, 12, 31).strftime("%Y-%m-%d")
                # get the k_data from Tushare
                k_data = ts.get_k_data(code=stock_code, start=str_period_start_date, end=str_period_end_date)
                # insert data to database
                cls.insert_to_db_no_duplicate(k_data, tbl_k_data)
                print("%d year updated" % y)
            print("updated the period")

            print("update the first year to be listed")
            str_listing_date = start_date.strftime("%Y-%m-%d")
            str_first_year_end_date = datetime.date(start_date.year, 12, 31).strftime("%Y-%m-%d")
            print('listing date:' + str_listing_date + ' ; fist year end date:' + str_first_year_end_date)
            # get the k_data from Tushare
            k_data = ts.get_k_data(code=stock_code, start=str_listing_date, end=str_first_year_end_date)
            # insert data to database
            cls.insert_to_db_no_duplicate(k_data, tbl_k_data)
            print("updated the first year")
        else:
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
        return '%s updated, done' % stock_code

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
        result = cls.engine.execute("select max(date) from %s where code=\'%s\'" % (tbl_history_data, stock_code))
        last_date = result.fetchone()[0]
        if last_date is None:
            start_date = cls.get_timeToMarket(stock_code)
        else:
            start_date = last_date + datetime.timedelta(days=1)
        # get today as the end date
        end_date = datetime.date.today()

        diff = end_date - start_date
        if diff.days > 365:
            print("exceed one year")

            print("update this year")
            str_last_year_start_date = datetime.date(end_date.year, 1, 1).strftime("%Y-%m-%d")
            str_end_date = end_date.strftime("%Y-%m-%d")
            print('start date:' + str_last_year_start_date + ' ; end date:' + str_end_date)
            # get the k_data from Tushare
            history_data = ts.get_hist_data(code=stock_code, start=str_last_year_start_date, end=str_end_date)
            history_data['code'] = stock_code
            # insert data to database
            cls.insert_to_db_no_duplicate(history_data, tbl_history_data)
            print("Update this year, done!")

            print("Update the period")
            for y in range(end_date.year + 1, start_date.year, -1):
                str_period_start_date = datetime.date(y, 1, 1).strftime("%Y-%m-%d")
                str_period_end_date = datetime.date(y, 12, 31).strftime("%Y-%m-%d")
                print('start date:' + str_period_start_date + ' ; end date:' + str_period_end_date)
                # get the k_data from Tushare
                history_data = ts.get_hist_data(code=stock_code, start=str_period_start_date, end=str_period_end_date)
                history_data['code'] = stock_code
                # insert data to database
                cls.insert_to_db_no_duplicate(history_data, tbl_history_data)
                print("%d year updated" % y)
            print("Update the period, done!")

            print("update the first year")
            str_start_date = start_date.strftime("%Y-%m-%d")
            str_first_year_end_date = datetime.date(start_date.year, 12, 31).strftime("%Y-%m-%d")
            # get the k_data from Tushare
            history_data = ts.get_hist_data(code=stock_code, start=str_start_date, end=str_first_year_end_date)
            history_data['code'] = stock_code
            # insert data to database
            cls.insert_to_db_no_duplicate(history_data, tbl_history_data)
            print("updated the first year")

            print('%s updated, done' % stock_code)
        else:
            if start_date < end_date:
                str_start_date = start_date.strftime("%Y-%m-%d")
                str_end_date = end_date.strftime("%Y-%m-%d")
            else:
                str_end_date = end_date.strftime("%Y-%m-%d")
                str_start_date = str_end_date
            print('start date:' + str_start_date + ' ; end date:' + str_end_date)
            # get the history data from Tushare
            history_data = ts.get_hist_data(code=stock_code, start=str_start_date, end=str_end_date)
            history_data['code'] = stock_code
            # insert data to database
            cls.insert_to_db_no_duplicate(history_data, tbl_history_data, has_index=True)

        # close the engine pool
        cls.engine.dispose()
        return "Update history, done!"

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
        for y in range(end_year, start_year, -1):
            dividend_data = ts.profit_data(year=y, top=4000)
            print("Dividend data at year:%s" % y)
            # insert data to database
            cls.insert_to_db_no_duplicate(dividend_data, tbl_dividend_data)

        print("Updated, done")
        # close the engine pool
        cls.engine.dispose()
        return "Update dividend, Done!"

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
        return "Update consolidated statement(%s season) %s, done!" % (statement_type, table_name)

    # ----------------------------------------------------------------------------
    @classmethod
    def update_data_hs300(cls):
        hs300_list_table = CreateTable.create_table_hs300_list()
        hs300_list_code = AdminDatabase.get_table_data(hs300_list_table.name, [hs300_list_table.c.code.name])
        count = 0.0
        print("K Data updating...")
        for row in hs300_list_code[hs300_list_table.c.code.name]:
            AdminDatabase.update_db_k_data(row)
            print("update :%s OK" % row)
            count = count + 1
            print("Percentage:%.1f%%" % (count / hs300_list_code.size * 100))

        print("Completed files:%d, ok!" % count)

        count = 0.0
        print("Balance Sheet updating...")
        for row in hs300_list_code[hs300_list_table.c.code.name]:
            AdminDatabase.update_db_consolidated_statement_data(row, 'BS')
            print("update :%s OK" % row)
            count = count + 1
            print("Percentage:%.1f%%" % (count / hs300_list_code.size * 100))

        print("Completed files:%d, ok!" % count)

        count = 0.0
        print("Cash Flow Statement updating...")
        for row in hs300_list_code[hs300_list_table.c.code.name]:
            AdminDatabase.update_db_consolidated_statement_data(row, 'Cash')
            print("update :%s OK" % row)
            count = count + 1
            print("Percentage:%.1f%%" % (count / hs300_list_code.size * 100))

        print("Completed files:%d, ok!" % count)

        count = 0.0
        print("Income Statement updating...")
        for row in hs300_list_code[hs300_list_table.c.code.name]:
            AdminDatabase.update_db_consolidated_statement_data(row, 'PL')
            print("update :%s OK" % row)
            count = count + 1
            print("Percentage:%.1f%%" % (count / hs300_list_code.size * 100))

        print("Completed files:%d, ok!" % count)
        return 'Update hs300, done!'

    @classmethod
    def update_data_sz50(cls):
        sz50_list_table = CreateTable.create_table_sz50_list()
        sz50_list_code = AdminDatabase.get_table_data(sz50_list_table.name, [sz50_list_table.c.code.name])
        count = 0.0
        print("K Data updating...")
        for row in sz50_list_code[sz50_list_table.c.code.name]:
            AdminDatabase.update_db_k_data(row)
            print("update :%s OK" % row)
            count = count + 1
            print("Percentage:%.1f%%" % (count / sz50_list_code.size * 100))

        print("K Data, completed files:%d, ok!" % count)

        count = 0.0
        print("*** Balance Sheet updating...")
        for row in sz50_list_code[sz50_list_table.c.code.name]:
            AdminDatabase.update_db_consolidated_statement_data(row, 'BS')
            print("update :%s OK" % row)
            count = count + 1
            print("Percentage:%.1f%%" % (count / sz50_list_code.size * 100))

        print("Completed files:%d, ok!" % count)

        count = 0.0
        print("Cash Flow Statement updating...")
        for row in sz50_list_code[sz50_list_table.c.code.name]:
            AdminDatabase.update_db_consolidated_statement_data(row, 'Cash')
            print("update :%s OK" % row)
            count = count + 1
            print("Percentage:%.1f%%" % (count / sz50_list_code.size * 100))

        print("Completed files:%d, ok!" % count)

        count = 0.0
        print("Income Statement updating...")
        for row in sz50_list_code[sz50_list_table.c.code.name]:
            AdminDatabase.update_db_consolidated_statement_data(row, 'PL')
            print("update :%s OK" % row)
            count = count + 1
            print("Percentage:%.1f%%" % (count / sz50_list_code.size * 100))

        print("Completed files:%d, ok!" % count)
        return 'Update sz50, done!'


if __name__ == '__main__':
    # AdminDatabase.update_db_consolidated_statement_data('002839','Cash')
    # AdminDatabase.update_data_sz50('2011-01-03')
    # AdminDatabase.update_db_history_data('000004')
    AdminDatabase.update_db_k_data('000002')
