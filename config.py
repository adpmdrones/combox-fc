#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class config(object):
        def config(self):
            ###########################
            # Configuration variables #
            ###########################
            # Device UUID version 4
            combox_UUID = "331f20a2-a36d-4a2a-add1-56dcb1757b5d"

            # Device Token CM4 Test - ThingsBoard ADPM
            device_token = "EeLqJHNQgWR4FtycieRD"
            device_token_ADSB = "ucaEaGMnN491sfbyBP1g"

            # Windy Token
            windy_token = "F0qmICttsRDw0UQ2G7KGw6K9B7FHngEY"
            windy_url = "https://api.windy.com/api/point-forecast/v2"

            # Drone ID - just for setting the variable
            droneID = "1"

            # Wait time between reads (seconds)
            wait_time = 5.0

            # Endpoints
            #
            # Mavlink2rest
            url_uav = f"http://localhost:8088/mavlink/vehicles/{droneID}/components/1/messages" # url_uav - just for setting the variable
        
            # ThingsBoard ADPM
            url_device = f"http://dashboard.adpmdrones.com:8080/api/v1/{device_token}/telemetry"
            url_device_adsb = f"http://dashboard.adpmdrones.com:8080/api/v1/{device_token_ADSB}/telemetry"