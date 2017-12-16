#encoding:utf-8
import pandas as pd
from modules import db_connector

#import sys
#sys.path.append('../')


DB = db_connector.Db_connector()
#get hs300 list
hs300_list_table = DB.table_creator.get_table_hs300_list()
hs300_list_code = DB.get_table_data(DB.str_db_stock_classification,hs300_list_table.name,
                                          [hs300_list_table.c.code.name])
#print(hs300_list_code)
count = 0.0
for row in hs300_list_code[hs300_list_table.c.code.name]:
    DB.update_db_history_data(row)
    print("update :%s OK"%row)
    count = count + 1
    print("Percentage:%.1f%%"%(count/hs300_list_code.size*100))

print("Completed files:%d"%count)
print("Ok!") 

