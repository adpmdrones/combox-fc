#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
##########
# by ADPM Drones Srl 2021-2023
##########
#


import time
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import requests
import json
import os

API = "http://localhost:8088"

thingsboard_server = "dashboard.adpmdrones.com"
access_token = "EeLqJHNQgWR4FtycieRD"


from time import time
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo


telemetry_with_ts = {"servots": int(round(time() * 1000)), "servo5": 1000}
client = TBDeviceMqttClient(thingsboard_server, access_token)
# we set maximum amount of messages sent to send them at the same time. it may stress memory but increases performance
client.max_inflight_messages_set(100)
client.connect()
results = []
result = True
for i in range(0, 100):
    results.append(client.send_telemetry(telemetry_with_ts))
for tmp_result in results:
    result &= tmp_result.get() == TBPublishInfo.TB_ERR_SUCCESS
print("Result", str(result))
client.disconnect()
