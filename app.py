# coding:utf-8
import os, io
import codecs
import flask
from flask import render_template
import time
import json
import eftmqtt
from flask_script import Manager
from livereload import Server
from flask_apscheduler import APScheduler

import threading
import pwmeter
import ACCtrl
import ipcInfor
import trymqtt
import findtoken
import ipcalert
import CtrlMode
import opentime


a = [0,0,0,0,0,0,0]
app = flask.Flask(__name__)
manager = Manager(app)

PWClast_status = 0
PW_dem_flag = 0
PW_dem_last = 0
PW_demandcal_15m = 0
PW_demandcal_1h = 0
ts_last = 0
#ipc_token = '2419-IPC000-23B672B2'


class Config(object):
    JOBS = [
        {
            'id': 'read_MEinfor',
            'func': '__main__:read_MEinfor',
            'args': (4, 5),
            'trigger': 'interval',
            'minutes': 2
        },
        {
            'id': 'read_ACinfor',
            'func': '__main__:read_ACinfor',
            'args': (4, 5),
            'trigger': 'interval',
            'minutes': 2
        },
        {
            'id': 'demandcal',
            'func': '__main__:demandcal',
            'args': (1, 2),
            'trigger': 'interval',
            'minutes': 15
        },
        {
            'id': 'AutoCtrl',
            'func': '__main__:AutoCtrl',
            'args': (1, 2),
            'trigger': 'interval',
            'minutes': 15
        }
    ]

def read_MEinfor(a, b): # send data to cloud
    MeterPORT = '/dev/ttyS1'
    ACPORT = '/dev/ttyS4'
    MainPW_ID = 1
    AC01PW_ID = 2
    AC02PW_ID = 3
    AC03PW_ID = 4 
    AC04PW_ID = 2
    AC05PW_ID = 6 #id 6 = empty
    all_token = findtoken.total_token()

       
    # CtrlMode = ipcinfo.read_data() # check control mode
    eftmqtt.connect_storemeter(all_token['storemeter'],MeterPORT,MainPW_ID,1,all_token['PWmode'])  
    eftmqtt.connect_ACMeter(all_token['ACMeter01'], MeterPORT, AC01PW_ID, 1)
    eftmqtt.connect_ACMeter(all_token['ACMeter02'], MeterPORT, AC02PW_ID, 1)
    eftmqtt.connect_ACMeter(all_token['ACMeter03'], MeterPORT, AC03PW_ID, 1)
    eftmqtt.connect_ACMeter(all_token['ACMeter04'], MeterPORT, AC04PW_ID, 2)
    eftmqtt.connect_ACMeter(all_token['ACMeter05'], MeterPORT, AC05PW_ID, 2)
    
    #print("send data to cloud 02")

def read_ACinfor(a, b): # send data to cloud
    ACPORT = '/dev/ttyS4'
    AC01_ID = 1
    AC02_ID = 2
    AC03_ID = 3
    AC04_ID = 4
    AC05_ID = 6 #id 6 = empty
    all_token = findtoken.total_token()

    eftmqtt.connect_ACstatus(all_token['ACinfor01'], ACPORT, AC01_ID)
    eftmqtt.connect_ACstatus(all_token['ACinfor02'], ACPORT, AC02_ID)
    eftmqtt.connect_ACstatus(all_token['ACinfor03'], ACPORT, AC03_ID)
    eftmqtt.connect_ACstatus(all_token['ACinfor04'], ACPORT, AC04_ID)
    eftmqtt.connect_ACstatus(all_token['ACinfor05'], ACPORT, AC05_ID)
    #print("send data to cloud 01")

def demandcal(a, b):
    
    LastPW = ipcInfor.ReadLastPower()
    NowPW = ipcInfor.SaveLastPower()

    
    if NowPW != 'error':
        dfTs = NowPW['LastTs'] - LastPW['LastTs']
        if dfTs <= 1200:
            defPW = NowPW['lastPW'] - LastPW['lastPW']
            PW_demandcal_1h = defPW * 4
        else:
            PW_demandcal_1h = 0
    else:
        PW_demandcal_1h = 0

    PW_dem_diff = NowPW['DemSet'] - PW_demandcal_1h
    
    ipcinfo_token = findtoken.device_token('IPC')
    if dfTs <= 1200:
        eftmqtt.connect_ipcinfor(ipcinfo_token, PW_demandcal_1h, PW_dem_diff, 1)
    else:
        eftmqtt.connect_ipcinfor(ipcinfo_token, PW_demandcal_1h, PW_dem_diff, 0)
    
    demMode = CtrlMode.read_Ctrldemand()
    if demMode == 0 :
        if PW_dem_diff < 0:
            lastdemalr = ipcInfor.Readdemalrchang()
            if lastdemalr == 0:
                ipcalr_token = findtoken.device_token('IPCAlr')
                ipcalert.send_alert(ipcalr_token, 1,1,0)
                ipcInfor.changdemalr(1)
        elif PW_dem_diff >= 0:
            lastdemalr = ipcInfor.Readdemalrchang()
            if lastdemalr == 1:
                ipcalr_token = findtoken.device_token('IPCAlr')
                ipcalert.send_alert(ipcalr_token, 1,2,0)
                ipcInfor.changdemalr(0)
    #print (ipcInfor.Readdemalrchang())
        
