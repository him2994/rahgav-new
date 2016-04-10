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
from raghav.function import *
# import mimetype
import csv
import datetime
import xlrd
import xlwt
import ipdb
import soldier
from xlutils.copy import copy
from models import *


models_map = {'bibliographicdata': BibliographicData,
 'citations': Citiations,
 'designatedstates': DesignatedStates,
 'documents': Documents,
 'eventhistory': EventHistory,
 'familymember': FamilyMember,
 'fees': Fees,
 'main': Main,
 'parentcontinuity': ParentContinuity,
 'patentfamily': PatentFamily,
 'ptoevent': PtoEvent }

def edit_file_input2():
    num     =   NumberList.objects.filter(is_processed=False).values('number','stype','alias')
    header  =   "Application Number,Type,Alias".split(",")
    with open('script/Input.csv','w') as fil:
        if fil:
            w   =   csv.writer(fil,dialect='excel')
            w.writerow(header)
            for data in num:
                data1=[]
                data1.extend([data['number'],data['stype'],data['alias']])
                w.writerow(data1)
                update_processed_in_NumberList(data['number'],0)
        else:
            print "Error occured"


def edit_file_input3():
    header  =   "Application Number,Type,Alias".split(",")
    #fb      =   open('script/failed_nums.csv','r')
    with open('script/Input.csv','w') as fil:
        if fil:
            w   =   csv.writer(fil,dialect='excel')
            w.writerow(header)
            #data = [row for row in csv.reader(fb.read().splitlines())]
            data = FailedNumbers.objects.all().values('number','stype','alias')
            print data
            i=0;
            for d in data:
                if len(d)>0:
                    if i :
                        print d['number']
                        data1=[]
                        number = d['number']
                        stype  = d['stype']
                        alias  = d['alias']
                        chk = Main.objects.filter(application_number=number)
                        if len(chk) > 0:
                            continue
                        data1.extend([number,stype,alias])
                        w.writerow(data1)
                    else:
                        i=1
        else:
            print "Error occured"
    #fb.close()
    fil.close()


def edit_file_input(num):
    print "num",num
    # num     =   NumberList.objects.filter(is_processed=False).values('number','stype','alias')
    header  =   "Application Number,Type,Alias".split(",")
    with open('script/Input.csv','w') as fil:
        if fil:
            w   =   csv.writer(fil,dialect='excel')
            w.writerow(header)
            print "num1",num
            # for numbe in num:
            #     data1=[]
            #     data1.extend([number,stype,alias])
            #     w.writerow(data1)
            i=0
            while i<len(num):
                num1=num[i:i+3]
                print num1
                w.writerow(num1)
                i+=3
        else:
            print "Error occured"

def add_failed_nums():
    header  =   "Application Number,Type,Alias".split(",")
    with open('script/failed_nums.csv','r') as fil:
        if fil:
            data = [row for row in csv.reader(fil.read().splitlines())]
            i=0;
            for r in data:
                if i :
                    #r=r.split(',')
                    number = r[0]
                    stype  = r[1]
                    alias  = r[2]
                    pnum   = r[3]
                    dis    = r[4]
                    if store_in_Failed_nums(number,stype,alias,pnum,dis) != 0:
                           #update_processed_in_NumberList(number,1)
                           pass
                else:
                    i=1
        else:
            print "Error Occured"
        fil.close()




def add_data():
    # ipdb.set_trace()
    print "add data ---------------------------"
    total_data  =   xlrd.open_workbook('script/Total/data.xlsx')
    # fl          =   open('script/Output/data.xls','r')
    fl = xlrd.open_workbook('script/Output/data.xlsx')
    data = dict()
    data_total = dict()
    sheets = fl.sheets()
    workbook = xlwt.Workbook()

    # ipdb.set_trace()
    for j in range(len(fl.sheets())):
        r_sheet     =   total_data.sheet_by_name(sheets[j].name)

        data[str(sheets[j].name)] = []
        data_total[str(r_sheet.name)] = []
        data_total[str(r_sheet.name)].append( r_sheet.row(0))
        i=1
        # data = [row for row in csv.reader(fl.read().splitlines())]
        # data = []
        while True:
            try:
                data_total[str(r_sheet.name)].append( r_sheet.row(i))
                i = i + 1
            except:
                break

        i=1
        # data = [row for row in csv.reader(fl.read().splitlines())]
        # data = []
        while True:
            try:
                data_total[str(sheets[j].name)].append( sheets[j].row(i))
                # if str(sheets[j].name) == 'Main':
                    # print sheets[j].row(i)
                i = i + 1
            except:
                break
    # ipdb.set_trace()
    # print data_total
    for key,value in data_total.iteritems():
        print key
        sheet = workbook.add_sheet(key)
        table = models_map[key.replace(" ","").lower()]
        table.objects.all().delete()
        # ipdb.set_trace()
        for i in range(0,len(value)):
            try:
                id = table.objects.latest('id').id + 1
            except:
                id = 1
            args = []
            for j in range(len(value[i])):
                x=str(value[i][j])
                #if key == 'Main' and j==1:
                    #ipdb.set_trace()
                    # print x
                if 'text' in x:
                    x = x[7:len(x)-1]
                    sheet.write(i,j,x.decode('unicode-escape'))
                    if not x.decode('unicode-escape') in args:
                        args.append(x.decode('unicode-escape'))
                elif 'empty' in x:
                    x = x[8:len(x)-1]
                    sheet.write(i,j,x.decode('unicode-escape'))
                    if not x.decode('unicode-escape') in args:
                        args.append(x.decode('unicode-escape'))

            if i!=0:
                try:
                    table = table(id, *args)
                    table.save()
                except:
                    pass
                table = models_map[key.replace(" ","").lower()]
    workbook.save('script/Total/data.xlsx')
    print data_total['Main']


