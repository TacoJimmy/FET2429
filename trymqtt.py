
# coding:utf-8
import codecs
import json
import ssl
import paho.mqtt.client as mqtt
import time
import CtrlMode
import opentime
import ACCtrl
import findtoken
import ipcInfor

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe('v1/devices/me/rpc/request/+',1)
    time.sleep(3)

def ipcaccontrl(data_payload):
    for i in data_payload['params']['deviceId']:
        AC_token = findtoken.total_token()
        if i == AC_token['ACinfor01']:
            AC_ID = 1
        elif i == AC_token['ACinfor02']:
            AC_ID = 2
        elif i == AC_token['ACinfor03']:
            AC_ID = 3
        elif i == AC_token['ACinfor04']:
            AC_ID = 4
        elif i == AC_token['ACinfor05']:
            AC_ID = 5
        CtrlCondition = CtrlMode.read_mode()
        #print(CtrlCondition)
        if 'airconditiongstatus' in data_payload['params']:
            DoorClose_check = opentime.CheckDoorClose()
            AC_CtrlMode = data_payload['params']['airconditiongstatus']
            if CtrlCondition['CtrlDoorClose'] == 0 : #非營業模式啟用
                if DoorClose_check == 1 and AC_CtrlMode == 1: #非營業時間且開啟冷氣
                    fb_payload = {'airconditiongstatus':'Store not opening'}    
                else:
                    AC_status = ACCtrl.AC_PowerONOFF('/dev/ttyS4', AC_ID, AC_CtrlMode)
                    fb_payload = {'airconditiongstatus': AC_status}
            else:                                    #非營業模式不啟用
                AC_status = ACCtrl.AC_PowerONOFF('/dev/ttyS4', AC_ID, AC_CtrlMode)
                fb_payload = {'airconditiongstatus': AC_status}
                
        if 'operationmode' in data_payload['params']:
            AC_OPMode = data_payload['params']['operationmode']
            if AC_OPMode in range(0,3):
                AC_OPStatus = ACCtrl.AC_OPset('/dev/ttyS4', AC_ID, AC_OPMode )
                fb_payload = {'operationmode': AC_OPStatus}
            else:
                fb_payload = {'operationmode': 'Please Check Control mode'}
            
        if 'temperature' in data_payload['params']:
            AC_CtrlTemp = data_payload['params']['temperature']
            if CtrlCondition['CtrlACTemplimit'] == 0:
                if AC_CtrlTemp >= CtrlCondition['ipctemplimit']:
                    AC_TempSet = ACCtrl.AC_SetTemp('/dev/ttyS4',AC_ID,AC_CtrlTemp)
                    fb_payload = {'temperature': AC_TempSet}
                else:
                    fb_payload = {'temperature': 'Check temperature setting'}
            else:
                AC_TempSet = ACCtrl.AC_SetTemp('/dev/ttyS4',AC_ID,AC_CtrlTemp)
                fb_payload = {data_payload['params']['commandname']: AC_TempSet}
                    
        if 'windspeed' in data_payload['params']:
            AC_CtrlSpeed = data_payload['params']['windspeed']
            if AC_CtrlSpeed in range(0,4): 
                AC_FanStatus = ACCtrl.AC_FanSpeed('/dev/ttyS4',AC_ID,AC_CtrlSpeed)
                fb_payload = {'windspeed': AC_FanStatus}
            else:
                fb_payload = {'windspeed': 'Check windspeed setting'}
    return fb_payload

