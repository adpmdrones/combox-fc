#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import logging
import json
import os
import random
import math
import datetime

# Windy Token
windy_token = "F0qmICttsRDw0UQ2G7KGw6K9B7FHngEY"
# Windi URL
windy_url = "https://api.windy.com/api/point-forecast/v2"

# Post windy request data
def get_windy(data, url, lat, lon):
		try:
			# POST windy request data
			r = requests.post(url , timeout=2, json=data)
			status = r.status_code
			print(status)
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


windy = windy()

windy.key = windy_token
windy.lat = 42.100
windy.lon = 13.100
windy.key = windy_token
windy.parameters = ['wind', 'dewpoint', 'rh', 'pressure']
windy.levels = ['surface', '800h', '300h']
windy.model = 'gfs'

jsonWindy = (windy.__dict__)
print(jsonWindy)

windy_data = get_windy(jsonWindy, windy_url, 41, 12)
#print("*" * 20)
#print(windy_data)

for n in range (80):
	os.system('clear')
	date = datetime.datetime.fromtimestamp(windy_data["ts"][n]/1000.0)

	print("*" * 20)
	print(date)
	print("*" * 20)
	print("units")
	print("*" * 20)
	print(windy_data["units"])

	print("*" * 20)
	print("Surface")
	print("*" * 20)
	print(windy_data["ts"][n])
	print(windy_data["wind_u-surface"][n])
	print(windy_data["wind_v-surface"][n])
	print(windy_data["dewpoint-surface"][n])
	print(windy_data["rh-surface"][n])
	print(windy_data["pressure-surface"][n])

	print("*" * 20)
	print("300h")
	print("*" * 20)
	print(windy_data["wind_u-300h"][n])
	print(windy_data["wind_v-300h"][n])
	print(windy_data["dewpoint-300h"][n])
	print(windy_data["rh-300h"][n])

	print("*" * 20)
	print("800h")
	print("*" * 20)
	print(windy_data["wind_u-800h"][n])
	print(windy_data["wind_v-800h"][n])
	print(windy_data["dewpoint-800h"][n])
	print(windy_data["rh-800h"][n])

	time.sleep(5)
