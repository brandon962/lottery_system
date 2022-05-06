from asyncio.windows_events import NULL
from pymongo import MongoClient
from pymongo import UpdateOne
import random
import pymongo


class My_mongodb:
    class My_user:
        def __init__(self, uid, uname):
            self.uid = uid
            self.uname = uname

    class prize_list:
        def __init__(self, uid, uname, prize):
            self.uid = uid
            self.uname = uname
            self.prize = prize

    def get_all_user(self):
        user_list = []
        user = self.all_col.find({}).sort('uid')
        for u in user:
            tmp = self.My_user(u['uid'], u['uname'])
            user_list.append(tmp)
        return user_list

    def get_prize_number(self, num):
        prize_member = []
        luck_member = self.all_col.find({"l_s."+str(self.lottery_name): int(num)}).sort(
            [(self.lottery_name, pymongo.ASCENDING), ("uid", pymongo.ASCENDING)])
        for p in luck_member:
            mem = self.prize_list(p['uid'], p['uname'], p[self.lottery_name])
            prize_member.append(mem)
        return prize_member

    def get_prize_allmember(self):
        prize_member = []
        luck_member = self.all_col.find({"l_s."+str(self.lottery_name): {"$exists":True}}).sort(
            [("l_s."+str(self.lottery_name), pymongo.ASCENDING), ("uid", pymongo.ASCENDING)])
        for p in luck_member:
            mem = self.prize_list(p['uid'], p['uname'], p["l_s"][str(self.lottery_name)])
            prize_member.append(mem)
        return prize_member

    def make_connection(self):
        self.connect = MongoClient(host="192.227.137.66", port=27017)
        self.mydb = self.connect["lottery_db"]
        self.all_col = self.mydb["lottery_member"]
        self.temp_col = self.mydb['lottery_table']

    def clean_temp_col(self):
        self.temp_col.drop()

    def clean_now_lottery(self, lottery_name):
        self.lottery_name = lottery_name
        self.all_col.update_many({}, {"$set": {self.lottery_name: 0}})

    def make_temp_col(self, lottery_name):
        self.lottery_name = lottery_name
        self.clean_temp_col()
        key = self.all_col.find({}, {"uid": 1, "l_s": 2})
        new_col = []
        for member in key:
            member['rand'] = random.uniform(0, 1)
            # member[self.lottery_name] = 0
            member["l_s"] = {self.lottery_name: 0}
            new_col.append(member)
        self.temp_col.insert_many(new_col)
        # self.all_col.update_many({},{"$set":{self.lottery_name:0}})

    def get_lottery(self, lottery_th, lottery_num):
        choose = self.temp_col.find(
            {"l_s."+str(self.lottery_name): lottery_th})
        opera = []

        if choose.count() != 0:
            for c in choose:
                opera.append(UpdateOne({"_id": c["_id"]}, {
                    "$set": {"l_s."+str(self.lottery_name): 0}}))
            self.all_col.bulk_write(opera)
            self.temp_col.bulk_write(opera)

        choose = self.temp_col.find({"l_s."+str(self.lottery_name): 0}).sort(
            "rand").limit(lottery_num)
        opera = []
        for c in choose:
            opera.append(UpdateOne({"_id": c["_id"]}, {
                "$set": {"l_s."+str(self.lottery_name): lottery_th}}))
        self.all_col.bulk_write(opera)
        self.temp_col.bulk_write(opera)


if __name__ == "__main__":
    import time
    a = My_mongodb()
    a.make_connection()
    a.clean_temp_col()
    a.make_temp_col('lottery1')
    t = time.time()
    a.get_lottery(10, 10000)
    tt = time.time()
    print(tt-t)

    t = time.time()
    a.get_lottery(9, 10000)
    tt = time.time()
    print(tt-t)

    t = time.time()
    a.get_lottery(7, 10000)
    tt = time.time()
    print(tt-t)

    t = time.time()
    a.get_lottery(2, 10000)
    tt = time.time()
    print(tt-t)

    a.get_prize_allmember()
