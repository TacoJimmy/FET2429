# coding:utf-8
import codecs
import json
import ssl
import paho.mqtt.client as mqtt
import pwmeter
import time
import ACCtrl
import CtrlMode
import opentime
import ipcalert
import findtoken


def read_ACON():
    with open('acon.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONDoorClose.close
    return (ACONCount['ACONTime'])

def count_ACON():
    with open('acon.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONDoorClose.close
        ACONCount['ACONTime'] += 1
        
    with open('acon.json', 'w') as ACONDoorClose:
        json.dump(ACONCount, ACONDoorClose)
        ACONDoorClose.close
    return (ACONCount['ACONTime'])

def Zero_ACON():
    with open('acon.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONDoorClose.close
        ACONCount['ACONTime'] = 0
        ACONCount['ACONDelay'] = 0
    with open('acon.json', 'w') as ACONDoorClose:
        json.dump(ACONCount, ACONDoorClose)
        ACONDoorClose.close
    return (ACONCount['ACONTime'])

def Plus_ACON():
    with open('acon.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONDoorClose.close
        ACONCount['ACONTime'] = 1
    with open('acon.json', 'w') as ACONDoorClose:
        json.dump(ACONCount, ACONDoorClose)
        ACONDoorClose.close
    return (ACONCount['ACONTime'])

def read_ACError():
    with open('acon.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONDoorClose.close
    return (ACONCount['ACerror'])

def Plus_ACError():
    with open('acon.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONDoorClose.close
        ACONCount['ACerror'] = 1
    with open('acon.json', 'w') as ACONDoorClose:
        json.dump(ACONCount, ACONDoorClose)
        ACONDoorClose.close
    return (ACONCount['ACerror'])

def Zero_ACError():
    with open('acon.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONDoorClose.close
        ACONCount['ACerror'] = 0
    with open('acon.json', 'w') as ACONDoorClose:
        json.dump(ACONCount, ACONDoorClose)
        ACONDoorClose.close
    return (ACONCount['ACerror'])

def Plus_Time():
    with open('acon.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONDoorClose.close
        TimeNow = time.strftime("%H:%M", time.localtime())
        timeString = "2020-12-17 "+ TimeNow +":00" 
        struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") 
        time_stamp = int(time.mktime(struct_time)) 
        
        OPtime = opentime.read_data()
        DoorClose_hm = OPtime['delayendtime']
        DoorClose_hm = DoorClose_hm .split(":")
        DoorClose_hours = int(DoorClose_hm[0])
        DoorClose_mins = int(DoorClose_hm[1])

        DoorDelay = DoorClose_hours*3600 + DoorClose_mins*60 + time_stamp
        
        ACONCount['ACONDelay'] = DoorDelay
    with open('acon.json', 'w') as ACONDoorClose:
        json.dump(ACONCount, ACONDoorClose)
        ACONDoorClose.close
    return (ACONCount['ACONDelay'])

def CheckACONDelay():
    with open('acon.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONTime = ACONCount['ACONDelay']
        ACONDoorClose.close
    TimeNow = time.strftime("%H:%M", time.localtime())
    timeString = "2020-12-17 "+ TimeNow +":00"     
    struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") 
    timeforchek = int(time.mktime(struct_time))



    if timeforchek >= ACONTime:
        return 1
    else:
        return 0

def connect_ipcinfor(token , PW_dem_1h, diffvalue, ipcinf):
    FETnet_token = token 
    FETnet_passwd = ''
    
    ipcInfor_payload = {
        "ipcdemandcal": PW_dem_1h,
        "ipcdemanddiff":diffvalue,
        "ipcinfo":"歐陸通風-ADTEK-AEMDR TEL:0935-534163",
        "ipcdevicealive": ipcinf
        } 
    
    client = mqtt.Client('', True, None, mqtt.MQTTv31)
    client.username_pw_set(FETnet_token, FETnet_passwd)
    
    
    # the key steps here
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # if you do not want to check the cert hostname, skip it
    # context.check_hostname = False
    client.tls_set_context(context)
    client.connect("portal.cat2.fetnet.net", 1883, 60)
    client.loop_start()
    time.sleep(1)
    client.on_connect = client.publish('v1/devices/me/telemetry',json.dumps(ipcInfor_payload))
    time.sleep(3)
    client.loop_stop()
    client.disconnect()

def connect_storemeter(token, COMport, id, loop, PWmode):
    FETnet_token = token 
    FETnet_passwd = ''
    if PWmode == 0:
        MainPW = pwmeter.read_3p3w_meter(COMport, id, loop) # main power
        metertype = "三相三線"
    elif PWmode == 1:
        MainPW = pwmeter.read_1p3w_meter(COMport, id, loop) # main power
        metertype = "單相三線"
    # MainPW = (0,0,0,0,0,0,0,0)
    MainPW_payload = {
        "emsstorelvoltage": MainPW[0],"emsstorercurrentA":MainPW[1],"emsstorercurrentB":MainPW[2],"emsstorercurrentC":MainPW[3],
        "emsstorepower": MainPW[4],"emsstoreopf": MainPW[5], "emsstorecumulativeelectricityconsumption": MainPW[6],
        "emsstoretype": metertype,"emsvendorinfo":"歐陸通風-ADTEK-AEMDR TEL:0935-534163",
        "emsdevicealive":MainPW[7]
        } 
    
    client = mqtt.Client('', True, None, mqtt.MQTTv31)
    client.username_pw_set(FETnet_token, FETnet_passwd)
    # the key steps here
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # if you do not want to check the cert hostname, skip it
    # context.check_hostname = False
    client.tls_set_context(context)
    client.connect("portal.cat2.fetnet.net", 1883, 60)
    client.loop_start()
    time.sleep(.5)
    client.on_connect = client.publish('v1/devices/me/telemetry',json.dumps(MainPW_payload))
    time.sleep(1)
    client.loop_stop()
    client.disconnect()
    

def connect_ACMeter(meter_token, port, kid, loop):
    FETnet_passwd = ''
    if (kid != 6):
        ACPW = pwmeter.read_1p2w_meter(port,kid,loop) # main power
    else:
        ACPW = (0,0,0,0,0,3)
    
    # 警報連線異常
    if ACPW[5] == 2:
        ipcalr_token = findtoken.device_token('IPCAlr')
        ipcalert.ME_connectalerty(ipcalr_token , meter_token)

    ACPW_payload = {
        "emsstoreacmvoltage":ACPW[0],
        "emsstoreacmcurrent":ACPW[1],
        "emsstoreacmpower":ACPW[2],
        "emsstoreacmpf":ACPW[3],
        "emsstoreacmconsumption": ACPW[4],
        "emsvendorinfo":"歐陸通風-ADTEK-AEMDR TEL:0935-534163",
        "emsdevicealive":ACPW[5]
        }
    
    client = mqtt.Client('', True, None, mqtt.MQTTv31)
    client.username_pw_set(meter_token, FETnet_passwd)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    client.tls_set_context(context)
    client.connect("portal.cat2.fetnet.net", 1883, 60)
    client.loop_start()
    time.sleep(1)
    client.on_connect = client.publish('v1/devices/me/telemetry',json.dumps(ACPW_payload))
    time.sleep(3)
    client.loop_stop()
    client.disconnect()



def CheckACOPLimit(port, id, ACstatus):
    AClimit = CtrlMode.read_mode() #read limit
    if AClimit['CtrlACFunclimit'] == 1:
        if ACstatus[0] == 1: #設備運轉中
            if ACstatus[1] == 3:
                ACstatus[1] = 2 #自動變冷氣
                ACChange = ACCtrl.AC_OPset(port,id,ACstatus[1]) 
            if ACstatus[1] == 4:
                ACstatus[1] = 2 #暖氣變送風
                ACChange = ACCtrl.AC_OPset(port,id,ACstatus[1])

def CheckACTempLimit(port, id, ACstatus):
    AClimit = CtrlMode.read_mode() #read limit
    if AClimit['CtrlACTemplimit'] == 1:
        if (ACstatus[3] < AClimit['ipctemplimit'] and ACstatus[0] == 1): #冷氣運轉下且低於設定溫度
            ACstatus[3] = AClimit['ipctemplimit']
            ACTempChange = ACCtrl.AC_SetTemp(port,id,AClimit['ipctemplimit'])               


def CheckOpenDuty(port, id, ACstatus):
    AClimit = CtrlMode.read_mode() #read limit
    if AClimit['CtrlDoorClose'] == 1:
        DoorClose = opentime.CheckDoorClose()
        if (DoorClose == 1 and ACstatus[0] == 1):
            ACstatus[0] = 0
            ACCtrl.AC_PowerONOFF(port,id,ACstatus[0])

'''       
def count_ACON():
    with open('ACON.json') as ACONDoorClose:
        ACONCount = json.load(ACONDoorClose)
        ACONDoorClose.close
        #print (ACOperate)
    return ACONCount
'''

def connect_ACstatus(AC_token, COMport, ACID):
    FETnet_passwd = ''
    if (ACID != 6):
        AC_Status = ACCtrl.AC_ReadFullFunction(COMport, ACID) # main power
        if AC_Status[5] == 0:
            ErrorStatus = read_ACError()
            if ErrorStatus == 0:
                ipcalr_token = findtoken.device_token('IPCAlr')
                ipcalert.send_alert(ipcalr_token, 3,1,0)
                Plus_ACError()
        elif AC_Status[5] == 1:
            Zero_ACError()
    else:
        AC_Status = (0,0,0,0,0,3)
    CheckACLimit = CtrlMode.read_mode()
    temp_funcenable = CheckACLimit["CtrlACTemplimit"]
    temp_setlimit = CheckACLimit['ipctemplimit']
    
    if temp_funcenable == 0:
        if AC_Status[3] < temp_setlimit:
            if opentime.prepeartime() == 1 and CheckACLimit["CtrlPrepare"] == 0: #不考慮節能
                a = 0
            else:
                ACCtrl.AC_SetTemp(COMport,ACID,temp_setlimit)

    if CheckACLimit["CtrlDoorClose"] == 0 :
        DoorClose = opentime.CheckDoorClose()
        #非營業時間操作
        if DoorClose == 1 and AC_Status[0] == 1:
            ACONCount = read_ACON()
            if ACONCount == 1:
                ACTrunOFF = CheckACONDelay()
                if ACTrunOFF == 1:
                    if opentime.prepeartime() == 1 and CheckACLimit["CtrlPrepare"] == 0: #不考慮節能
                        Zero_ACON()
                    else:
                        ACCtrl.AC_PowerONOFF(COMport,1,0) #trun off AC
                        time.sleep(3)
                        ACCtrl.AC_PowerONOFF(COMport,2,0) #trun off AC
                        time.sleep(3)
                        ACCtrl.AC_PowerONOFF(COMport,3,0) #trun off AC
                        time.sleep(3)
                        ACCtrl.AC_PowerONOFF(COMport,4,0) #trun off AC
                        time.sleep(3)
                        ACCtrl.AC_PowerONOFF(COMport,5,0) #trun off AC
                        time.sleep(3)
                        ipcalr_token = findtoken.device_token('IPCAlr')
                        ipcalert.send_alert(ipcalr_token, 3,1,0)
                        Zero_ACON()
            
            else:
                Plus_ACON()
                Plus_Time()
        elif DoorClose == 0 and AC_Status[0] == 1:
            Zero_ACON()
            
    if CheckACLimit["CtrlACFunclimit"] == 0 :
        if AC_Status[1] == 3:
            ACCtrl.AC_OPset(COMport,ACID,0) #trun AC to AC mode
        elif AC_Status[1] == 4:
            ACCtrl.AC_OPset(COMport,ACID,2) #trun AC to fan only mode

    AC_Status = ACCtrl.AC_ReadFullFunction(COMport, ACID)    
    
    # 警報連線異常
    if AC_Status[5] == 2:
        ipcalr_token = findtoken.device_token('IPCAlr')
        ipcalert.AC_connectalerty(ipcalr_token , AC_token)
    AC_payload = {
        "emsstoreairconditioningstatus": AC_Status[0],
        "emsstoreoperationmode":AC_Status[1],
        "emsstorewindspeed":AC_Status[2],
        "emsstoresettemperature":AC_Status[3],
        "emsstoreroomtemperature": AC_Status[4],
        "emsvendorinfo":"歐陸通風-ADTEK-AEMDR TEL:0935-534163",
        "emsdevicealive":AC_Status[5]
        }

    client = mqtt.Client('', True, None, mqtt.MQTTv31)
    client.username_pw_set(AC_token, FETnet_passwd)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    client.tls_set_context(context)
    client.connect("portal.cat2.fetnet.net", 1883, 60)
    client.loop_start()
    time.sleep(1)
    client.on_connect = client.publish('v1/devices/me/telemetry',json.dumps(AC_payload))
    time.sleep(3)
    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    while True:
        connect_ipcinfor()
        time.sleep(5)
