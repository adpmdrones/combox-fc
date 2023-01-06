#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This Python code is  a script for collecting telemetry data from a drone using the MAVLink protocol
# and sending it to a remote ThingsBoard dashboard. 
# It uses the "requests" library to make HTTP requests to the drone and send telemetry data to the dashboard.
# The script defines several functions for reading MAVLink data from the drone, sending it to the dashboard, 
# and handling errors during execution. 
# It also includes a "telemetry" class representing the drone's telemetry data and a logger to log events 
# and errors during script execution.
#
# To run the script, the ThingsBoard device token and the drone ID must be specified, as well as endpoint 
# variables for the drone and dashboard. 
# The script then makes periodic requests to the drone for MAVLink data and sends telemetry data to the dashboard via HTTP POST requests.

# In order to avoid incorrect behavior when working with the map, we use different devices to show their coordinates on the map
# for tracking vehicle and ADSB data

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
			return (status)
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



windy.key = windy_token
windy.lat = 42.100
windy.lon = 13.100

jsonWindy = (windy.__dict__)
print(jsonWindy)

windy_data = get_windy(jsonWindy, windy_url, 41, 12)
print(windy_data)
print("*" * 20)

