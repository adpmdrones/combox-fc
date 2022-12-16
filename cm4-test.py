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
wait_time = 0.5

# Endpoints
#
# Mavlink2rest
url_uav = "http://localhost:8088/mavlink/vehicles/" + droneID + "/components/1/messages"
#
# ThingsBoard ADPM
url_dashboard = "http://dashboard.adpmdrones.com:8080/api/v1/" + device_token + "/telemetry"

while True:
	time.sleep(wait_time)
	try:
		print("Start local request")
		r = requests.get(url_uav , timeout=2)
		data = r.json()

		data_gps = data["GPS_RAW_INT"]["message"]
		data_attitude = data["ATTITUDE"]["message"]
		data_vibration = data["VIBRATION"]["message"]
		data_wind = data["WIND"]["message"]

		TIS = data["ATTITUDE"]["status"]["time"]["last_update"]	# Timestamp
		#
		ALT = data_gps["alt"]									# Altitude  (MSL). Positive for up. mm
		LAT = data_gps["lat"]									# Latitude  (WGS84, EGM96 ellipsoid) degE7
		LON = data_gps["lon"]									# Longitude (WGS84, EGM96 ellipsoid) degE7
		VEL = data_gps["vel"]									# GPS ground speed cm/s
		#
		SAT = data_gps["satellites_visible"]					# Number of satellites visible
		PIT = data_attitude["pitch"]							# Pitch angle (-pi..+pi) radians
		RLL = data_attitude["roll"]								# Roll  angle (-pi..+pi) radians
		YAW = data_attitude["yaw"]								# Yaw   angle (-pi..+pi) radians
		#
		VIX = data_vibration["vibration_x"]						# Vibration levels on X-axis
		VIY = data_vibration["vibration_y"]						# Vibration levels on Y-axis
		VIZ = data_vibration["vibration_z"]						# Vibration levels on Z-axis
		#
		WDIR = data_wind["direction"]								#
		WSPD = data_wind["speed"]									#
		WSPDZ = data_wind["speed_z"]								#
		#

		data = '{' + \
			'\"droneid\":' + str(droneID) + \
			',\"timestamp\":\"' + TIS + '\"' + \
			',\"latitude\":' + str(LAT / 10000000) + \
			',\"longitude\":' + str(LON / 10000000) + \
			',\"altitude\":' + str(ALT / 1000) + \
			',\"speed\":' + str(VEL * 100) + \
			',\"satellites\":' + str(SAT) + \
			',\"pitch\":' + str(PIT) + \
			',\"roll\":' + str(RLL) + \
			',\"yaw\":' + str(YAW) + \
			',\"vibration_x\":' +str(VIX) + \
			',\"vibration_y\":' +str(VIY) + \
			',\"vibration_z\":' +str(VIZ) + \
			',\"wind_speed\":' + str(WSPD) + \
			',\"wind_dir\":' + str(WDIR) + \
			',\"wind_speed_z\":' + str(WSPDZ) + \
			'}'

		data = json.loads(data)
		logger.info(data)
		print(data)

		r = requests.post(url_dashboard, timeout=2, json=data)
		logger.info(r.status_code)
		print(r.status_code)

	except KeyboardInterrupt:
		break
	except:
		logger.error("POST Issue")
		pass
