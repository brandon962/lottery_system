from multiprocessing import allow_connection_pickling
from pymongo import MongoClient
from pymongo import UpdateOne
import random
import pymongo
import csv
import json
import pandas
import names

connect = MongoClient(host="127.0.0.1", port=27017)
mydb = connect["lottery_db"]
all_col = mydb["lottery_member"]
temp_col = mydb['lottery_table']
test_col = mydb['testing']
group_col = mydb['lottery_group']

add = []
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    add.append(['uid','uname'])
    for i in range(60000,120000):
        add.append([str(i),names.get_full_name()])
    writer.writerows(add)
