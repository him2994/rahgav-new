import os,tempfile,zipfile
from django.shortcuts import render
# from form import UserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from raghav.models import Ruser,NumberList,Email
from django.core.mail import send_mail,BadHeaderError
from django.core.mail import EmailMessage
# from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from wsgiref.util import FileWrapper
from project.settings import BASE_DIR
from raghav.function import *
from raghav.file_manage import *
# import mimetype
import csv
import datetime
import time
import soldier
import ipdb
from threading import Thread
from config import *


def index(request):

    if request.method == 'POST':
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)
        try:

            user=authenticate(username=username,password=password)
        except:
            return render(request,"raghav/index.html",{"status":"login error occured"})

        if user:
            print "here"
            login(request,user)
            # return render(request,"raghav/dashboard.html",{})
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request,"raghav/index.html",{})
    else:
        print "here 3"

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request,"raghav/index.html",{})


def dashboard(request):
    # ipdb.set_trace()
    if request.user.is_authenticated():
         if request.FILES:
             csvfile = request.FILES['csv_file']
             print csvfile
             print request.POST["time"]
             tt = int(request.POST['anotherTime']) # will be request.POST after wards
             data = [row for row in csv.reader(csvfile.read().splitlines())]
             i=0;
             for app_number,s_type,n_alias in data:
                 if i :
                     number = app_number
                     stype  = s_type
                     alias  = n_alias
                     update = request.POST["time"]
                     try:
                         if store_in_NumberList(number,stype,alias,update) == 0 :
                             print "as"
                             pass
                     except:
                         return render(request,"raghav/dashboard.html",{"status" : "Duplicate number "+number+"."})
                 else:
                     i=1
             edit_file_input2()
             print "here"
             thread = Thread(target=run_script,args=(data,tt*60,1,))
             thread.daemon = True
             thread.start()

             print "here 2"

             return render(request,"raghav/dashboard.html",{"status" : "Application number successfully Queued for processing. You will get the update through email."})


         elif request.method == "POST":
             try:
                 print request.POST["number"]
                 number = request.POST["number"]
                 stype  = request.POST["type"]
                 alias  = request.POST["alias"]
                 update = request.POST["time"]
             except:
                 return render(request,"raghav/dashboard.html",{"status" : "Some Inputs empty or not filled correctly"})
             if store_in_NumberList(number,stype,alias,update) != 0:
                    return render(request,"raghav/dashboard.html",{"status" : "Duplicate number."})
             else:
                    edit_file_input2()
                    update_processed_in_NumberList(number,0)
                    # run_script()
                    fb      =   open('script/Input.csv','r')
                    data = [row for row in csv.reader(fb.read().splitlines())]
                    print data
                    try:
                        tt = int(request.POST['anotherTime1'])
                    except:
                        return render(request,"raghav/dashboard.html",{"status" : "Some Inputs empty or not filled correctly"})
                    thread = Thread(target=run_script,args=(data,tt*60,1,))
                    thread.daemon = True
                    thread.start()
                    # add_data()
                    return render(request,"raghav/dashboard.html",{"status" : "Application number successfully Queued."})

         else:
             return render(request,"raghav/dashboard.html",{})
    else:
        return HttpResponseRedirect(reverse('login'))



def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def add_emails(request):
    if request.user.is_authenticated():
         if request.method == "POST":
             try:
                 email  = request.POST["email"]
                 name = request.POST["name"]
             except:
                 return render(request,"raghav/emails.html",{"status" : "Some input empty or not filled correctly."})
             add_email = Email(email=email,name=name)
             add_email.save()
             return render(request,"raghav/emails.html",{"status" : "Email successfully added."})
         else:
             return render(request,"raghav/emails.html",{})
    else:
        return HttpResponseRedirect(reverse('login'))

def del_emails(request):
    if request.user.is_authenticated():
         if request.method == "POST":
             for email  in request.POST.getlist("email"):
                print email
                del_email = Email.objects.get(email=email)
                del_email.delete()
             return render(request,"raghav/dashboard.html",{"status" : "Email successfully deleted."})
         else:
             email = Email.objects.all()
             print email
             return render(request,"raghav/del_emails.html",{"email":email})
    else:
        return HttpResponseRedirect(reverse('login'))



def check_updates():
    now     = datetime.datetime.now().date()
    numbers = NumberList.objects.all()
    tobe_update =[]
    # print numbers
    for data in numbers:
        print data.processed_date
        print now - data.processed_date
        if (now - data.processed_date).days == data.update_in:
            tobe_update.extend([data.number,data.stype,data.alias])
            update_date_query_NumberList(data.number,now)
    # print tobe_update[1].processed_date
    print "here1"
    print "tobeupdate",tobe_update
    edit_file_input(tobe_update)
    thread = Thread(target=update_thread)
    thread.daemon = True
    thread.start()
    return render(request,"raghav/dashboard.html",{})


