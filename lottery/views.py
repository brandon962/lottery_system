from asyncio.windows_events import NULL
from collections import UserList
from xml.etree.ElementTree import tostring
from django.shortcuts import render
from djongo import models
from .models import Member, lottery
from .models import User_py
import random
import names
from pymongo import MongoClient
from pymongo import UpdateOne
import time
from .getlottery import My_mongodb


all_user = Member.objects.order_by('uid')[:]
luck_system = My_mongodb()

def users(request):
    return render(request, 'index.html', {'all_user': all_user})


from django.http import HttpResponse
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
    # luck_system = My_mongodb()
    luck_system.make_connection()
    luck_system.clean_temp_col()
    luck_system.make_temp_col('lottery')
    if 'type' in request.POST and request.POST['type']=='start':
        # luck_system.get_lottery(2,100)
        luck_start(request)
        return render(request, 'luck_start.html')
    else:
        return render(request, 'luck_home.html')


def luck_start(request):
    luck_system.get_lottery(2,100)
    return render(request, 'luck_start.html')