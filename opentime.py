from datetime import datetime
import datetime
import time
import json


def read_data():
    with open('openinghours.json') as OpenTime:
        StoreOperate = json.load(OpenTime)
        OpenTime.close
        
    return StoreOperate
    
def CheckDoorClose():
    
    DoorClose_Flag = 0
    OpenHours = read_data()
    DoorClose = OpenHours['endtime']
    DoorClose_hm = DoorClose.split(":")
    DoorClose_hours = int(DoorClose_hm[0])
    DoorClose_mins = int(DoorClose_hm[1])
    
    DoorOpen = OpenHours['starttime']
    DoorOpen_hm = DoorOpen.split(":")
    DoorOpen_hours = int(DoorOpen_hm[0])
    DoorOpen_mins = int(DoorOpen_hm[1])
    
    TimeNow = time.strftime("%H:%M", time.localtime())
    TimeNow_hm = TimeNow.split(":")
    TimeNow_hours = int(TimeNow_hm[0])
    TimeNow_mins = int(TimeNow_hm[1])
    

    Now_door = datetime.datetime(2020,12,17,TimeNow_hours,TimeNow_mins,0)
    Close_Door = datetime.datetime(2020,12,17,DoorClose_hours,DoorClose_mins,0)
    Open_Door = datetime.datetime(2020,12,17,DoorOpen_hours,DoorOpen_mins,0)
    
    if (Close_Door < Now_door or Now_door < Open_Door):
        DoorClose_Flag = 1
    else:
        DoorClose_Flag = 0
    return DoorClose_Flag

'''
def CheckDoorClose():
    DoorClose_Flag = 0
    OpenHours = read_data()
    DoorClose = OpenHours['endtime']
    #DoorClose_time = time.strptime(DoorClose, "%H:%M")
    DoorOpen = OpenHours['starttime']
    #print ('DoorOpen :',DoorOpen)
    #DoorOpen_time = time.strptime(DoorOpen, "%H:%M")
    TimeNow = time.strftime("%H:%M", time.localtime())
    if (DoorClose < TimeNow or DoorOpen > TimeNow):
        DoorClose_Flag = 1
    else:
        DoorClose_Flag = 0
    return DoorClose_Flag
'''

def prepeartime():
    OPtime = read_data()
    starttime = OPtime['starttime']
    DoorOpen_hm = starttime.split(":")
    DoorOpen_hours = int(DoorOpen_hm[0])
    DoorOpen_mins = int(DoorOpen_hm[1])


    prestarttime = OPtime['prestarttime']
    prestart_hm = prestarttime.split(":")
    prestart_hours = int(prestart_hm[0])
    prestart_mins = int(prestart_hm[1])

    Open_prepear = datetime.timedelta(hours=-prestart_hours,minutes=-prestart_mins)
    Open_Door = datetime.datetime(2020,12,17,DoorOpen_hours,DoorOpen_mins,0)
    Open_DoorPrePear = Open_Door + Open_prepear

    TimeNow = time.strftime("%H:%M", time.localtime())
    TimeNow_hm = TimeNow.split(":")
    TimeNow_hours = int(TimeNow_hm[0])
    TimeNow_mins = int(TimeNow_hm[1])
    Now_door = datetime.datetime(2020,12,17,TimeNow_hours,TimeNow_mins,0)

    # print(Open_Door)
    # print(Open_DoorPrePear)
    # print(Now_door)
    if  Open_DoorPrePear < Now_door < Open_Door:
        return (1)
    else:
        return (0)

def change_OPtime(settime, timereset):
    OPtime = read_data()
    
    starttime = OPtime['starttime']
    prestarttime = OPtime['prestarttime']
    endtime = OPtime['endtime']
    delayendtime = OPtime['delayendtime']
    
    if settime == 'starttime':
        starttime = timereset
    elif settime == 'prestarttime':
        prestarttime = timereset
    elif settime == 'endtime':
        endtime = timereset
    elif settime == 'delayendtime':
        delayendtime = timereset

    if OPtime['starttime'] != starttime:
        OPtime['starttime'] = starttime
        # send change
    elif OPtime['prestarttime'] != prestarttime:
        OPtime['prestarttime'] = prestarttime
        # send change
    elif OPtime['endtime'] != endtime:
        #print(OPtime['endtime'])
        #print(OPtime['starttime'])
        #print(OPtime['endtime'] > OPtime['starttime'])
        if endtime > OPtime['starttime']:
            
            OPtime['endtime'] = endtime    
        # send change
    elif OPtime['delayendtime'] != delayendtime:
        OPtime['delayendtime'] = delayendtime   
        # send change
    with open('openinghours.json', 'w') as OpenTime:
        json.dump(OPtime, OpenTime)
    
    return OPtime 


if __name__ == '__main__':
    prepeartime()
    #print(CheckDoorClose())
    
    
    
    
    