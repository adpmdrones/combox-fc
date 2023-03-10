#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
##########
# by ADPM Drones Srl 2021-2023
##########
#

'''
https://antima.it/tutorial-utilizzare-mqtt-con-python-parte-2-callback-e-loop/?unapproved=249&moderation-hash=9a5e6c6a86663fafe619e4889fa25bf1#comment-249
'''

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

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("*" * 20)
    print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    if data['method'] == 'getValue':
        # Reply with status fro mavlink
        client.publish(msg.topic.replace('request', 'response'), get_Value(), 1)
    elif data['method'] == 'setValue':
        # Update status and reply
        print(data)
        print(data['params'])
        print('response')
        set_Value()

def get_Value():
    print("Get Value")
    servo_state = random.randrange(0,100, step=10)
    print(servo_state)
    return servo_state

def set_Value():
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


def main():
    print("main")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        os._exit(0)

####################
#
if __name__ == "__main__":
    main()
