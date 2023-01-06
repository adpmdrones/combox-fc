#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import logging
import json
import os
import random
import math


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
windy.levels = ['surface']
windy.model = 'gfs'

jsonWindy = (windy.__dict__)
print(jsonWindy)

windy_data = get_windy(jsonWindy, windy_url, 41, 12)
print(windy_data)
print("*" * 20)

