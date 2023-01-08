#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
'''
This script contains a function called set_servo that sends an HTTP POST request to the specified API endpoint (http://localhost:8088)
with a JSON payload containing several key-value pairs.
The purpose of the request is to control a servo (a rotary actuator used in robotics) connected to a drone.

The set_servo function takes three arguments:

servo_num: an integer representing the number of the servo to control (valid values are 1-16)
servo_pos: an integer representing the position to set the servo to
droneID: an integer representing the ID of the drone the servo is connected to

The function constructs a dictionary object, servo_message, containing the JSON payload to be sent in the request.
This payload contains several key-value pairs representing various parameters, such as the system ID and component ID of the drone,
the servo number and position to set, and the command type (in this case, MAV_CMD_DO_SET_SERVO).

The function then sends an HTTP POST request to the API endpoint with the servo_message dictionary as the JSON payload.
The response from the API is stored in the response variable.
The function returns True if the request was successful (indicated by a status code of 200), and False otherwise.

The script also contains a set function that calls the set_servo function with the provided arguments, and a main function that does nothing.
The if __name__ == "__main__": block at the bottom of the script calls the main function when the script is run directly, but not when it is 
imported as a module.
'''
import requests
import json

API = "http://localhost:8088"

#
# Set servo position
#
def set(droneID, url_device, servo_num, servo_pos):
    print("*" * 20)
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
            "system_id": int(droneID),
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
    #print(f"{API}/mavlink")
    #print(servo_message)
    response = requests.post(f"{API}/mavlink", json=servo_message)
    print("Servo set -> ", requests.codes.ok)
    print("*" * 20)
    return response.status_code == requests.codes.ok

def main():
    print("main")

####################
#
if __name__ == "__main__":
    main()