def ipcenergymag(data_payload):
    # 確認限制模式開啟或關閉
    if 'ipcctrlmode' in data_payload['params']:
        AC_LimitMode = data_payload['params']['ipcctrlmode']
        if 5 >= AC_LimitMode >=1:
            #print(AC_LimitMode)
            #print(type(AC_LimitMode))
            AC_LimitEnable = data_payload['params']['ipcctrlenable']
            CtrlLimit_Status = CtrlMode.change_mode(AC_LimitMode, AC_LimitEnable)
            if data_payload['params']['ipcctrlmode'] == 1:
                fb_payload = {"1":CtrlLimit_Status['CtrlDoorClose']}
            elif data_payload['params']['ipcctrlmode'] == 2:
                fb_payload = {"2":CtrlLimit_Status['CtrlACFunclimit']}
            elif data_payload['params']['ipcctrlmode'] == 3:
                fb_payload = {"3":CtrlLimit_Status['CtrlACTemplimit']}
            elif data_payload['params']['ipcctrlmode'] == 4:
                fb_payload = {"4":CtrlLimit_Status['CtrlPrepare']}
        else:
            fb_payload = {'ipcenergymanage':'please check control mode'}
    # 確認IPC限制溫度
    if 'ipctemplimit' in data_payload['params']:
        AC_LimitTemp = data_payload['params']['ipctemplimit']
        CtrlLimit_Status = CtrlMode.change_mode(6, AC_LimitTemp)
        fb_payload = {'ipctemplimit':CtrlLimit_Status['ipctemplimit']}
    # 確認營業時間    
    if 'starttime' in data_payload['params']:
        try:
            resettime = data_payload['params']['starttime']
            #print(resettime)
            time.strptime(resettime, "%H:%M") 
            CtrlLimit_Status = opentime.change_OPtime('starttime', resettime)
            fb_payload = {'starttime':CtrlLimit_Status['starttime']}
        except:
            fb_payload = {'starttime':'check setting'}   
    # 確認預備時間
    if 'prestarttime' in data_payload['params']:
        try:
            resettime = data_payload['params']['prestarttime']
            time.strptime(resettime, "%H:%M") 
            CtrlLimit_Status = opentime.change_OPtime('prestarttime', resettime)
            fb_payload = {'prestarttime':CtrlLimit_Status['prestarttime']}
        except:
            fb_payload = {'prestarttime':'check setting'} 
    # 確認閉店時間
    if 'endtime' in data_payload['params']:
        try:
            resettime = data_payload['params']['endtime']
            time.strptime(resettime, "%H:%M") 
            CtrlLimit_Status = opentime.change_OPtime('endtime', resettime)
            fb_payload = {'endtime':CtrlLimit_Status['endtime']}
        except:
            fb_payload = {'endtime':'check setting'} 
    # 確認開店預備時間
    if 'delayendtime' in data_payload['params']:
        try:
            resettime = data_payload['params']['delayendtime']
            time.strptime(resettime, "%H:%M") 
            CtrlLimit_Status = opentime.change_OPtime('delayendtime', resettime)
            fb_payload = {'delayendtime':CtrlLimit_Status['delayendtime']}
        except:
            fb_payload = {'delayendtime':'check setting'} 
    
    return fb_payload
    
def ipcdemamag(data_payload):
    # 設定需量警告開啟或關閉
    if 'ipcctrlenable' in data_payload['params']:
        AC_LimitEnable = data_payload['params']['ipcctrlenable']
        CtrlLimit_Status = CtrlMode.change_mode(5, AC_LimitEnable)
        if (data_payload['params']['ipcctrlenable'] == 0) or (data_payload['params']['ipcctrlenable'] == 1):
            fb_payload = {"ipcenergymanage":CtrlLimit_Status['Ctrldemand']}
        else:
            fb_payload = {'ipcenergymanage':'please check control mode'}

    # 重新設定須量值
    if 'ipdemendset' in data_payload['params']:
            ipc_demndset = data_payload['params']['ipdemendset']
            setdemalr = ipcInfor.Savedemalrchang(ipc_demndset)
            fb_payload = {'ipdemendset':setdemalr}
    
    return fb_payload

def on_message(client, userdata, msg):
    data_topic = msg.topic
    data_payload = json.loads(msg.payload.decode())
    time.sleep(.5)
    listtopic = data_topic.split("/")  
    signal_fb = 'v1/devices/me/rpc/response/'+str(listtopic[5]) # response topic
    
    if data_payload['method'] == 'ipccontrolac':
        fb_payload = ipcaccontrl(data_payload)
    elif data_payload['method'] == 'ipcenergymanage':
        fb_payload = ipcenergymag(data_payload)                
    elif data_payload['method'] == 'ipcdemamanage':
        fb_payload = ipcdemamag(data_payload)
    
    client.publish(signal_fb,json.dumps(fb_payload)) # send response

'''    
def on_publish(client, userdata, rc, data):
    if rc == 0:
        client.publish('v1/devices/me/rpc/response/'+'00000000-0000-0000-0000-000000000000',json.dumps(data))
        time.sleep(3)
    else:
        client.disconnect()
'''

def ipc_subscribe(token):
    meter_token = token
    meter_pass = ''
    url = 'portal.cat2.fetnet.net'

    client = mqtt.Client('', True, None, mqtt.MQTTv31)
    client.on_connect = on_connect
    time.sleep(.5)
    client.on_message = on_message
    time.sleep(.5)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    client.tls_set_context(context)
    client.username_pw_set(meter_token, meter_pass)
    client.connect(url, 1883, 60)


    client.loop_forever()
