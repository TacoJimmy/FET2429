# coding:utf-8
import codecs

from datetime import datetime
import time
import json
import ipcalert
import findtoken

def read_mode():
    with open('Ctrlmode.json') as ACCtrlMode:
        ACOperate = json.load(ACCtrlMode)
        ACCtrlMode.close
        #print (ACOperate)
    return ACOperate

def read_AutoMode():
    with open('Ctrlmode.json') as ACCtrlMode:
        PWdemand = json.load(ACCtrlMode)
        ACCtrlMode.close
        
    return PWdemand['Automode']

def count_automode():
    with open('Ctrlmode.json') as ACCtrlChange:
        ACOPSET = json.load(ACCtrlChange)
        ACCtrlChange.close
        if ACOPSET['Autocunt'] < 2 :
            ACOPSET['Autocunt'] += 1
        else:
            ACOPSET['Autocunt'] = 0

    with open('Ctrlmode.json', 'w') as ACCtrlChange:
        json.dump(ACOPSET, ACCtrlChange)
        ACCtrlChange.close
    return (ACOPSET['Autocunt'])

def read_Ctrldemand():
    with open('Ctrlmode.json') as ACCtrlMode:
        PWdemand = json.load(ACCtrlMode)
        ACCtrlMode.close
        
    return PWdemand['Ctrldemand']
    
def change_mode(ipcctrlmode, ipcctrlenable):
    with open('Ctrlmode.json') as ACCtrlChange:
        ACModeRead = json.load(ACCtrlChange)
    
    
    CtrlDoorClose = ACModeRead['CtrlDoorClose']
    CtrlACFunclimit = ACModeRead['CtrlACFunclimit']
    CtrlACTemplimit = ACModeRead['CtrlACTemplimit']
    CtrlPrepare = ACModeRead['CtrlPrepare']
    Ctrldemand = ACModeRead['Ctrldemand']
    CtrlLimittemp = ACModeRead['ipctemplimit']

    if ipcctrlmode == 1:
        if ipcctrlenable in [0,1]: 
            CtrlDoorClose = ipcctrlenable
    
    elif ipcctrlmode == 2:
        if ipcctrlenable in [0,1]:
            CtrlACFunclimit = ipcctrlenable
    
    elif ipcctrlmode == 3:
        if ipcctrlenable in [0,1]:
            CtrlACTemplimit = ipcctrlenable
    
    elif ipcctrlmode == 4:
        if ipcctrlenable in [0,1]:
            CtrlPrepare = ipcctrlenable
    elif ipcctrlmode == 5:
        if ipcctrlenable in [0,1]:
            Ctrldemand = ipcctrlenable
    elif ipcctrlmode == 6:
        if ipcctrlenable >= 18 and ipcctrlenable <= 30:
            CtrlLimittemp = ipcctrlenable
        else:
            CtrlLimittemp = 26

    # chang conftrl mode
    if CtrlDoorClose != ACModeRead['CtrlDoorClose']:
        ACModeRead['CtrlDoorClose'] = CtrlDoorClose
        ipcalr_token = findtoken.device_token('IPCAlr')
        if CtrlDoorClose == 0:
            ipcalert.send_alert(ipcalr_token , 2, 1,0)
            
        elif CtrlDoorClose == 1:
            ipcalert.send_alert(ipcalr_token , 2, 2,0)
            

    elif CtrlACFunclimit != ACModeRead['CtrlACFunclimit']:
        ACModeRead['CtrlACFunclimit'] = CtrlACFunclimit
        ipcalr_token = findtoken.device_token('IPCAlr')
        if CtrlACFunclimit == 0:
            ipcalert.send_alert(ipcalr_token , 2, 3,0)
            
        
        elif CtrlACFunclimit == 1:
            ipcalert.send_alert(ipcalr_token , 2, 4,0)
            
        
    elif CtrlACTemplimit != ACModeRead['CtrlACTemplimit']:
        ACModeRead['CtrlACTemplimit'] = CtrlACTemplimit
        ipcalr_token = findtoken.device_token('IPCAlr')
        if CtrlACTemplimit == 0:
            ipcalert.send_alert(ipcalr_token , 2, 5,0)
            
        elif CtrlACTemplimit == 1:
            ipcalert.send_alert(ipcalr_token , 2, 6,0)
            
        
    elif CtrlPrepare != ACModeRead['CtrlPrepare']:
        ACModeRead['CtrlPrepare'] = CtrlPrepare
        ipcalr_token = findtoken.device_token('IPCAlr')
        if CtrlPrepare == 0:
            ipcalert.send_alert(ipcalr_token , 2, 8,0)
            
        elif CtrlPrepare == 1:
            ipcalert.send_alert(ipcalr_token , 2, 7,0)
            

    elif Ctrldemand != ACModeRead['Ctrldemand']:
        ACModeRead['Ctrldemand'] = Ctrldemand
        ipcalr_token = findtoken.device_token('IPCAlr')
        if Ctrldemand == 0:
            ipcalert.send_alert(ipcalr_token , 1, 3,0)
        elif Ctrldemand == 1:
            ipcalert.send_alert(ipcalr_token , 1, 4,0)
    
    

    elif CtrlLimittemp != ACModeRead['ipctemplimit']:
        ACModeRead['ipctemplimit'] = CtrlLimittemp
        ipcalr_token = findtoken.device_token('IPCAlr')
        # add Publish
    
    # load file
    with open('Ctrlmode.json', 'w') as CtrlFuntion:
        json.dump(ACModeRead, CtrlFuntion)
    
    return ACModeRead

if __name__ == '__main__':
    print(change_mode(4,1))