def update_thread():
    run_script()
    diff_data()
    send_emails("update")

def send_emails(r):
    To  = Email.objects.all()
    from_email = Email_USER
    job = soldier.run('cp script/update/data.xlsx > script/update/data.xls')
    print job.output
    job = soldier.run('cp script/Total/data.xlsx > script/Total/data.xls')
    print job.output
    job = soldier.run('cp script/Output/data.xlsx > script/Output/data.xls')
    print job.output
    # for email,name in to:
    if r == 'add':
        # print to[0].name
        try:
            for to in To:
                send_mail("check","Hello "+to.name+" you are registered for email update.",from_email,[to.email])
            print "Mail sent"
        except BadHeaderError:
            return "Invalide Header Found"
    elif r == 'add':
        # print to[0].name
        try:
            for to in To:
                send_mail("check","Hello "+to.name+" you are unsubscribed for email update.",from_email,[to.email])
            print "Mail sent"
        except BadHeaderError:
            return "Invalide Header Found"
    elif r == 'update':
        # print to[0].name
        try:
            for to in To:
                email   =   EmailMessage("Difference in data.xls","Hello, "+to.name+".This is the data.xls file contain difference",from_email,[to.email])
                # send_mail("check","Hello "+to.name,from_email,[to.email])
                email.attach_file('script/update/data.xls')
                email.attach_file('script/Output/data.xls')
                try:
                    email.send()
                    print "Mail sent"
                except:
                    print "Mail not sent"
        except BadHeaderError:
            return "Invalide Header Found"

    else:
        try:
            for to in To:
                email   =   EmailMessage("data.xls","Hello, "+to.name+".This is the data.xls file",from_email,[to.email])
                # send_mail("check","Hello "+to.name,from_email,[to.email])
                email.attach_file('script/Total/data.xls')
                email.attach_file('script/failed_nums.csv')
                try:
                    email.send()
                    print "Mail sent"
                except:
                    print "Mail not sent"
        except BadHeaderError:
            return "Invalide Header Found"

def run(request):
    edit_file_input3()
    run_script()
    # add_data()
    return HttpResponseRedirect(reverse('dashboard'))



def download(request,filename):
    if filename == "failed_nums":
        filename    =   "script/"+filename+".csv"
        download_name   =   "failed_nums.csv"
        content_type    =   'text/csv'
    else:
        filename    =   "script/Total/"+filename+".xlsx"
        download_name   =   "data.xls"
        content_type    =   'text/xls'
    Wrapper         =   FileWrapper(open(filename))
    response        =   HttpResponse(Wrapper,content_type=content_type)
    response['Content-Length']= os.path.getsize(filename)
    response['Content-Disposition']="attachment;filename=%s"%download_name
    return response



def run_script(data=[],tt=0,email=0):
    while os.path.isfile('script/lock'):
        continue
    if len(data) == 0:
        f = open("script/Input.csv","rb")
        r = csv.reader(f)
        for row in r:
            x.append( ', '.join(row))
        data = x
        # x = f.readlines()
        # x = x[1:]
        # data = x
    # ipdb.set_trace()
    try:
        a=soldier.run('touch script/lock')
        header  =   "Application Number,Type,Alias".split(",")
        fb      =   open('script/ready_nums.csv','w')
        w       =   csv.writer(fb,dialect='excel')
        w.writerow(header)
        fb.close()
        cnt = 1
        print 'len ==== ' + str(len(data))
        while cnt<len(data):
            try:
                os.remove(os.path.join(os.path.join(os.path.join(BASE_DIR,"script"),"Output"),"data.xlsx"))
            except:
                pass
            fb      =   open('script/Input.csv','w')
            w       =   csv.writer(fb,dialect='excel')
            w.writerow(header)
            for i in range(cnt,min(cnt+10,len(data))):
                w.writerow(data[i])
            cnt+=10
            fb.close()
            out = soldier.run('cat script/Input.csv')
            print out.output

            job     =   soldier.run('python3 script/patent.py')
            print job.output
            print job.is_alive()
            print "here"
            try:
                if email == 1:
                    print "run add data"
                    add_data()
                else:
                    diff_data()
            except:
                pass
            time.sleep(tt)
        a=soldier.run('rm script/lock')
    except:
        a=soldier.run('rm script/lock')
    if email == 1:
        send_emails("send")

    add_failed_nums()

    return
