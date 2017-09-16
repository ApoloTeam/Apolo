from Apolo.modules.connect_database import connect_server

conn, cur = connect_server()

TBL_TEST = "create table test(name varchar(20))"

cur.execute(TBL_TEST)
conn.commit()
conn.close()
