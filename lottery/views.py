from collections import UserList
from xml.etree.ElementTree import tostring
from django.shortcuts import render
from djongo import models
from .models import Member
from .models import User_py
import random
import names
def user(request):
    all_user = Member.objects.all()
    
    return render(request,'index.html',{'all_user':all_user,})

def scan(request):
    result=''
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
        return render(request,'scan.html',{'result':result})
    else:
        return render(request, 'scan.html')


def add(request):
    
    db = Member()
    db.uid =str(60000).zfill(10)
    # print(db.uid)    
    db.uname = names.get_full_name()
    db.lottery_state = 0
    db.create_time = models.DateTimeField(auto_now_add=True)
    db.update_time = models.DateTimeField(auto_now=True)
    db.save()
    return render(request,'index.html')

def luck(request):
    all_user = Member.objects.all()
    user_list=[]
    print(all_user)
    for user in all_user:
        temp_user = User_py()
        temp_user.__inti__(user.id, user.uid, user.uname, 0)
        print(user.id)
        print(user.uid)
        print(user.uname)
        print()
        user_list.append(temp_user)
    
    print([u.id for u in user_list])
    random.shuffle(user_list)
    print([u.id for u in user_list])
    for i in range(10000):
        temp_user = Member.objects.get(id=user_list[i].id)
        temp_user.lottery_state = 1
        temp_user.save()
    return render(request, 'luck.html')
# Create your views here.
