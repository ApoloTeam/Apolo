import pymysql

connect_server = pymysql.connect(
    host='localhost',
    port=3306,
    user='york',
    passwd='4466',
    db='apolo',
    charset='utf8'
)
cur = connect_server.cursor()

if __name__ == '__main__':
    # cur.execute("insert into york(name) values(%s)",('Chris'))
    cur.execute("select * from york")
    result = cur.fetchall()
    print(result)

    cur.close()
    connect_server.commit()
    connect_server.close()