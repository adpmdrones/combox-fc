#!/usr/bin/env python3

import aiohttp
import asyncio
import json
import requests
import time

API = "http://localhost:8088"

droneID = "64"

def vehicle_mode():
    response = requests.get(f"{API}/mavlink/vehicles/{droneID}/components/1/messages/HEARTBEAT").json()
    return response["message"]["base_mode"]["bits"]

def set_arm(arm: int):
    arm_message = {
        "header": {
            "system_id": 1,
            "component_id": 1,
            "sequence": 0
        },
        "message": {
            "type":"COMMAND_LONG",
            "param1":arm,
            "param2":0.0,"param3":0.0,"param4":0.0,"param5":0.0,"param6":0.0,"param7":0.0,
            "command":{
            "type":"MAV_CMD_COMPONENT_ARM_DISARM"
            },
            "target_system":0,
            "target_component":0,
            "confirmation":0
        }
    }

    response = requests.post(f"{API}/mavlink", json=arm_message)
    return response.status_code == requests.codes.ok

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

#
# Set Flight Mode
#
def set_fmode(fmode: int):
    arm_message = {
        "header": {
            "system_id": 1,
            "component_id": 1,
            "sequence": 0
        },
        "message": {
            "type":"COMMAND_LONG",
            "param1":"MAV_MODE_AUTO",
            "param2":0.0,
            "param3":0.0,
            "param4":0.0,
            "param5":0.0,
            "param6":0.0,
            "param7":0.0,
            "command":{
            "type":"MAV_CMD_DO_SET_MODE"
            },
            "target_system":0,
            "target_component":0,
            "confirmation":0
        }
    }

    response = requests.post(f"{API}/mavlink", json=arm_message)
    return response.status_code == requests.codes.ok


async def start_client(url: str, amount: int) -> None:
    ws = await aiohttp.ClientSession().ws_connect(url, autoclose=False, autoping=False)

    async def dispatch():
        msgs = []
        while len(msgs) < amount:
            msg = await ws.receive()

            if msg.type == aiohttp.WSMsgType.TEXT:
                msgs += [json.loads(msg.data.strip())]
            elif msg.type == aiohttp.WSMsgType.BINARY:
                pass
            elif msg.type == aiohttp.WSMsgType.PING:
                await ws.pong()
            elif msg.type == aiohttp.WSMsgType.PONG:
                pass
            else:
                if msg.type == aiohttp.WSMsgType.CLOSE:
                    await ws.close()
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print("Error during receive %s" % ws.exception())
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    pass

                break
        return msgs

    return await dispatch()


print("Test info..")
response = requests.get(f"{API}/info").json()

assert(response["version"] >= 0), "Info version is invalid."
assert(response["service"]["name"] == "mavlink2rest"), "Invalid service name."
assert(len(response["service"]["sha"]) != 0), "Invalid sha length."

print("Test heartbeat..")
response = requests.get(f"{API}/mavlink/vehicles/64/components/1/messages/HEARTBEAT").json()

assert(response["message"]["type"] == "HEARTBEAT"), "Message type is incorrect."
assert(response["message"]["autopilot"]["type"]), "Autopilot type does not exist."
assert(response["status"]["time"]["frequency"] > 0.0), "Heartbeat frequency is wrong."

servo_num = [5, 6, 7, 8]
servo_pos = [1100, 1500, 1900, 1500]
servo_wait = 2

print("test servo..")
for x in servo_num:
    for y in servo_pos:
        print("Servo: " + str(x) + " postion: " + str(y))
        assert(set_servo(x, y)), "Fail to send SERVO command"
        time.sleep(servo_wait)

print("Test ARM and DISARM..")
assert(set_arm(0)), "Fail to send DISARM command"
time.sleep(1)
assert((vehicle_mode() & 128)  == 0), "Vehicle appears to be ARMED."
assert(set_arm(1)), "Fail to send ARM command"
time.sleep(1)
assert((vehicle_mode() & 128) != 0), "Failed to ARM vehicle."

#print("Test change mode to AUTO")
print(vehicle_mode())
#assert(set_fmode(0)), "Fail to send change mode to AUTO command"

print("Test pretty..")
response = requests.get(f"{API}/mavlink/vehicles/{droneID}/components/1/messages/HEARTBEAT")
assert(response.text.count('\n') == 26), "Pretty heartbeat does not look correct."

async def test_websocket_fetch_filter():
    print("Test websocket..")
    msgs = await start_client(f"{API}/ws/mavlink", 30)
    assert(len(list(filter(lambda msg: msg["message"]["type"] == "HEARTBEAT", msgs))) != 30), "Failed to fetch more than one type of msg."
    msgs = await start_client(f"{API}/ws/mavlink?filter=HEARTBEAT", 30)
    assert(len(list(filter(lambda msg: msg["message"]["type"] == "HEARTBEAT", msgs))) == 30), "Filter failed."

asyncio.run(test_websocket_fetch_filter())