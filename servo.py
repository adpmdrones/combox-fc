#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import requests
import json

API = "http://localhost:8088"

def get(droneID, url_device, servo_num, servo_pos):
    print("Get Servo status")



def set(droneID, url_device, servo_num, servo_pos):
    print("Set servo position")
    print(url_device)
    print(droneID)
    print(servo_num)
    print(servo_pos)
    set_servo(servo_num, servo_pos, droneID)



#
# Control Servo 1 - 16
#
def set_servo(servo_num: int, servo_pos: int, droneID: int):
    servo_message = {
        "header": {
            "system_id": droneID,
            "component_id": 1,
            "sequence": 0
        },
        "message": {
            "type":"COMMAND_LONG",
            "param1":servo_num,
            "param2":servo_pos,
            "param3":0.0,"param4":0.0,"param5":0.0,"param6":0.0,"param7":0.0,
            "command":{
            "type":"MAV_CMD_DO_SET_SERVO"
            },
            "target_system":0,
            "target_component":0,
            "confirmation":0
        }
    }
    print(f"{API}/mavlink")
    print(servo_message)
    response = requests.post(f"{API}/mavlink", json=servo_message)
    return response.status_code == requests.codes.ok



def main():
    print("main")


####################
#
if __name__ == "__main__":
    main()