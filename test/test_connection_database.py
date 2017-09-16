from Apolo.modules.connect_database import connect_server

conn, cur = connect_server()

if __name__ == '__main__':
    # cur.execute("insert into york(name) values(%s)",('Chris'))
    cur.execute("select * from test")
    result = cur.fetchall()
    print(result)

    cur.close()
    conn.commit()
    conn.close()
