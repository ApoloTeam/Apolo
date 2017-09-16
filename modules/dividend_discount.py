import math
import pandas as pd
import os
import glob
import csv
import numpy as np, matplotlib.pyplot as plt, scipy

import pymysql
import sys

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



