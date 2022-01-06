
# coding:utf-8
import codecs
import json
import ssl
import paho.mqtt.client as mqtt
import time
import findtoken

def send_alert(token , alerttype, alertcause,id):
    FETnet_token = token 
    FETnet_passwd = ''
    if alerttype == 1:
        if alertcause ==1:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"超約事件開始/即時需量大於契約容量"
                }
        elif alertcause ==2:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"超約事件結束/即時需量小於契約容量"
                }
        elif alertcause ==3:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"啟用需量監視需量"
                }
        elif alertcause ==4:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"解除需量監視需量"
                }

    if alerttype == 2:
        if alertcause ==1:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"啟用非營業模式功能"
                }
        elif alertcause ==2:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"解除非營業模式功能"
                }
        elif alertcause ==3:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"啟用空調功能限制功能"
                }
        elif alertcause ==4:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"解除空調功能限制功能"
                }
        elif alertcause ==5:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"啟用營業模式功能"
                }
        elif alertcause ==6:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"解除營業模式功能"
                }
        elif alertcause ==7:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"解除預備營業模式功能"
                }
        elif alertcause ==8:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"啟用預備營業模式功能"
                }
    if alerttype == 3:
        if alertcause ==1:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"遙控器開啟冷氣 - 非營業時間"
                }
        elif alertcause ==2:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"冷氣故障警報:"+str(id)
                }
        elif alertcause ==3:
            ipcaler_payload = {
                "emshmialerttype":alerttype,
                "emshmialertcause":alertcause,
                "emshmialertcontent":"冷氣故障恢復"+str(id)
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
    client.on_connect = client.publish('v1/devices/me/telemetry',json.dumps(ipcaler_payload))
    time.sleep(3)
    client.loop_stop()
    client.disconnect()  

def AC_connectalerty(token , ACtoken):
    FETnet_token = token 
    FETnet_passwd = ''
    
    ipcInfor_payload = {
        "emshmialertlink": "設備連線異常:"+ ACtoken +"連線異常",
        "emsvendorinfo":"歐陸通風-ADTEK-AEMDR TEL:0935-534163"
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

def ME_connectalerty(Arltoken , MEtoken):
    
    ipcInfor_payload = {
        "emshmialertlink": "設備連線異常:"+MEtoken+"連線異常",
        "emsvendorinfo":"歐陸通風-ADTEK-AEMDR TEL:0935-534163"
        } 
    
    client = mqtt.Client('', True, None, mqtt.MQTTv31)
    client.username_pw_set(Arltoken, '')
    
    
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



