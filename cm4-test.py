#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import logging
import json
import math

# Create logger
logger = logging.getLogger('IRS')
logging.basicConfig(level=logging.INFO, filename='/var/logIRS.log', \
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
					datefmt='%d/%m/%Y %I:%M:%S %p')

# Device Token CM4 Test
device_token = "EeLqJHNQgWR4FtycieRD"

# Drone ID
droneID = "64"

# Endpoints
url_uav = "http://localhost:8088/mavlink/vehicles/" + droneID + "/components/1/messages"
url_dashboard = "http://dashboard.adpmdrones.com:8080/api/v1/" + device_token + "/telemetry"

while True:
	time.sleep(1.0)
	try:
		print("Start local request")
		r = requests.get(url_uav , timeout=2)
		data = r.json()
		#print(data)
		data_gps = data["GPS_RAW_INT"]["message"]
		data_attitude = data["ATTITUDE"]["message"]
		#print("==========")

		ALT = data_gps["alt"]			#
		LAT = data_gps["lat"]			#
		LON = data_gps["lon"]			#
		SAT = data_gps["satellites_visible"]	#
		PIT = data_attitude["pitch"]		#
		RLL = data_attitude["roll"]		#
		YAW = data_attitude["yaw"]		#
		VEL = data_gps["vel"]			# GPS ground speed cm/s

		timestamp = data["ATTITUDE"]["status"]["time"]["last_update"]

		data = '{' + \
			'\"droneid\":' + str(droneID) + \
			',\"timestamp\":\"' + timestamp + '\"' + \
			',\"latitude\":' + str(LAT / 10000000) + \
			',\"longitude\":' + str(LON / 10000000) + \
			',\"altitude\":' + str(ALT / 1000) + \
			',\"speed\":' + str(VEL * 100) + \
			',\"satellites\":' + str(SAT) + \
			',\"pitch\":' + str(PIT) + \
			',\"roll\":' + str(RLL) + \
			',\"yaw\":' + str(YAW) + \
			'}'
		data = json.loads(data)
		print(data)

		r = requests.post(url_dashboard, timeout=2, json=data)
		print(r)


	except KeyboardInterrupt:
		break

	except:
		logger.error("POST Issue")
		pass
