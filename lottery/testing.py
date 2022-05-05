from pymongo import MongoClient


connect = MongoClient(host="127.0.0.1", port=27017)
mydb = connect["lottery_db"]
lottery_col = mydb["lottery_prize"]

# x = lottery_col.find()
# for i in x:
#     print(i)