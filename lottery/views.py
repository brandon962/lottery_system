# from asyncio.windows_events import NULL
from collections import UserList
from turtle import update
from xml.etree.ElementTree import tostring
from django.shortcuts import render, redirect
from djongo import models
import os
from .models import Member, Document, testing
import names
from pymongo import MongoClient
from pymongo import UpdateOne
from .Myclass import My_mongodb
from django.http import HttpResponse
import json
import pandas

# all_user = Member.objects.order_by('uid')[:]

luck_system = My_mongodb()
lottery_name = 'origin'
group_id = 1

def users(request):
    global luck_system
    luck_system.make_connection()
    luck_system.lottery_name = lottery_name
    # all_user = Member.objects.order_by('uid')[:]

    # return render(request, 'index.html', {'all_user': all_user})
    # return render(request)
    return render(request, 'index.html', {"all_user": luck_system.get_all_user()})


def welcome(request):

    if 'user_name' in request.GET and request.GET['user_name'] != '':
        return HttpResponse('Welcome!~' + request.GET['user_name'])
    else:
        return render(request, 'welcome.html', locals())


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
    global luck_system, lottery_name
    # luck_system = My_mongodb()
    luck_system.make_connection()
    luck_system.lottery_name = lottery_name

    # print(lottery_name)

    if request.method == 'POST':
        if 'start_lottery' in request.POST:
            luck_system.make_temp_col(lottery_name)
            return redirect("/luck_start")

        if 'lottery_clear' in request.POST:
            luck_system.clean_now_lottery(lottery_name)
            # luck_system.clean_temp_col()
    print(lottery_name)
    return render(request, 'luck_home.html', {"ln": lottery_name,'all_group':luck_system.get_all_group_id()})


def luck_start(request):
    global lottery_name, luck_system, group_id
    # luck_system.make_temp_col(lottery_name)
    connect = MongoClient(host="127.0.0.1", port=27017)
    mydb = connect["lottery_db"]
    lottery_col = mydb["lottery_prize"]
    tmp = lottery_col.find({}).sort('prize')
    prize = []
    for t in tmp:
        prize.append(t[lottery_name])
    if request.method == 'POST':
        # print(request.POST)
        if 'prize_all' in request.POST:
            for i in range(1, 11):
                luck_system.get_lottery(group_id, i, prize[i-1])
            return redirect("/look_prize")

        for i in range(1, 11):
            if 'prize_'+str(i) in request.POST:
                luck_system.get_lottery(group_id, i, prize[i-1])
                return redirect("/look_prize")
        return render(request, 'luck_start.html')
    else:
        return render(request, 'luck_start.html')


def luck_reset(request):
    global lottery_name, luck_system, group_id
    if request.method == 'POST':

        lottery_name = request.POST.get('lottery_name')
        luck_system.mydb['lottery_id'].insert_one({'lottery_id':lottery_name})
        prize = []
        for i in range(1, 11):
            if request.POST.get('prize_'+str(i)) != '':
                prize.append(int(request.POST.get('prize_'+str(i))))
            else:
                prize.append(0)

        connect = MongoClient(host="127.0.0.1", port=27017)
        mydb = connect["lottery_db"]
        lottery_col = mydb["lottery_prize"]
        for i in range(0, len(prize)):
            if lottery_col.find({"prize": i+1}).count() == 0:
                lottery_col.insert_one({"prize": i+1, lottery_name: prize[i]})
            else:
                lottery_col.update_one(
                    {"prize": i+1}, {"$set": {lottery_name: prize[i]}})
        luck_system.clean_now_lottery(lottery_name)
        return render(request, 'luck_reset.html', {'member_count': luck_system.all_col.find({"group."+str(group_id):"1"}).count(),'group_id':group_id})
    else:
        return render(request, 'luck_reset.html', {'member_count': luck_system.all_col.find({"group."+str(group_id):"1"}).count(),'group_id':group_id})


def look_home(request):
    global luck_system
    
    return render(request, 'look_home.html')


def look_prize_single(request):
    global luck_system
    pass
    return render(request)


def look_prize(request):
    global luck_system
    prize_member = luck_system.get_prize_allmember()
    # return render(request, 'index.html', {'all_user': all_user})
    return render(request, 'look_prize.html', {'prize_member': prize_member})


def uploadFile(request):
    global group_id
    if request.method == "POST":
        # Fetching the form data
        # fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        # document = Document(
        #     title=fileTitle,
        #     uploadedFile=uploadedFile
        # )
        # document.save()
        # print(uploadedFile.name)
        # return render(request, "upload_file.html")
        
        csv_name = os.path.join('media','UploadedFiles',uploadedFile.name)
        data = pandas.read_csv(csv_name,encoding = 'UTF-8')
        data_json = json.loads(data.to_json(orient='records'))
        msg =[]
        testcol = luck_system.all_col
        opera=[]    
        opera2=[]    
        group_id = luck_system.mydb['lottery_group'].count()+1
        luck_system.mydb['lottery_group'].insert_one({'group_id':group_id})
        all_tmp = testcol.find({})
        all_uid = {}
        for a in all_tmp:
            all_uid[a['uid']]={'group':a['group'],'_id':a['_id']}

        for d in data_json:
            if d['uid'] in all_uid:
                if str(group_id) in all_uid[d['uid']]['group']:
                    msg.append('Same group.')
                else:
                    opera2.append(UpdateOne({'_id':all_uid[d['uid']]['_id']},{'$set':{'group.'+str(group_id):'1'}}))
            else:
                opera.append({'uid':d['uid'],'uname':d['uname'],'group': {str(group_id): '1'}})

        if len(opera)>0 :
            testcol.insert_many(opera)
        if len(opera2) > 0:
            testcol.bulk_write(opera2)
        
        os.remove(csv_name)
        return redirect('/luck_reset')
    return render(request, "upload_file.html")


def select_group(request):
    global luck_system, group_id
    for p in luck_system.get_all_group_id():
        print(p.group_id)
    if request.method == "POST":
        print(request.POST)
        if 'upload' in request.POST:
            return redirect("/upload_file")
        for i in luck_system.get_all_group_id():
            if str(i.group_id) in request.POST['group_id']:
                group_id = i.group_id
                return redirect("/luck_reset")
        return render(request, 'select_group.html', {'all_group':luck_system.get_all_group_id()})
        

    return render(request, 'select_group.html', {'all_group':luck_system.get_all_group_id()})