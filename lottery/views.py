from asyncio.windows_events import NULL
from collections import UserList
from xml.etree.ElementTree import tostring
from django.shortcuts import render
from djongo import models

from .models import Member
import names
from pymongo import MongoClient
from pymongo import UpdateOne
from .getlottery import My_mongodb
from django.http import HttpResponse


all_user = Member.objects.order_by('uid')[:]
luck_system = My_mongodb()
lottery_name = 'lottery'


def users(request):
    return render(request, 'index.html', {'all_user': all_user})


def welcome(request):
    
    if 'user_name' in request.GET and request.GET['user_name'] != '':
        return HttpResponse('Welcome!~' + request.GET['user_name'])
    else:
        return render(request,'welcome.html',locals())

def myscan(request):
    result = ''
    if request.method == 'POST':
        uid = request.POST.get('uid')
        uname = request.POST.get('uname')
        db = Member()
        db.uid = int(uid)
        db.uname = uname
        db.lottery_state = 0
        db.create_time = models.DateTimeField(auto_now_add=True)
        db.update_time = models.DateTimeField(auto_now=True)
        db.save()
        result = 'success'
        return render(request, 'scan.html', {'result': result})
    else:
        return render(request, 'scan.html')


def add(request):

    db = Member()
    db.uid = str(60000).zfill(10)
    # print(db.uid)
    db.uname = names.get_full_name()
    db.lottery_state = 0
    db.create_time = models.DateTimeField(auto_now_add=True)
    db.update_time = models.DateTimeField(auto_now=True)
    db.save()
    return render(request, 'index.html')


def luck_home(request):
    global luck_system ,lottery_name
    # luck_system = My_mongodb()
    luck_system.make_connection()
    luck_system.clean_temp_col()
    luck_system.make_temp_col(lottery_name)
    print(lottery_name)
    
    return render(request, 'luck_home.html')


def luck_start(request):
    global lottery_name, luck_system
    connect = MongoClient(host="127.0.0.1", port=27017)
    mydb = connect["lottery_db"]
    lottery_col = mydb["lottery_prize"]
    prize = lottery_col.find({}).sort(lottery_name)
    for p in prize:  
        luck_system.get_lottery(p['prize'],p[lottery_name])
    return render(request, 'luck_start.html')



def luck_reset(request):
    global lottery_name
    if request.method == 'POST':
        lottery_name = request.POST.get('lottery_name')
        prize=[]
        for i in range(1,11):
            if request.POST.get('prize_'+str(i)) != '':
                prize.append(int(request.POST.get('prize_'+str(i))))
            else:
                prize.append(0)
        
        connect = MongoClient(host="127.0.0.1", port=27017)
        mydb = connect["lottery_db"]
        lottery_col = mydb["lottery_prize"]
        for i in range(0,len(prize)):
            if lottery_col.find({"prize":i+1}).count() == 0:
                lottery_col.insert_one({"prize":i+1, lottery_name:prize[i]})
            else:
                lottery_col.update_one({"prize":i+1},{"$set":{lottery_name:prize[i]}})        

        return render(request, 'luck_reset.html')
    else:
        return render(request, 'luck_reset.html')