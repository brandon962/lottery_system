from pymongo import MongoClient
from pymongo import UpdateOne
import random

class My_mongodb:
    def make_connection(self):
        self.connect = MongoClient(host="127.0.0.1", port=27017)
        self.mydb = self.connect["lottery_db"]
        self.all_col = self.mydb["lottery_member"]
        self.temp_col = self.mydb['lottery_table']

    def clean_temp_col(self):
        self.temp_col.drop()

    def make_temp_col(self, lottery_name):
        self.lottery_name = lottery_name
        self.clean_temp_col()
        key = self.all_col.find({}, {"uid": 1, self.lottery_name: 2})
        new_col = []
        for member in key:
            member['rand'] = random.uniform(0, 1)
            member[self.lottery_name] = 0
            new_col.append(member)
        self.temp_col.insert_many(new_col)
        self.all_col.update_many({},{"$set":{lottery_name:0}})

    def get_lottery(self, lottery_th, lottery_num):
        choose = self.temp_col.find({self.lottery_name: 0}).sort(
            "rand").limit(lottery_num)
        opera = []
        for c in choose:
            opera.append(UpdateOne({"_id": c["_id"]}, {
                "$set": {self.lottery_name: lottery_th}}))
        self.all_col.bulk_write(opera)
        self.temp_col.bulk_write(opera)

if __name__ == "__main__":
    import time
    a = My_mongodb()
    a.make_connection()
    a.clean_temp_col()
    a.make_temp_col('lottery1')
    t = time.time()
    a.get_lottery(10,10000)
    tt = time.time()
    print(tt-t)

    t = time.time()
    a.get_lottery(9,10000)
    tt = time.time()
    print(tt-t)

    t = time.time()
    a.get_lottery(7,10000)
    tt = time.time()
    print(tt-t)

    t = time.time()
    a.get_lottery(2,10000)
    tt = time.time()
    print(tt-t)