from modules.create_table import CreateTable
from modules.admin_database import AdminDatabase

# get hs300 list
hs300_list_table = CreateTable.create_table_hs300_list()
hs300_list_code = AdminDatabase.get_table_data(hs300_list_table.name, [hs300_list_table.c.code.name])
count = 0.0
for row in hs300_list_code[hs300_list_table.c.code.name]:
    AdminDatabase.update_db_k_data(row)
    print("update :%s OK" % row)
    count = count + 1
    print("Percentage:%.1f%%" % (count / hs300_list_code.size*100))

print("Completed files:%d" % count)
print("Ok!") 
