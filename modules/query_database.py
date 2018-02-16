from sqlalchemy import select ,MetaData, Table, Column, Integer, String, Date, DECIMAL, \
    PrimaryKeyConstraint, and_, or_, not_, between
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base
from modules.connect_database import ConnectDatabase
from modules.create_table import CreateTable
import datetime as dt

Base = declarative_base()


class TEST:
    metadata = MetaData()
    connection = ConnectDatabase()
    engine = connection.create_db_engine()


class KDATA(object):
    __table_args__ = {"useexisting": True}

    def __init__(self, date, open, close, high, low, volume, code):
        self.date = date
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.code = code


class QueryDatabase:
    connection = ConnectDatabase()
    engine = connection.create_db_engine()
    con, cur = connection.connect_server()
    db_session = sessionmaker(bind=engine)
    Session = db_session()
    engine = connection.create_db_engine()
    metadata = MetaData(engine)
    users = Table('k_data', metadata, autoload=True)

    @classmethod
    def get_k_value(cls, stock_code, date):
        # Method 1
        # map_k_data = CreateTable.create_table_k_data()
        # mapper(KDATA, map_k_data)
        # values = cls.Session.query(KDATA).filter_by(code=stock_code, date=date).first()
        # cls.Session.close()
        # return values.close

        # Method 2
        select_sql = [cls.users.columns.close]
        where_sql = and_(cls.users.columns.code == stock_code, cls.users.columns.date == dt.datetime.strptime(date,'%Y-%m-%d'))
        sql = select(select_sql).where(where_sql)
        values = sql.execute()
        for value in values:
            return float(value[0])

    @classmethod
    def get_k_value_period(cls, stock_code, start_date, end_date):
        arr_values = []
        arr_index = []
        select_sql = [cls.users.columns.close]
        where_sql = and_(cls.users.columns.code == stock_code,
                         between(cls.users.columns.date, dt.datetime.strptime(start_date, '%Y-%m-%d'),
                                 dt.datetime.strptime(end_date, '%Y-%m-%d')))
        sql = select(select_sql).where(where_sql)
        values = sql.execute()
        for value in values:
            arr_values.append(float(value[0]))

        from_day = dt.datetime.strptime(start_date, '%Y-%m-%d').day
        to_day = dt.datetime.strptime(end_date, '%Y-%m-%d').day
        for day in range(int(from_day), int(to_day)+1):
            arr_index.append(day)
        print(arr_index)
        return arr_values, arr_index


if __name__ == "__main__":
    print(QueryDatabase.get_k_value_period("000001", "2018-01-22", "2018-01-25"))
#     print(QueryDatabase.get_k_value("000001", "1991-04-06"))
