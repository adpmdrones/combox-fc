#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
##########
# by ADPM Drones Srl 2021-2023
##########
#


import time
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import random
import requests
import json

API = "http://localhost:8088"

thingsboard_server = "dashboard.adpmdrones.com"
access_token = "EeLqJHNQgWR4FtycieRD"


# dependently of request method we send different data back
def on_server_side_rpc_request(client, request_id, request_body):
    print(request_id, request_body)
    if request_body["method"] == "getValue":
        print("getValue")
    elif request_body["method"] == "setValue":
        client.send_rpc_reply(request_id, random.randrange(1000,2000, step=250))

client = TBDeviceMqttClient(thingsboard_server, access_token, 1883, 5)
client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
client.connect()


while True:
    time.sleep(2)
