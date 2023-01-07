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
import bisect

# Gh altitude
#
windy_gh = [150, 200, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000]

# Windy URL
windy_url = "https://api.windy.com/api/point-forecast/v2"

# Windy forecast timespan
windy_forecast = 1	# step. each step forecast is every 3 hours

# Post windy request data
def get_windy(data, url):
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


# Telemetry class
class telemetry:
	timestamp = ''
	lat = 0.0
	lon = 0.0

# Posting telemetry data 
def write_telemetry(data, url_thingsboard):
		try:
			# POST Telemetry data
			r = requests.post(url_thingsboard, timeout=2, json=data)
			status = r.status_code
			print("Windy data post status:", status)
			return (status)
		except KeyboardInterrupt:
			os._exit(0)
		except:
			print("Error posting telemetry data.")
			print("Retrying...")
			time.sleep(5.0)
			pass


def get(url_device, windy_token, lat, lon, press):

    # Windy class
    class windy_class:
        lat = 49.809
        lon = 16.787
        model = 'gfs'
        parameters = ['wind', 'dewpoint', 'rh', 'pressure']
        levels = ['surface', '800h']
        key: 'token'
    print("*" * 20)
    print("Windy data")
    print("url device :" + url_device)
    print("windy_token :" + windy_token)
    print("lat :" + str(lat))
    print("lon :" + str(lon))
    print("press :" + str(press))
    print("*" * 20)

    windy_class = windy_class()

    windy_class.key = windy_token
    windy_class.lat = lat
    windy_class.lon = lon
    windy_class.parameters = ['wind', 'dewpoint', 'rh', 'pressure']
    windy_class.levels = ['surface', '1000']
    windy_class.model = 'gfs'

    jsonWindy = (windy_class.__dict__)
    extracted_gh_index = bisect.bisect(windy_gh, press)
    if extracted_gh_index == 0:
	    extracted_gh_index = 1

    gh_h = str(windy_gh[extracted_gh_index - 1]) + "h"

    windy_class.levels = ['surface', gh_h]

    windy_data = get_windy(jsonWindy, windy_url)

    windy_forecast_span = windy_forecast * 3 * 3600	# transform in seconds

    for n in range (5):

        dt_windy_obj = datetime.fromtimestamp(windy_data["ts"][n]/1000.0)
        dt_windy = int(float(dt_windy_obj.strftime('%s.%f')))

        dt_obj = datetime.utcnow() 
        dt = int(float(dt_obj.strftime('%s.%f')))

        if dt_windy >= dt and dt_windy <= dt + windy_forecast_span:
            
            telem = telemetry()

            if False:
                os.system('clear')
                print("*" * 20)
                print(gh_h)
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
                print(gh_h)
                print("*" * 20)
                print("wind_u-" + gh_h + ":", windy_data["wind_u-" + gh_h][n], windy_data["units"]["wind_u-" + gh_h])
                print("wind_v-" + gh_h + ":", windy_data["wind_v-" + gh_h][n], windy_data["units"]["wind_v-" + gh_h])
                print("dewpoint-" + gh_h + ":", windy_data["dewpoint-" + gh_h][n], windy_data["units"]["dewpoint-" + gh_h])
                print("rh-" + gh_h + ":", windy_data["rh-" + gh_h][n], windy_data["units"]["rh-" + gh_h])   

            telem.windy_timestamp = windy_data["ts"][n]
            telem.wind_u_surface = windy_data["wind_u-surface"][n]
            telem.wind_v_surface = windy_data["wind_v-surface"][n]
            telem.dewpoint_surface = windy_data["dewpoint-surface"][n]
            telem.rh_surface = windy_data["rh-surface"][n]
            telem.pressure_surface = windy_data["pressure-surface"][n]

            telem.h = gh_h
            telem.wind_u_h = windy_data["wind_u-" + gh_h][n]
            telem.wind_v_h = windy_data["wind_v-" + gh_h][n]
            telem.dewpoint_h = windy_data["dewpoint-" + gh_h][n]
            telem.rh_h = windy_data["rh-" + gh_h][n]

            jsonTelem = (telem.__dict__)
            write_telemetry(jsonTelem, url_device)



def main():
    print("main")

if __name__ == "__main__":
    main()