def diff_data():
    total_data  =   xlrd.open_workbook('script/Total/data.xlsx')
    # fl          =   open('script/Output/data.xls','r')
    fl = xlrd.open_workbook('script/Output/data.xlsx')
    data = dict()
    data_total = dict()

    # ipdb.set_trace()
    r_sheet     =   total_data.sheet_by_name('Main')
    sheet       =   fl.sheet_by_name('Main')
    data = {}
    data_total = {}
    i=1
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('Main')
    headers = r_sheet.row(0)
    # data = [row for row in csv.reader(fl.read().splitlines())]
    # data = []
    while True:
        try:
            x=str( r_sheet.row(i)[1])
            data_total[x[7:len(x)-1]] = []

            data_total[x[7:len(x)-1]].append( r_sheet.row(i))
            i = i + 1
        except:
            break

    i=1
    # data = [row for row in csv.reader(fl.read().splitlines())]
    # data = []
    while True:
        try:
            x=str( sheet.row(i)[1])
            data[x[7:len(x)-1]] = []

            data[x[7:len(x)-1]].append( sheet.row(i))
            i = i + 1
        except:
            break
    # for row in len(data):
    #     app_id = row[1]

    for i in range(len(headers)):
        x=str(headers[i])
        if 'text' in x:
            x = x[7:len(x)-1]
            sheet1.write(0,i,x.decode('unicode-escape'))
        elif 'empty' in x:
            x = x[8:len(x)-1]
            sheet1.write(0,i,x.decode('unicode-escape'))
    # ipdb.set_trace()

    j=1
    for key,value in data.iteritems():
        # k=0
        sheet1.write(j,1,key)
        # k=k+1
        for i in range(len( data_total[key][0])):
            # l =
            if str(value[0][i]).decode('unicode-escape').split() != str(data_total[key][0][i]).decode('unicode-escape').split():
                print str(data_total[key][0][i]) + " -> " + str(value[0][i])
                sheet1.write(j,i,str(data_total[key][0][i]) + " -> " + str(value[0][i]))
                # k = k + 1
        j = j + 1

    no_ch_sh = ['Main', 'Documents', 'history']
    for sh in fl.sheets():
        x = False
        for s in no_ch_sh:
            if s in str(sh.name):
                x=True
        if not x:
            sh_total = total_data.sheet_by_name(sh.name)
            sh1 = workbook.add_sheet(sh.name)
            if 'PTO' in str(sh.name) or 'MEMBER' in str(sh.name):
                val_update = sh.col_values(1)[1:]
                val_total = sh_total.col_values(1)[1:]
            else:
                val_update = sh.col_values(0)[1:]
                val_total = sh_total.col_values(0)[1:]
            vu = {}
            vt = {}
            for v in val_update:
                if vu.has_key(v):
                    vu[v]+=1
                else:
                    vu[v]=1
            for v in val_total:
                if vt.has_key(v):
                    vt[v]+=1
                else:
                    vt[v]=1
            j=0
            s = set()
            for key,value in vu.iteritems():
                s.add(key)
                sh1.write(j,0,str(key))
                if vt.has_key(key):
                    sh1.write(j,1,str(vt[key]) + " -> " + str(value))
                else:
                    sh1.write(j,1,str(0) + " -> " + str(value))
                j=j+1
            for key,value in vt.iteritems():
                if key not in s:
                    sh1.write(j,0,str(key))
                    if vu.has_key(key):
                        sh1.write(j,1,str(value) + " -> " + str(vu[key]))
                    else:
                        sh1.write(j,1,str(value) + " -> " + str(0))
                    j=j+1

    ch_sh = ['Documents', 'history']
    for sh in fl.sheets():
        x = False
        for s in ch_sh:
            if s in str(sh.name):
                x=True
        if x:
            sh_total = total_data.sheet_by_name(sh.name)
            sh1 = workbook.add_sheet(sh.name)
            if 'Documents' in str(sh.name):
                val_update = [(sh.col_values(0)[i+1],sh.col_values(1)[i+1]) for i in range(len(sh.col_values(0))-1)]
                val_total = [(sh_total.col_values(0)[i+1],sh_total.col_values(1)[i+1]) for i in range(len(sh_total.col_values(0))-1)]
            else:
                val_update = [(sh.col_values(0)[i+1],sh.col_values(2)[i+1]) for i in range(len(sh.col_values(0))-1)]
                val_total = [(sh_total.col_values(0)[i+1],sh_total.col_values(2)[i+1]) for i in range(len(sh_total.col_values(0))-1)]
            vu = {}
            vt = {}
            for v in val_update:
                if vu.has_key(v):
                    vu[v]+=1
                else:
                    vu[v]=1
            for v in val_total:
                if vt.has_key(v):
                    vt[v]+=1
                else:
                    vt[v]=1
            j=0
            s = set()
            for key,value in vu.iteritems():
                s.add(key)
                sh1.write(j,0,str(key))
                if vt.has_key(key):
                    sh1.write(j,1,str(vt[key]) + " -> " + str(value))
                else:
                    sh1.write(j,1,str(0) + " -> " + str(value))
                j=j+1
            for key,value in vt.iteritems():
                if key not in s:
                    sh1.write(j,0,str(key))
                    if vu.has_key(key):
                        sh1.write(j,1,str(value) + " -> " + str(vu[key]))
                    else:
                        sh1.write(j,1,str(value) + " -> " + str(0))
                    j=j+1

    workbook.save('script/update/data.xlsx')
        # print key
    # print data_total
