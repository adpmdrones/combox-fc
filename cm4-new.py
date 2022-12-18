#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import logging
import json

# Create logger
logger = logging.getLogger('CBFC')
logging.basicConfig(level=logging.INFO, filename='/var/log/CBFC-data.log', \
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
					datefmt='%d/%m/%Y %I:%M:%S %p')

# Device Token CM4 Test - ThingsBoard ADPM
device_token = "EeLqJHNQgWR4FtycieRD"

# Drone ID
droneID = "64"

# Wait time between reads (seconds)
wait_time = 0.25

# Endpoints
#
# Mavlink2rest
url_uav = f"http://localhost:8088/mavlink/vehicles/{droneID}/components/1/messages"
#
# ThingsBoard ADPM
url_dashboard = f"http://dashboard.adpmdrones.com:8080/api/v1/{device_token}/telemetry"

while True:
	time.sleep(wait_time)
	try:
		print("Start local request")
		r = requests.get(url_uav , timeout=2)
		data = r.json()

		# Extract data groups
		data_gps = data["GPS_RAW_INT"]["message"]
		data_attitude = data["ATTITUDE"]["message"]
		data_vibration = data["VIBRATION"]["message"]
		data_wind = data["WIND"]["message"]
		data_servo = data["SERVO_OUTPUT_RAW"]["message"]

		r = requests.post(url_dashboard, timeout=2, json=data_gps)
		#logger.info(r.status_code)
		print(r.status_code)
		r = requests.post(url_dashboard, timeout=2, json=data_attitude)
		#logger.info(r.status_code)
		print(r.status_code)


	except KeyboardInterrupt:
		break
	except:
		logger.error("POST Issue")
		pass
