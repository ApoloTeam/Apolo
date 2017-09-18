from Apolo.modules.connect_database import connect_server

conn, cur = connect_server()

def testing():
    cur.execute("select * from test")
    result = cur.fetchall()
    print(result)

if __name__ == '__main__':
    # cur.execute("insert into york(name) values(%s)",('Chris'))
    testing()