def AutoCtrl(a, b):
    if CtrlMode.read_automode == 0:
        status = opentime.CheckDoorClose
        if status == 0:
            if CtrlMode.read_AutoMode == 0:
                ACCtrl.AC_OPset('/dev/ttyS4',1,0) #冷氣
                time.sleep(5)
                ACCtrl.AC_OPset('/dev/ttyS4',2,2) #送風
                time.sleep(5)
                ACCtrl.AC_OPset('/dev/ttyS4',3,2) #送風
                time.sleep(5)
            if CtrlMode.read_AutoMode == 1:
                ACCtrl.AC_OPset('/dev/ttyS4',1,2)
                time.sleep(5)
                ACCtrl.AC_OPset('/dev/ttyS4',2,0)
                time.sleep(5)
                ACCtrl.AC_OPset('/dev/ttyS4',3,2)
                time.sleep(5)
            if CtrlMode.read_AutoMode == 2:
                ACCtrl.AC_OPset('/dev/ttyS4',1,2)
                time.sleep(5)
                ACCtrl.AC_OPset('/dev/ttyS4',2,2)
                time.sleep(5)
                ACCtrl.AC_OPset('/dev/ttyS4',3,0)
                time.sleep(5)
        CtrlMode.count_automode


def ipc_subscribejob(ipc):
    ipcinfo_token = findtoken.device_token('IPC')
    trymqtt.ipc_subscribe(ipcinfo_token)
    
    
@app.route('/home')
@app.route('/')
def home():
    Main_PW = pwmeter.read_3p3w_meter('/dev/ttyS1',1,1)
    #Main_PW = [0,0,0,0,0,0,0,0]
    appInfo = {  # dict
        'LineVolt':'{:.2f}'.format(Main_PW[0]),
        'L1Current':'{:.2f}'.format(Main_PW[1]),
        'L2Current':'{:.2f}'.format(Main_PW[2]),
        'L3Current':'{:.2f}'.format(Main_PW[3]),
        'PF':'{:.2f}'.format(Main_PW[4]),
        'Power':'{:.2f}'.format(Main_PW[5]),
        'Consumption':'{:.2f}'.format(Main_PW[6]),
        'alive':Main_PW[7]
        }
    return render_template('home.html', appInfo=appInfo)

@app.route('/ac01data')
def ac01data():
    ac01_meter = pwmeter.read_1p2w_meter('/dev/ttyS1',2,1)
    ac01_infor = ACCtrl.AC_ReadFullFunction('/dev/ttyS4',1)
    #ac01_meter = [1,1,1,1,1,1]
    #ac01_infor = [1,1,1,1,1,1]
    appInfo = {  # dict
        'AC01voltage':'{:.2f}'.format(ac01_meter[0]),
        'AC01current':'{:.2f}'.format(ac01_meter[1]),
        'AC01pf':'{:.2f}'.format(ac01_meter[2]),
        'AC01power':'{:.2f}'.format(ac01_meter[3]),
        'AC01consumption':'{:.2f}'.format(ac01_meter[4]),
        'AC01alive':'{:.2f}'.format(ac01_meter[5]),
        'AC01status':'{:.2f}'.format(ac01_infor[0]),
        'AC01mode':'{:.2f}'.format(ac01_infor[1]),
        'AC01settemp':'{:.2f}'.format(ac01_infor[2]),
        'AC01windspeed':'{:.2f}'.format(ac01_infor[3]),
        'AC01roomtemp':'{:.2f}'.format(ac01_infor[4]),
        'AC01alive':'{:.2f}'.format(ac01_infor[5]),        
    }
    return render_template('ac01data.html', appInfo=appInfo)
    
