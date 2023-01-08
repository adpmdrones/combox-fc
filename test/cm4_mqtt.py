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
import random

THINGSBOARD_HOST = 'dashboard.adpmdrones.com'
API = "http://localhost:8088"
ACCESS_TOKEN = 'EeLqJHNQgWR4FtycieRD'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    # Sending current stastus from mavlink
    client.publish('v1/devices/me/attributes', getValue() , 1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("*" * 20)
    print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    if data['method'] == 'getValue':
        # Reply with status fro mavlink
        getValue()

    elif data['method'] == 'setValue':
        # Update status and reply
        print(data)
        print(data['params'])
        print('response')
        setValue(random.randrange(0,100, step=10))

def getValue():
    print("Get Value")
    status = random.randrange(0,100, step=5)
    return status


def setValue(status):
    print("Set Value")

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



