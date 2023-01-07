#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import logging
import json


# Create logger
logger = logging.getLogger('WINDY')
logging.basicConfig(level=logging.INFO, filename='/var/log/WINDY-data.log', \
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
					datefmt='%d/%m/%Y %I:%M:%S %p')

# Windy API token
windy_token = "F0qmICttsRDw0UQ2G7KGw6K9B7FHngEY"


latitude = 0.0
longitude = 0.0
altitude = 0.0

# Wait time between reads (seconds)
wait_time = 10

# Endpoints
#
# Mavlink2rest
url_windy = "https://api.windy.com/api/point-forecast/v2"

data = {
    "lat": 49.809,
    "lon": 16.787,
    "model": "gfs",
    "parameters": ["wind", "dewpoint", "rh", "pressure"],
    "levels": ["surface"],
    "key": "F0qmICttsRDw0UQ2G7KGw6K9B7FHngEY"
}

while True:
    print(f"Start local request to {url_windy}")
    header = {"Content-Type" :"application/json"}
    r = requests.post(url_windy , headers = header, json = data)
    print(json.dumps(r.json(), indent=4))
    time.sleep(wait_time)
