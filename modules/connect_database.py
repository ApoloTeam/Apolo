import pymysql
from sqlalchemy import create_engine
from modules.config import Config


class ConnectDatabase:
    """
    This class is used to connect to mysql server and
    select, insert, delete data
    """
    def __init__(self):
        # get the user configuration of db info:
        user_config = Config()
        user_db_param = user_config.get_config_db_info()
        self.db_host = user_db_param['host']
        self.db_port = user_db_param['port']
        self.db_user = user_db_param['user']
        self.db_pass = user_db_param['pass']

    def create_db_engine(self):  # db_name=''
        #  connect to mysql server
        engine = create_engine(
                                'mysql+pymysql://' + self.db_user
                                + ':' + self.db_pass
                                + '@' + self.db_host
                                + ':' + self.db_port
                                + '/' + 'apolo'
                                + '?charset=utf8'
                                )  # use mysqlconnector to connect db
        # print("engine:" + db_name + ' OK')
        return engine

    def connect_server(self):
        conn = pymysql.connect(
            host=self.db_host,
            port=int(self.db_port),
            user=self.db_user,
            passwd=self.db_pass,
            db='apolo',
            charset='utf8'
        )
        cur = conn.cursor()
        return conn, cur

    def testing_engine(self):
        print(self.create_db_engine())

    def testing_server(self):
        conn, cur = self.connect_server()
        cur.execute("select * from test")
        print(cur.fetchall())


if __name__ == '__main__':
    test = ConnectDatabase()
    test.testing_engine()
    test.testing_server()
