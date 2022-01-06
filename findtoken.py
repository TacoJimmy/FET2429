
# coding:utf-8
import codecs
import json
import ssl
import paho.mqtt.client as mqtt
import time

def device_token(device):
    with open('storetoke.json') as systoken:
        devtoken = json.load(systoken)
        systoken.close
    return (devtoken[device])

def total_token():
    with open('storetoke.json') as systoken:
        devtoken = json.load(systoken)
        systoken.close
    return (devtoken)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe('v1/devices/me/rpc/request/+',1)
    time.sleep(3)

def on_message(client, userdata, msg):
    
    data_payload = json.loads(msg.payload.decode())
    #j = json.loads(data)
    print(data_payload)
    
'''
ipc_token = device_token('IPC')

meter_token = ipc_token
meter_pass = ''
url = 'portal.cat2.fetnet.net'

client = mqtt.Client('', True, None, mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
client.tls_set_context(context)
client.username_pw_set(meter_token, meter_pass)
client.connect(url, 1883, 60)


client.loop_forever()
'''
