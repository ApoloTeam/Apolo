import pymysql
from sqlalchemy import create_engine

def connect_server():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='york',
        passwd='4466',
        db='apolo',
        charset='utf8'
    )
    cur = conn.cursor()
    return conn,cur


def connect_engine():
    engine = create_engine('mysql+pymysql://york:4466@localhost/apolo?charset=utf8')
    return engine

def testing():
    print('connect_database.py')


# if __name__ == '__main__':
#     conn, cur = connect_sever()
#     cur.execute("select * from york")
#     result = cur.fetchall()
#     print(result)
#
#     cur.close()
#     conn.commit()
#     conn.close()