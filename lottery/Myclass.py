# from asyncio.windows_events import NULL
from pymongo import MongoClient
from pymongo import UpdateOne
import random
import pymongo
import os


class My_mongodb:
    class My_group:
        def __init__(self,group_id):
            self.group_id = group_id

    class My_user:
        def __init__(self, uid, uname):
            self.uid = uid
            self.uname = uname

    class prize_list:
        def __init__(self, uid, uname, prize):
            self.uid = uid
            self.uname = uname
            self.prize = prize

    def test(self):
        print(os.getcwd())

    def get_all_group_id(self):
        group_list=[]
        group = self.mydb['lottery_group'].find({})
        for g in group:
            group_list.append(self.My_group(g['group_id']))
        return group_list

    def get_all_user(self):
        user_list = []
        user = self.all_col.find({}).sort('uid')
        for u in user:
            tmp = self.My_user(u['uid'], u['uname'])
            user_list.append(tmp)
        return user_list

    def get_prize_number(self, num):
        prize_member = []
        luck_member = self.all_col.find({"lottery_state."+str(self.lottery_name): int(num)}).sort(
            [(self.lottery_name, pymongo.ASCENDING), ("uid", pymongo.ASCENDING)])
        for p in luck_member:
            mem = self.prize_list(p['uid'], p['uname'], p[self.lottery_name])
            prize_member.append(mem)
        return prize_member

    def get_prize_allmember(self):
        prize_member = []
        luck_member = self.all_col.find({"lottery_state."+str(self.lottery_name): {"$ne": 0}}).sort(
            [("lottery_state."+str(self.lottery_name), pymongo.ASCENDING), ("uid", pymongo.ASCENDING)])
        for p in luck_member:
            mem = self.prize_list(p['uid'], p['uname'],
                                  p["lottery_state"][str(self.lottery_name)])
            prize_member.append(mem)
        return prize_member

    def make_connection(self):
        self.connect = MongoClient(host="127.0.0.1", port=27017)
        self.mydb = self.connect["lottery_db"]
        self.all_col = self.mydb["lottery_member"]
        self.temp_col = self.mydb['lottery_table']

    def clean_temp_col(self):
        self.temp_col.drop()

    def clean_now_lottery(self, lottery_id):
        self.lottery_name = lottery_id
        self.all_col.update_many({}, {"$set": {'lottery_state.'+str(lottery_id): 0}})

    def make_temp_col(self, lottery_id):
        self.lottery_name = lottery_id
        current_lottery_state_field: str = "lottery_state."+self.lottery_name
        self.all_col.update_many(
            {}, {"$set": {current_lottery_state_field: 0}})
        # self.clean_temp_col()
        # key = self.all_col.find({}, {"uid": 1, "lottery_state": 2})
        # new_col = []
        # for member in key:
        #     member['rand'] = random.uniform(0, 1)
        #     # member[self.lottery_id] = 0
        #     member["lottery_state"] = {self.lottery_id: 0}
        #     new_col.append(member)
        # self.temp_col.insert_many(new_col)
        # self.all_col.update_many({},{"$set":{self.lottery_id:0}})

    def get_lottery(self,group_id, lottery_type, lottery_num):
        current_lottery_state_field: str = "lottery_state."+self.lottery_name
        # 清空先前中獎人員
        self.all_col.update_many({current_lottery_state_field: lottery_type}, {
                                 "$set": {current_lottery_state_field: 0}})

        self.all_col.aggregate([{
            # 尋找沒抽過獎的人
            "$match": {'group.'+str(group_id):"1", current_lottery_state_field: 0}
        }, {
            # 隨機抽取
            "$sample": {"size": lottery_num}
        }, {
            # 設定抽獎狀態
            "$set": {current_lottery_state_field: lottery_type}
        }, {
            # 寫回 collection
            "$merge": {"into": 'lottery_member', "on": "_id"}  # Collection to modify
        }
        ])

        # choose = self.temp_col.find({"lottery_state."+str(self.lottery_id): 0}).sort(
        #     "rand").limit(lottery_num)
        # opera = []
        # for c in choose:
        #     opera.append(UpdateOne({"_id": c["_id"]}, {
        #         "$set": {"lottery_state."+str(self.lottery_id): lottery_type}}))
        # self.all_col.bulk_write(opera)
        # self.temp_col.bulk_write(opera)


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
