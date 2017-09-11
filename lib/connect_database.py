import pymysql
from sqlalchemy import create_engine


def connect_server():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='york',  # change your username
        passwd='4466',  # change your password
        db='apolo',
        charset='utf8'
    )
    cur = conn.cursor()
    return conn, cur


def connect_engine():
    # change your username
    # change your password
    engine = create_engine('mysql+pymysql://york:4466@localhost/apolo?charset=utf8')
    return engine


def testing():
    print('connect_database.py')


# if __name__ == '__main__':
#     conn, cur = connect_sever()
#     cur.execute("select * from york")
#     result = cur.fetchall()
#     print(result)
#     cur.close()
#     conn.commit()
#     conn.close()
