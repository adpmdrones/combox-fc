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

thingsboard_server = 'dashboard.adpmdrones.com'
access_token = 'EeLqJHNQgWR4FtycieRD'


def main():

        # Callback for server RPC requests (Used for control servo and led blink)
    def on_server_side_rpc_request(client, request_id, request_body):
        if request_body['method'] == 'getValue':
            servo_angle = float(request_body['params'])
            getValue(servo_angle)

        elif request_body['method'] == 'setValue':
            client.send_rpc_reply(request_id, servo_angle)
            setValue(request_id, servo_angle)

    # Connecting to ThingsBoard
    client = TBDeviceMqttClient(thingsboard_server, access_token)
    client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
    client.connect()


def getValue(status):
    print("Get Value")
    print("Servo Angle Status", status)


def setValue(pin, status):
    print("Set Value")
    print(pin)
    print(status)



if __name__ == '__main__':
    main()
