# coding:utf-8
import codecs
import json
import time
import findtoken
import pwmeter


def ReadLastPower():
    with open('demandcal.json') as lastPC:
        LastPCommsu = json.load(lastPC)
        lastPC.close
    return LastPCommsu

def SaveLastPower():
    with open('demandcal.json') as lastPC:
        LastPCommsu = json.load(lastPC)
        lastPC.close
    #記錄時間
    ts = time.time()
    LastPCommsu['LastTs'] = ts
    #紀錄電錶
    MainPWType = findtoken.device_token('PWmode') # PWmod 0 = 3p3w, 1 = 1p3w
    if MainPWType == 0:
        MainPW = pwmeter.read_3p3w_meter('/dev/ttyS1', 1, 1)
    elif MainPWType == 1:
        MainPW = pwmeter.read_1p3w_meter('/dev/ttyS1', 1, 1)
    if MainPW[7] == 1:
        LastPCommsu['lastPW'] = MainPW[6]
        with open('demandcal.json', 'w') as LastMainPower:
            json.dump(LastPCommsu, LastMainPower, ensure_ascii=False)
            LastMainPower.close
        return LastPCommsu
    else:
        return 'error'

def Savedemalrchang(demalr):
    with open('demandcal.json') as lastPC:
        LastPCommsu = json.load(lastPC)
        lastPC.close
    LastPCommsu['DemSet'] = demalr
    with open('demandcal.json', 'w') as LastMainPower:
        json.dump(LastPCommsu, LastMainPower, ensure_ascii=False)
        LastMainPower.close
    return LastPCommsu['DemSet']

def Readdemalrchang():
    with open('demandcal.json') as lastPC:
        LastPCommsu = json.load(lastPC)
        lastPC.close
    demalr = LastPCommsu['demandcalalr'] 
    return demalr

def changdemalr(demalr):
    with open('demandcal.json') as lastPC:
        LastPCommsu = json.load(lastPC)
        lastPC.close
    LastPCommsu['demandcalalr'] = demalr
    with open('demandcal.json', 'w') as LastMainPower:
        json.dump(LastPCommsu, LastMainPower, ensure_ascii=False)
        LastMainPower.close
    return LastPCommsu['demandcalalr']
    
    
'''
def save_data(PW_set_value):
    with open('demandcal.json') as EngySaving_Mode:
        PW_ESread = json.load(EngySaving_Mode)
        EngySaving_Mode.close
    PW_ESread['PW_set_dem'] = PW_set_value
    with open('demandcal.json', 'w') as f:
        json.dump(PW_ESread, f, ensure_ascii=False)
        f.close

    
def read_demandcalSet():
    with open('demandcal.json') as EngySaving_Mode:
        PW_ES = json.load(EngySaving_Mode)
        PW_set_dem = PW_ES['PWsetdem']
    
    return(PW_set_dem)


def save_lastinfo(lastts, laststatus):
    with open('demandcal.json') as ipcinfo:
        new_ipcinfo = json.load(ipcinfo)
        ipcinfo.close

    new_ipcinfo['lastts'] = lastts
    new_ipcinfo['lastPW'] = laststatus

    with open('demandcal.json', 'w') as f:
        json.dump(ipcinfo, f, ensure_ascii=False)
        f.close

def read_lastinfo():
    with open('ipcinfo.json') as ipcinfo:
        lastinfo = json.load(ipcinfo)    
    return(lastinfo)
'''
    

if __name__ == '__main__':
    print(ReadLastPower())
    time.sleep(10)
    print (SaveLastPower())
    '''
    PW_power = 100
    save_data(PW_power)
    print(read_demandcalSet())
    while True: 
        ts = time.time()
        print(ts)
        print(ts+1200)
        time.sleep(60)
    '''
