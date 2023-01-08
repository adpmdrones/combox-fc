#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import requests
import json


def get(url_device, url_drone, servo_num, servo_pos):
    print("Get Servo status")



def set(url_device, url_drone, servo_num, servo_pos):
    print("Set servo position")
    print(url_device)
    print(url_drone)
    print(servo_num)
    print(servo_pos)



#
# Control Servo 1 - 16
#
def set_servo(servo_num: int, servo_value: int):
    arm_message = {
        "header": {
            "system_id": 1,
            "component_id": 1,
            "sequence": 0
        },
        "message": {
            "type":"COMMAND_LONG",
            "param1":servo_num,
            "param2":servo_value,
            "param3":0.0,"param4":0.0,"param5":0.0,"param6":0.0,"param7":0.0,
            "command":{
            "type":"MAV_CMD_DO_SET_SERVO"
            },
            "target_system":0,
            "target_component":0,
            "confirmation":0
        }
    }

    response = requests.post(f"{API}/mavlink", json=arm_message)
    return response.status_code == requests.codes.ok



def main():
    print("main")


####################
#
if __name__ == "__main__":
    main()