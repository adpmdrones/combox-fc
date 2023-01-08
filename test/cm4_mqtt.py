#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
##########
# by ADPM Drones Srl 2021-2023
##########
#

import paho.mqtt.client as mqtt
import requests
import json
import os

THINGSBOARD_HOST = 'dashboard.adpmdrones.com'
API = "http://localhost:8088"
ACCESS_TOKEN = 'EeLqJHNQgWR4FtycieRD'

servo_state = {5: '1000', 6: '1000', 7: '1000', 8: '1000', 9: '1000', 10: '1000', 11: '1000', 12: '1000', 13: '1000',
              14: '1000', 15: '1000', 16: '1000'}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    # Sending current status
    client.publish('v1/devices/me/attributes', getValue(), 1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    if data['method'] == 'getValue':
        # Reply with status
        client.publish(msg.topic.replace('request', 'response'), getValue(), 1)
    elif data['method'] == 'setValue':
        # Update status and reply
        print(data)
        print(data['params'])
        print('response')
        setValue(1000, data['params'])
        client.publish(msg.topic.replace('request', 'response'), getValue(), 1)
        client.publish('v1/devices/me/attributes', getValue(), 1)

def getValue():
    print("Get Value")
    print(json.dumps(servo_state))
    return json.dumps(servo_state)

def setValue(pin, status):
    print("Set Value")
    print(pin)
    print(status)
    servo_state[pin] = status


client = mqtt.Client()
# Register connect callback
client.on_connect = on_connect
# Registed publish message callback
client.on_message = on_message
# Set access token
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    os._exit(0)



