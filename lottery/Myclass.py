# from asyncio.windows_events import NULL
from pymongo import MongoClient
from pymongo import UpdateOne
import random
import pymongo
import os


class My_mongodb:
    # some class for struct
    class My_group:
        def __init__(self, group_id):
            self.group_id = group_id

    class My_user:
        def __init__(self, uid, uname):
            self.uid = uid
            self.uname = uname

    class My_prize:
        def __init__(self, uid, uname, prize):
            self.uid = uid
            self.uname = uname
            self.prize = prize

    class My_lottery:
        def __init__(self, lottery_name):
            self.lottery_name = lottery_name

    class My_prize_list:
        def __init__(self, prize):
            self.prize = prize

    # return class-list from mongodb
    def get_prize_list(self):
        prize_list = []
        prize = self.mydb['lottery_prize'].find({})
        prize_list.append(self.My_prize_list('all'))
        for p in prize:
            prize_list.append(self.My_prize_list(str(p['prize'])))
        return prize_list

    # return class-list from mongodb
    def get_all_lottery_name(self):
        lottery_list = []
        lottery = self.mydb['lottery_name'].find({})
        for l in lottery:
            lottery_list.append(self.My_lottery(l['lottery_name']))
        return lottery_list

    # return class-list from mongodb
    def get_all_group_id(self):
        group_list = []
        group = self.mydb['lottery_group'].find({})
        for g in group:
            group_list.append(self.My_group(g['group_id']))
        return group_list

    # return class-list from mongodb
    def get_all_user(self):
        user_list = []
        user = self.all_col.find({}).sort('uid')
        for u in user:
            tmp = self.My_user(u['uid'], u['uname'])
            user_list.append(tmp)
        return user_list

    # return class-list from mongodb
    def get_prize_number(self, num):
        prize_member = []
        luck_member = self.all_col.find({"lottery_state."+str(self.lottery_name): num}).sort(
            [("lottery_state."+str(self.lottery_name), pymongo.ASCENDING), ("uid", pymongo.ASCENDING)])
        for p in luck_member:
            mem = self.My_prize(p['uid'], p['uname'],
                                p["lottery_state"][str(self.lottery_name)])
            prize_member.append(mem)
        return prize_member

    # return class-list from mongodb
    def get_prize_allmember(self):
        prize_member = []
        luck_member = self.all_col.find({"lottery_state."+str(self.lottery_name): {"$gt": 0}}).sort(
            [("lottery_state."+str(self.lottery_name), pymongo.ASCENDING), ("uid", pymongo.ASCENDING)])
        for p in luck_member:
            mem = self.My_prize(p['uid'], p['uname'],
                                p["lottery_state"][str(self.lottery_name)])
            prize_member.append(mem)
        return prize_member

    # make connection to mongodb
    def make_connection(self):
        self.connect = MongoClient(host="127.0.0.1", port=27017)
        self.mydb = self.connect["lottery_db"]
        self.all_col = self.mydb["lottery_member"]
        self.temp_col = self.mydb['lottery_table']

    # clean the lottery with lottery_name
    def clean_now_lottery(self, lottery_name):
        self.lottery_name = lottery_name
        self.all_col.update_many(
            {}, {"$set": {'lottery_state.'+str(lottery_name): 0}})

    # starting lottery one by one prize
    def get_lottery(self, group_id, lottery_type, lottery_num):
        current_lottery_state_field: str = "lottery_state."+self.lottery_name
        # clean the people how have won the prize
        self.all_col.update_many({current_lottery_state_field: lottery_type}, {
                                 "$set": {current_lottery_state_field: 0}})

        self.all_col.aggregate([{
            # find the people didn't win prize yet
            "$match": {'group.'+str(group_id): "1", current_lottery_state_field: 0}
        }, {
            # random get people
            "$sample": {"size": lottery_num}
        }, {
            # setting prize state
            "$set": {current_lottery_state_field: lottery_type}
        }, {
            # Collection to modify
            "$merge": {"into": 'lottery_member', "on": "_id"}
        }
        ])
