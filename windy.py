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
gh = [150, 200, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000]


def get(url_device, windy_token, lat, lon, press):

    # Windy class
    class windy_class:
        lat = 49.809
        lon = 16.787
        model = 'gfs'
        parameters = ['wind', 'dewpoint', 'rh', 'pressure']
        levels = ['surface', '800h']
        key: 'token'

    print("Windy data")
    print("url device :" + url_device)
    print("windy_token :" + windy_token)
    print("lat :" + str(lat))
    print("lon :" + str(lon))
    print("press :" + str(press))

    windy_class = windy_class()

    windy_class.key = windy_token
    windy_class.lat = lat
    windy_class.lon = lon
    windy_class.parameters = ['wind', 'dewpoint', 'rh', 'pressure']
    windy_class.levels = ['surface', '1000']
    windy_class.model = 'gfs'

    jsonWindy = (windy.__dict__)
    extracted_gh_index = bisect.bisect(gh, press)
    if extracted_gh_index == 0:
	    extracted_gh_index = 1

    levelh = str(windy_gh[gh - 1]) + "h"

    windy_class.levels = ['surface', levelh]





def main():
    print("main")

if __name__ == "__main__":
    main()