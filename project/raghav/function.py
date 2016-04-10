import os,tempfile,zipfile
from django.shortcuts import render
# from form import UserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from raghav.models import *
from django.core.mail import send_mail,BadHeaderError
# from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from wsgiref.util import FileWrapper
from project.settings import BASE_DIR
# import mimetype
import csv
import datetime
import soldier
import ipdb

def store_in_NumberList(number,stype,alias,update,now=datetime.datetime.now().date()):
    try:
        # ipdb.set_trace()
        num = NumberList(number=number,stype=stype,alias=alias,update_in=update,processed_date=now)
        num.save()
        return 0
    except :
        return 1

def store_in_Failed_nums(number,stype,alias,pnum,dis):
    try:
        # ipdb.set_trace()
        num = FailedNumbers(number=number,stype=stype,alias=alias,patent_number=pnum,discription=dis)
        num.save()
        return 0
    except :
        return 1


def update_date_query_NumberList(number,now=datetime.datetime.now().date()):
    NumberList.objects.filter(number=number).update(processed_date=now,is_processed=True)
    return 1

def get_is_processed():
    try:
        num     =   NumberList.objects.filter(is_processed=False).values('number','stype','alias')
        return num
    except:
        return 0

def update_processed_in_NumberList(number,d):
    if d == 0:
        NumberList.objects.filter(number=number).update(is_processed=True)
        return 1
    else:
        NumberList.objects.filter(number=number).update(is_processed=False)
        return 1
