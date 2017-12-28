import math
import pandas as pd
import os
import glob
import csv
import numpy as np, matplotlib.pyplot as plt, scipy

from modules.connect_database import ConnectDatabase

connection = ConnectDatabase()
conn, cur = connection.connect_server()

if __name__ == '__main__':
    # cur.execute("insert into york(name) values(%s)",('Chris'))
    cur.execute("select * from york")
    result = cur.fetchall()
    print(result)

    cur.close()
    conn.commit()
    conn.close()
