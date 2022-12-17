#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import logging
import json

# Create logger
logger = logging.getLogger('CBFC')
logging.basicConfig(level=logging.INFO, filename='/var/log/CBFC-test.log', \
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
					datefmt='%d/%m/%Y %I:%M:%S %p')

# Device Token CM4 Test - ThingsBoard ADPM
device_token = "EeLqJHNQgWR4FtycieRD"

# Drone ID
droneID = "64"

# Wait time between reads (seconds)
wait_time = 0.5

# Endpoints
#
# Mavlink2rest
url_uav = "http://localhost:8088/mavlink/vehicles/" + droneID + "/components/1/messages"
#
# ThingsBoard ADPM
url_dashboard = "http://dashboard.adpmdrones.com:8080/api/v1/" + device_token + "/telemetry"


data = '{
  "header": {
    "system_id": 255,
    "component_id": 240,
    "sequence": 0
  },
  "message": {
    "type":"COMMAND_LONG",
    "param1": 1.0,
    "param2": 0.0,"param3":0.0,"param4":0.0,"param5":0.0,"param6":0.0,"param7":0.0,
    "command": {
      "type": "MAV_CMD_COMPONENT_ARM_DISARM"
    },
    "target_system": 1,
    "target_component": 1,
    "confirmation": 1
  }
}'

r = requests.post(url_dashboard, timeout=2, json=data)



