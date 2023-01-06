#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import logging
import json
import os
import random
import math
from datetime import datetime


# Device Token CM4 Test - ThingsBoard ADPM
device_token = "EeLqJHNQgWR4FtycieRD"

# ThingsBoard ADPM
url_device = f"http://dashboard.adpmdrones.com:8080/api/v1/{device_token}/telemetry"

# Windy Token
windy_token = "F0qmICttsRDw0UQ2G7KGw6K9B7FHngEY"
# Windy URL
windy_url = "https://api.windy.com/api/point-forecast/v2"
# Windy forecast timespan
windy_forecast = 2	# step. each step forecast is every 3 hours

# Post windy request data
def get_windy(data, url, lat, lon):
		try:
			# POST windy request data
			r = requests.post(url , timeout=2, json=data)
			status = r.status_code
			#print(status)
			data = r.json()
			return (data)
		except KeyboardInterrupt:
			os._exit(0)
		except:
			print("Error getting windy data.")
			print("Retrying...")
			time.sleep(5.0)
			pass

# Windy class
class windy:
	lat = 49.809
	lon = 16.787
	model = 'gfs'
	parameters = ['wind', 'dewpoint', 'rh', 'pressure']
	levels = ['surface', '800h', '300h']
	key: 'F0qmICttsRDw0UQ2G7KGw6K9B7FHngEY'

# Posting telemetry data 
def write_telemetry(data, url_thingsboard):
		try:
			# POST Telemetry data
			r = requests.post(url_thingsboard, timeout=2, json=data)
			status = r.status_code
			print(status)
			return (status)
		except KeyboardInterrupt:
			os._exit(0)
		except:
			print("Error posting telemetry data.")
			print("Retrying...")
			logger.error("Error posting telemetry data.")
			time.sleep(5.0)
			pass

# Telemetry class
class telemetry:
	lat = 49.809
	lon = 16.787

# Start
#
windy = windy()

windy.key = windy_token
windy.lat = 42.100
windy.lon = 13.100
windy.key = windy_token
windy.parameters = ['wind', 'dewpoint', 'rh', 'pressure']
windy.levels = ['surface', '800h', '300h']
windy.model = 'gfs'

jsonWindy = (windy.__dict__)
#print(jsonWindy)

windy_data = get_windy(jsonWindy, windy_url, 41, 12)
#print("*" * 20)
#print(windy_data)

windy_forecast_span = windy_forecast * 3 * 3600	# transform in seconds

for n in range (6):
	telem = telemetry()

	dt_windy_obj = datetime.fromtimestamp(windy_data["ts"][n]/1000.0)
	dt_windy = int(float(dt_windy_obj.strftime('%s.%f')))

	dt_obj = datetime.utcnow() 
	dt = int(float(dt_obj.strftime('%s.%f')))

	if dt_windy >= dt and dt_windy <= dt + windy_forecast_span:


		os.system('clear')
		print("*" * 20)
		print("Windy ts ", dt_windy)
		print("Box ts ", dt)
		print("Record: " + str(n), datetime.fromtimestamp(dt_windy))
		print("*" * 20)
		print("units")
		print("*" * 20)
		print("Surface")
		print("*" * 20)
		print(windy_data["ts"][n])
		print("wind_u-surface:", windy_data["wind_u-surface"][n], windy_data["units"]["wind_u-surface"])
		print("wind_v-surface:", windy_data["wind_v-surface"][n], windy_data["units"]["wind_v-surface"])
		print("dewpoint-surface:", windy_data["dewpoint-surface"][n], windy_data["units"]["dewpoint-surface"])
		print("rh-surface:", windy_data["rh-surface"][n], windy_data["units"]["rh-surface"])
		print("pressure-surface:", windy_data["pressure-surface"][n], windy_data["units"]["pressure-surface"])

		print("*" * 20)
		print("300h")
		print("*" * 20)
		print("wind_u-300h:", windy_data["wind_u-300h"][n], windy_data["units"]["wind_u-300h"])
		print("wind_v-300h:", windy_data["wind_v-300h"][n], windy_data["units"]["wind_v-300h"])
		print("dewpoint-300h:", windy_data["dewpoint-300h"][n], windy_data["units"]["dewpoint-300h"])
		print("rh-300h:", windy_data["rh-300h"][n], windy_data["units"]["rh-300h"])

		print("*" * 20)
		print("800h")
		print("*" * 20)
		print("wind_u-800h:", windy_data["wind_u-800h"][n], windy_data["units"]["wind_u-800h"])
		print("wind_v-800h:", windy_data["wind_v-800h"][n], windy_data["units"]["wind_v-800h"])
		print("dewpoint-800h:", windy_data["dewpoint-800h"][n], windy_data["units"]["dewpoint-800h"])
		print("rh-800h:", windy_data["rh-800h"][n], windy_data["units"]["rh-800h"])
 
		telem.wind_u_surface = [windy_data["wind_u-surface"][n], windy_data["wind_u-300h"][n]]
		telem.wind_v_surface = windy_data["wind_v-surface"][n]
		telem.dewpoint_surface = windy_data["dewpoint-surface"][n]
		telem.rh_surface = windy_data["rh-surface"][n]
		telem.pressure_surface = windy_data["pressure-surface"][n]

		telem.wind_u_300h = windy_data["wind_u-300h"][n]
		telem.wind_v_300h = windy_data["wind_v-300h"][n]
		telem.dewpoint_300h = windy_data["dewpoint-300h"][n]
		telem.rh_300h = windy_data["rh-300h"][n]

		telem.wind_u_800h = windy_data["wind_u-800h"][n]
		telem.wind_v_800h = windy_data["wind_v-800h"][n]
		telem.dewpoint_800h = windy_data["dewpoint-800h"][n]
		telem.rh_800h = windy_data["rh-800h"][n]
		time.sleep(2)

	jsonTelem = (telem.__dict__)
	write_telemetry(jsonTelem, url_device)