@app.route('/ac02data')
def ac02data():
    ac02_meter = pwmeter.read_1p2w_meter('/dev/ttyS1',3,1)
    ac02_infor = ACCtrl.AC_ReadFullFunction('/dev/ttyS4',2)
    appInfo = {  # dict
        'AC02voltage':'{:.2f}'.format(ac02_meter[0]),
        'AC02current':'{:.2f}'.format(ac02_meter[1]),
        'AC02pf':'{:.2f}'.format(ac02_meter[2]),
        'AC02power':'{:.2f}'.format(ac02_meter[3]),
        'AC02consumption':'{:.2f}'.format(ac02_meter[4]),
        'AC02alive':'{:.2f}'.format(ac02_meter[5]),
        'AC02status':'{:.2f}'.format(ac02_infor[0]),
        'AC02mode':'{:.2f}'.format(ac02_infor[1]),
        'AC02settemp':'{:.2f}'.format(ac02_infor[2]),
        'AC02windspeed':'{:.2f}'.format(ac02_infor[3]),
        'AC02roomtemp':'{:.2f}'.format(ac02_infor[4]),
        'AC02alive':'{:.2f}'.format(ac02_infor[5]),        
    }
    return render_template('ac02data.html', appInfo=appInfo)

@app.route('/ac03data')
def ac03data():
    ac03_meter = pwmeter.read_1p2w_meter('/dev/ttyS1',4,1)
    ac03_infor = ACCtrl.AC_ReadFullFunction('/dev/ttyS4',3)
    
    appInfo = {  # dict
        'AC03voltage':'{:.2f}'.format(ac03_meter[0]),
        'AC03current':'{:.2f}'.format(ac03_meter[1]),
        'AC03pf':'{:.2f}'.format(ac03_meter[2]),
        'AC03power':'{:.2f}'.format(ac03_meter[3]),
        'AC03consumption':'{:.2f}'.format(ac03_meter[4]),
        'AC03alive':'{:.2f}'.format(ac03_meter[5]),
        'AC03status':'{:.2f}'.format(ac03_infor[0]),
        'AC03mode':'{:.2f}'.format(ac03_infor[1]),
        'AC03settemp':'{:.2f}'.format(ac03_infor[2]),
        'AC03windspeed':'{:.2f}'.format(ac03_infor[3]),
        'AC03roomtemp':'{:.2f}'.format(ac03_infor[4]),
        'AC03alive':'{:.2f}'.format(ac03_infor[5]),        
    }
    return render_template('ac03data.html', appInfo=appInfo)


@app.route('/ac04data')
def ac04data():
    ac04_meter = pwmeter.read_1p2w_meter('/dev/ttyS1',2,1)
    ac04_infor = ACCtrl.AC_ReadFullFunction('/dev/ttyS4',4)
    appInfo = {  # dict
        'AC04voltage':'{:.2f}'.format(ac04_meter[0]),
        'AC04current':'{:.2f}'.format(ac04_meter[1]),
        'AC04pf':'{:.2f}'.format(ac04_meter[2]),
        'AC04power':'{:.2f}'.format(ac04_meter[3]),
        'AC04consumption':'{:.2f}'.format(ac04_meter[4]),
        'AC04alive':'{:.2f}'.format(ac04_meter[5]),
        'AC04status':'{:.2f}'.format(ac04_infor[0]),
        'AC04mode':'{:.2f}'.format(ac04_infor[1]),
        'AC04settemp':'{:.2f}'.format(ac04_infor[2]),
        'AC04windspeed':'{:.2f}'.format(ac04_infor[3]),
        'AC04roomtemp':'{:.2f}'.format(ac04_infor[4]),
        'AC04alive':'{:.2f}'.format(ac04_infor[5]),         
        }
    return render_template('ac04data.html', appInfo=appInfo)

@app.route('/ac05data')                               
def ac05data():
    ac05_meter = pwmeter.read_1p2w_meter('/dev/ttyS1',2,1)
    ac05_infor = ACCtrl.AC_ReadFullFunction('/dev/ttyS4',1)
    appInfo = {  # dict
        'AC05voltage':'{:.2f}'.format(ac05_meter[0]),
        'AC05current':'{:.2f}'.format(ac05_meter[1]),
        'AC05pf':'{:.2f}'.format(ac05_meter[2]),
        'AC05power':'{:.2f}'.format(ac05_meter[3]),
        'AC05consumption':'{:.2f}'.format(ac05_meter[4]),
        'AC05alive':'{:.2f}'.format(ac05_meter[5]),
        'AC05status':'{:.2f}'.format(ac05_infor[0]),
        'AC05mode':'{:.2f}'.format(ac05_infor[1]),
        'AC05settemp':'{:.2f}'.format(ac05_infor[2]),
        'AC05windspeed':'{:.2f}'.format(ac05_infor[3]),
        'AC05roomtemp':'{:.2f}'.format(ac05_infor[4]),
        'AC05alive':'{:.2f}'.format(ac05_infor[5]),        
    }
    return render_template('ac05data.html', appInfo=appInfo)     
        
if __name__ == '__main__':
    
    
    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    
    first_thread = threading.Thread(target = ipc_subscribejob, args=("ipcjob",))
    first_thread.start()
    

    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url_delay=True)
