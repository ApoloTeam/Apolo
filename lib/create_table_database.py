import pymysql
import sqlalchemy
from connect_database import connect_server
from connect_database import connect_engine

conn, cur = connect_server()

def create_table_stock_basics():
    try:
        cur.execute("drop table if exists stock_basics")
        cur.execute("create table stock_basics(code int unsigned, name varchar(20),industry varchar(20), area varchar(20),\
                    pe decimal(8,2),\
                    outstanding decimal(10,2),\
                    totals decimal(10,2),\
                    totalAssets decimal(20,2),\
                    liquidAssets decimal(20,2),\
                    fixedAssets decimal(20,2),\
                    reserved decimal(20,2),\
                    reservedPerShare decimal(10,2),\
                    esp decimal(10,4),\
                    bvps decimal(8,2),\
                    pb decimal(10,2),\
                    timeToMarket int,\
                    undp decimal(20,2),\
                    perundp decimal(8,2),\
                    rev decimal(10,2),\
                    profit decimal(10,2),\
                    gpr decimal(10,2),\
                    npr decimal(10,2),\
                    holders int,\
                    createDate varchar(20))")
    except pymysql.Warning as w:
        print("Warning:%s" % str(w))
    except pymysql.Error as e:
        print("Error %d:%s" % (e.args[0], e.args[1]))

    conn.commit()
    conn.close()

def create_table_report_data():
    try:
        cur.execute("drop table if exists report_data")
        cur.execute("create table report_data(code decimal(7,0) unsigned, name varchar(20),eps decimal(10,4),\
                    eps_yoy decimal(10,2),\
                    bvps decimal(8,2),\
                    roe decimal(8,2),\
                    epcf decimal(8,2),\
                    net_profits decimal(12,2),\
                    profits_yoy decimal(12,2),\
                    distrib varchar(50),\
                    report_date varchar(10),\
                    report_y_q decimal(6,0) unsigned)")
    except pymysql.Warning as w:
        print("Warning:%s" % str(w))
    except pymysql.Error as e:
        print("Error %d:%s" % (e.args[0], e.args[1]))

    conn.commit()
    conn.close()

def create_table_profit_data():
    try:
        cur.execute("drop table if exists profit_data")
        cur.execute("create table profit_data(code decimal(7,0) unsigned, name varchar(20),\
                    roe decimal(8,2),\
                    net_profit_ratio decimal(8,2),\
                    gross_profit_rate decimal(10,4),\
                    net_profits decimal(10,4),\
                    eps decimal(8,4),\
                    business_income decimal(15,4),\
                    bips decimal(8,4),\
                    report_y_q decimal(6,0) unsigned)")
    except pymysql.Warning as w:
        print("Warning:%s" % str(w))
    except pymysql.Error as e:
        print("Error %d:%s" % (e.args[0], e.args[1]))

    conn.commit()
    conn.close()

def create_industry_classified():
    try:
        cur.execute("drop table if exists industry_classified")
        cur.execute("create table industry_classified(code decimal(7,0) unsigned, name varchar(20),\
                    c_name varchar(20),\
                    createDate varchar(20))")
    except pymysql.Warning as w:
        print("Warning:%s" % str(w))
    except pymysql.Error as e:
        print("Error %d:%s" % (e.args[0], e.args[1]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_industry_classified()
