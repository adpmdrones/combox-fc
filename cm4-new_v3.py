#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
##########
# by ADPM Drones Srl 2021-2023
##########
#
'''
This Python code is  a script for collecting telemetry data from a drone using the MAVLink protocol
and sending it to a remote ThingsBoard dashboard. 
It uses the "requests" library to make HTTP requests to the drone and send telemetry data to the dashboard.
The script defines several functions for reading MAVLink data from the drone, sending it to the dashboard, 
and handling errors during execution. 
It also includes a "telemetry" class representing the drone's telemetry data and a logger to log events 
and errors during script execution.

To run the script, the ThingsBoard device token and the drone ID must be specified, as well as endpoint 
variables for the drone and dashboard. 
The script then makes periodic requests to the drone for MAVLink data and sends telemetry data to the dashboard via HTTP POST requests.

In order to avoid incorrect behavior when working with the map, we use different devices to show their coordinates on the map
for tracking vehicle and ADSB data
'''

import schedule
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import requests
import logging
import json
import os
import random
import math

import random

import windy as windy_data
import servo

# Create logger
logger = logging.getLogger('CBFC')
logging.basicConfig(level=logging.INFO, filename='/var/log/CBFC-data.log', \
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
					datefmt='%d/%m/%Y %I:%M:%S %p')

###########################
#        Functions        #
###########################

# Reading mavlink stream
#
def read_mavlink(url_uav):
	while True:
		try:
			# Request Mavlink data from UAV
			r = requests.get(url_uav , timeout=2)
			data = r.json()
			return (data)
		except KeyboardInterrupt:
			os._exit(0)
		except:
			print("Error reading mavlink data.")
			print("Retrying...")
			logger.error("Error reading mavlink data.")
			time.sleep(5.0)
			pass

# Posting telemetry data 
#
def write_telemetry(data, url_thingsboard):
		try:
			# POST Telemetry data
			r = requests.post(url_thingsboard, timeout=2, json=data)
			status = r.status_code
			print("Post telemetry status:",status)
			return (status)
		except KeyboardInterrupt:
			os._exit(0)
		except:
			print("Error posting telemetry data.")
			print("Retrying...")
			logger.error("Error posting telemetry data.")
			time.sleep(5.0)
			pass

# Finding mavID
#
def find_mavID(base_url):
	# We try from 1 to 255 to get automatically the mavid
	# Finding mav id
	flag_found_vehicle = False
	while not flag_found_vehicle:
		# retry for different FC boot time
		# if the first run does not return a 
		# vehicle ID
		for n in range (255):
			# Request Mavlink data
			url = base_url + str(n)
			print(url)
			print("Checking vehicle ID " + str(n))
			try:
				r = requests.get(url, timeout=2)
				data = r.json()
				print("Vehicle found @" + url)
				logger.info("Vehicle found @" + url)
				droneID = str(n)
				url_uav = f"http://localhost:8088/mavlink/vehicles/{droneID}/components/1/messages"
				# exit the loop
				# vehicle ID found
				flag_found_vehicle = True
				# Returns url_uav and droneID updated
				#
				return(url_uav, droneID)
			except KeyboardInterrupt:
				os._exit(0)
			except:
				print("Vehicle not found @" + url)
				print("Retrying...")
				logger.error("Vehicle not found @" + url)
				pass
		print("Retry from start...")

# Check autopilot type
#
def check_autopilot(data_telemetry):
	# Check autopilot
	#
	#  3 - MAV_AUTOPILOT_ARDUPILOTMEGA
	# 12 - MAV_AUTOPILOT_PX4
	#
	autopilot = data_telemetry["HEARTBEAT"]["message"]["autopilot"]["type"]		# https://mavlink.io/en/messages/common.html#MAV_AUTOPILOT

	# Check mavtype
	#
	#  1 - MAV_TYPE_FIXED_WING
	#  2 - MAV_TYPE_QUADROTOR
	# 13 - MAV_TYPE_HEXAROTOR
	# 14 - MAV_TYPE_OCTOROTOR
	#
	mavtype_multirotor = ["MAV_TYPE_QUADROTOR", "MAV_TYPE_HEXAROTOR", "MAV_TYPE_OCTOROTOR"]
	mavtype_wing = ["MAV_TYPE_FIXED_WING"]

	mavtype = data_telemetry["HEARTBEAT"]["message"]["mavtype"]["type"]				# https://mavlink.io/en/messages/common.html#MAV_TYPE

	if (autopilot == "MAV_AUTOPILOT_ARDUPILOTMEGA"):
		print(autopilot)
	elif (autopilot == "MAV_AUTOPILOT_PX4"):
		print(autopilot)
	else:
		print("Autopilot not supported. Exiting.")
		logger.error("Autopilot not supported")
		os._exit(0)

	if (mavtype in mavtype_wing):
		print(mavtype)
	elif (mavtype in mavtype_multirotor):
		print(mavtype)
	else:
		print("mavtype not supported. Exiting.")
		logger.error("mavtype not supported")
		os._exit(0)
	# Returns autopilot and mavtype
	#
	return autopilot, mavtype

# Read Windy data
#
def windy_schedule():
	# Windy data @location / surface / altitude
	# Update data for scheduled jobs
	print("*" * 20)
	print("Read Windy data")
	windy_data.get(config.url_device, \
		config.windy_token, \
		data_gps_int["lat"] / 10000000, \
		data_gps_int["lon"] / 10000000, \
		float("{:.4f}".format(data_pressure["press_abs"])) \
		)

def test_schedule():
	print("*" * 20, datetime.utcnow(), "*" * 20)

# MQTT Client
# The callback for when the client receives a CONNACK response from the server.
#
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')

# The callback for when a PUBLISH message is received from the server.
#
def on_message(client, userdata, msg):
	print("*" * 20)
	print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
	# Decode JSON request
	data = json.loads(msg.payload)
	# Check request method
	print(data['method'])
	print("*" * 20)
	if data['method'] in config.servo_get:
		#print("Method GET")
		servo_num = config.servo_get.index(data['method'])
		servo_num = servo_num + 1
		#print(servo_num)
		# Reply with status from mavlink
		client.publish(msg.topic.replace('request', 'response'), get_Value(data['method'].lstrip("get_")), 1)

	elif data['method'] in config.servo_set:
		#print("Method SET")
		servo_num = config.servo_set.index(data['method'])
		servo_num = servo_num + 1
		position = data['params']
		#print(servo_num)
		#print(position)
		# Update status and reply
		set_Value(servo_num, position)

# Get Servo Value
#
def get_Value(servo_name):
	#print("Get Value")
	servo_state = servo_name
	position = data_servo[servo_state]
	#print(servo_state)
	#print(position)
	return position

# Set Servo Value
#
def set_Value(servo_num, position):
	#print("Set Value")
	#print(servo_num)
	#print(position)
	servo.set(droneID, config.url_device, servo_num, position)


###########################
# Configuration variables #
###########################
class config(object):

	# Device UUID version 4
	#
	combox_UUID = "331f20a2-a36d-4a2a-add1-56dcb1757b5d"

	# Device Token CM4 Test - ThingsBoard ADPM
	#
	device_token = "EeLqJHNQgWR4FtycieRD"
	device_token_ADSB = "ucaEaGMnN491sfbyBP1g"

	# Windy Token
	#
	windy_token = "F0qmICttsRDw0UQ2G7KGw6K9B7FHngEY"
	windy_url = "https://api.windy.com/api/point-forecast/v2"

	# Drone ID - just for setting the variable
	#
	droneID = "1"

	# Wait time between reads (seconds)
	#
	wait_time = 2.5

	# Endpoints
	#
	# Mavlink2rest
	#
	url_uav = f"http://localhost:8088/mavlink/vehicles/{droneID}/components/1/messages" # url_uav - just for setting the variableurl_vehicle = "http://localhost:8088/mavlink/vehicles/"
	url_vehicle = "http://localhost:8088/mavlink/vehicles/"
	url_api = API = "http://localhost:8088"

	servo_get = ["get_servo1_raw", "get_servo2_raw", "get_servo3_raw", "get_servo4_raw", "get_servo5_raw", "get_servo6_raw", "get_servo7_raw", "get_servo8_raw"]
	servo_set = ["set_servo1_raw", "set_servo2_raw", "set_servo3_raw", "set_servo4_raw", "set_servo5_raw", "set_servo6_raw", "set_servo7_raw", "set_servo8_raw"]

	# ThingsBoard ADPM
	#
	url_base = "dashboard.adpmdrones.com"
	url_device = f"http://dashboard.adpmdrones.com:8080/api/v1/{device_token}/telemetry"
	url_device_adsb = f"http://dashboard.adpmdrones.com:8080/api/v1/{device_token_ADSB}/telemetry"

# Telemetry class
#
class telemetry:
	droneid = 1				# DroneID
	timestamp = ''			# timestamp

# ADSB class
#
class telemetry_adsb:
	droneid = 1				# DroneID
	timestamp = ''			# timestamp

# ADSB list
# 
adsb_list = []

###########################
#          Start          #
###########################

# Read config variables
#
config = config()

# MQTT
#
client = mqtt.Client()
# Register connect callback
client.on_connect = on_connect
# Registed publish message callback
client.on_message = on_message
# Set access token
client.username_pw_set(config.device_token)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(config.url_base, 1883, 60)

# Start MQTT Loop
#
client.loop_start()

# Finding mavID from the telemetry stream
# returns url_uav and droneID
#
url_uav, droneID = find_mavID(config.url_vehicle)

# Read mavlink stream
# with the correct mavID
#
data = read_mavlink(url_uav)

# Check autopilot
# and return autopilot and mavtype
#
#  3 - MAV_AUTOPILOT_ARDUPILOTMEGA
# 12 - MAV_AUTOPILOT_PX4
#
autopilot, mavtype = check_autopilot(data)

# Test scheduling jobs
#
#schedule.every(10).seconds.do(test_schedule)

# Scheduling Windy data
# every 5 minutes
#
schedule.every(5).minutes.do(windy_schedule)

flag_windy_first_run = False

# Start loop
# telemetry post to dashboard
#
while True:
	#
	telem = telemetry()
	adsb = telemetry_adsb()
	#
	# Reading mavlink data
	data = read_mavlink(url_uav)
	telem.timestamp = data["ATTITUDE"]["status"]["time"]["last_update"]

	telem.droneid = droneID
	telem.autopilot = autopilot
	telem.mavtype = mavtype
	telem.combox_UUID = config.combox_UUID

	adsb.timestamp = telem.timestamp
	adsb.droneid = telem.droneid
	
	# Check if ADSB data is available
	if "ADSB_VEHICLE" in data:
		# Read ADSB data
		data_adsb = data["ADSB_VEHICLE"]["message"]							# https://mavlink.io/en/messages/common.html#ADSB_VEHICLE
		data_adsb_status = data["ADSB_VEHICLE"]["status"]
		# Update
		telem.adsb_lat = data_adsb["lat"] / 10000000						# Latitude  (WGS84, EGM96 ellipsoid) degE7
		telem.adsb_lon = data_adsb["lon"] / 10000000						# Longitude (WGS84, EGM96 ellipsoid) degE7
		telem.adsb_heading = data_adsb["heading"] / 100						# Course over ground cDeg
		telem.adsb_hor_velocity = data_adsb["hor_velocity"] /100 			# The horizontal velocity cm/s
		telem.adsb_ver_velocity = data_adsb["ver_velocity"] / 100			# The vertical velocity. Positive is up
		telem.adsb_squawk = data_adsb["squawk"]								# Squawk code
		telem.adsb_type = data_adsb["type"]									# 
		telem.adsb_tslc = data_adsb["tslc"]									# Time since last communication in seconds
		# Update
		adsb.adsb_lat = data_adsb["lat"] / 10000000							# Latitude  (WGS84, EGM96 ellipsoid) degE7
		adsb.adsb_lon = data_adsb["lon"] / 10000000							# Longitude (WGS84, EGM96 ellipsoid) degE7
		adsb.adsb_heading = data_adsb["heading"] / 100						# Course over ground cDeg
		adsb.adsb_hor_velocity = data_adsb["hor_velocity"] /100 			# The horizontal velocity cm/s
		adsb.adsb_ver_velocity = data_adsb["ver_velocity"] / 100			# The vertical velocity. Positive is up
		adsb.adsb_squawk = data_adsb["squawk"]								# Squawk code
		adsb.adsb_type = data_adsb["type"]									# 
		adsb.adsb_tslc = data_adsb["tslc"]									# Time since last communication in seconds
		adsb.adsb_icao = data_adsb["ICAO_address"]
		adsb.adsb_alt = data_adsb["altitude"]
		adsb.adsb_alt_type = data_adsb["altitude_type"]["type"]
		adsb.adsb_emitter = data_adsb["emitter_type"]["type"]
		adsb.adsb_callsign = data_adsb["callsign"]
		adsb.adsb_last_update = data_adsb_status["time"]["last_update"]
		
	#
	# Check if WIND data is available
	if "WIND" in data:
		# Read wind data
		data_wind = data["WIND"]["message"]
		# Update
		telem.wind_dir = data_wind["direction"]
		telem.wind_speed = data_wind["speed"]
		telem.wind_speed_z = data_wind["speed_z"]
	#
	data_gps_raw_int = data["GPS_RAW_INT"]["message"]						# https://mavlink.io/en/messages/common.html#GPS_RAW_INT
	telem.vel = data_gps_raw_int["vel"] / 100								# GPS ground speed cm/s
	telem.satellites = data_gps_raw_int["satellites_visible"]				# Number of satellites visible
	#
	data_gps_int = data["GLOBAL_POSITION_INT"]["message"]					# https://mavlink.io/en/messages/common.html#GLOBAL_POSITION_INT
	telem.altitude_msl = data_gps_int["alt"] / 1000							# Altitude  (MSL). Positive for up. mm
	telem.altitude = data_gps_int["relative_alt"] / 1000					# Altitude above ground
	telem.latitude = data_gps_int["lat"] / 10000000							# Latitude  (WGS84, EGM96 ellipsoid) degE7
	telem.longitude = data_gps_int["lon"] / 10000000						# Longitude (WGS84, EGM96 ellipsoid) degE7
	telem.heading = data_gps_int["hdg"]										# Vehicle heading (yaw angle), 0.0..359.99 degrees
	telem.vx = float("{:.4f}".format(data_gps_int["vx"] / 100))								# Ground X Speed (Latitude, positive north) cm/s
	telem.vy = float("{:.4f}".format(data_gps_int["vy"] / 100))								# Ground Y Speed (Longitude, positive east) cm/s
	telem.vz = float("{:.4f}".format(data_gps_int["vz"] / 100))								# Ground Z Speed (Altitude, positive down) cm/s
	#
	data_attitude = data["ATTITUDE"]["message"]												# https://mavlink.io/en/messages/common.html#ATTITUDE
	telem.pitch = float("{:.4f}".format(math.degrees(data_attitude["pitch"])))				# Pitch angle (-pi..+pi) radians
	telem.roll = float("{:.4f}".format(math.degrees(data_attitude["roll"])))				# Roll  angle (-pi..+pi) radians
	telem.yaw = float("{:.4f}".format(math.degrees(data_attitude["yaw"])))					# Yaw   angle (-pi..+pi) radians
	telem.pitch_speed = float("{:.4f}".format(data_attitude["pitchspeed"]))					# Ground X Speed (Latitude, positive north) cm/s
	telem.roll_speed = float("{:.4f}".format(data_attitude["rollspeed"]))					# Ground Y Speed (Longitude, positive east) cm/s
	telem.yaw_speed = float("{:.4f}".format(data_attitude["yawspeed"]))						# Ground Z Speed (Altitude, positive down) cm/s
	#
	data_vibration = data["VIBRATION"]["message"]											# https://mavlink.io/en/messages/common.html#VIBRATION 
	telem.vibration_x = float("{:.4f}".format(data_vibration["vibration_x"]))				# Vibration levels on X-axis
	telem.vibration_y = float("{:.4f}".format(data_vibration["vibration_y"]))				# Vibration levels on Y-axis
	telem.vibration_z = float("{:.4f}".format(data_vibration["vibration_z"]))				# Vibration levels on Z-axis
	#
	data_servo = data["SERVO_OUTPUT_RAW"]["message"]						# https://mavlink.io/en/messages/common.html#SERVO_OUTPUT_RAW
	telem.servo1 = data_servo["servo1_raw"]									# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.servo2 = data_servo["servo2_raw"]									# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.servo3 = data_servo["servo3_raw"]									# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.servo4 = data_servo["servo4_raw"]									# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.servo5 = data_servo["servo5_raw"]									# Value 900-2100 ms
	telem.servo6 = data_servo["servo6_raw"]									# Value 900-2100 ms
	telem.servo7 = data_servo["servo7_raw"]									# Value 900-2100 ms
	telem.servo8 = data_servo["servo8_raw"]									# Value 900-2100 ms
	telem.servo9 = data_servo["servo9_raw"]									# Value 900-2100 ms
	telem.servo10 = data_servo["servo10_raw"]								# Value 900-2100 ms
	telem.servo11 = data_servo["servo11_raw"]								# Value 900-2100 ms
	telem.servo12 = data_servo["servo12_raw"]								# Value 900-2100 ms
	telem.servo13 = data_servo["servo13_raw"]								# Value 900-2100 ms
	telem.servo14 = data_servo["servo14_raw"]								# Value 900-2100 ms
	telem.servo15 = data_servo["servo15_raw"]								# Value 900-2100 ms
	telem.servo16 = data_servo["servo16_raw"]								# Value 900-2100 ms
	#
	data_vfr = data["VFR_HUD"]["message"]									# https://mavlink.io/en/messages/common.html#VFR_HUD
	telem.vfr_airspeed = data_vfr["airspeed"]								# Vehicle speed in form appropriate for vehicle type.
																			# For standard aircraft this is typically calibrated airspeed (CAS)
																			# or indicated airspeed (IAS) - either of which can be used by a pilot
																			# to estimate stall speed. m/s
	telem.vfr_alt = data_vfr["alt"]											# Current altitude (MSL) m
	telem.vfr_climb = data_vfr["climb"]										# Current climb rate m/s
	telem.vfr_speed = data_vfr["groundspeed"]								# Current ground speed m/s
	telem.vfr_heading = data_vfr["heading"]									# Current heading in compass units (0-360, 0=north) Deg

	data_pressure = data["SCALED_PRESSURE"]["message"] 						# https://mavlink.io/en/messages/common.html#SCALED_PRESSURE
	telem.press_abs = float("{:.4f}".format(data_pressure["press_abs"]))	# Absolute pressure hPa
	telem.press_dif = float("{:.4f}".format(data_pressure["press_diff"]))	# Differential pressure hPa
	telem.press_tmp = data_pressure["temperature"] / 100					# Absolute pressure temperature cdegC

	# jsonTelem = json.dumps(telem.__dict__)
	# jsonTelem will be dumped in write_telemetry

	# Get Windy data at boot
	#
	if not flag_windy_first_run:
		windy_schedule()
		flag_windy_first_run = True

	# Checking scheduled jobs
	#
	schedule.run_pending()

	###########################
	# send telemetry to
	# dashboard
	###########################
	#
	jsonTelem = (telem.__dict__)
	if False:
		print("*" * 20)
		print("Telemetry data:\n", json.dumps(jsonTelem, indent=4))
		print("*" * 20)
		print("URL:\n", config.url_device)
		print("*" * 20)
	write_telemetry(jsonTelem, config.url_device)

	# ADSB data
	#
	if "ADSB_VEHICLE" in data:
		jsonADSB = (adsb.__dict__)
		print(jsonADSB)
		print(config.url_device_adsb)
		write_telemetry(jsonADSB, config.url_device_adsb)

		# Update ADSB list
		icao = jsonADSB['adsb_icao']
		print(icao)
		result = next((item for item in adsb_list if item["adsb_icao"] == icao), None)
		print(result)
		if  result is None:
			# Add new ADSB data to the list
			adsb_list.append(jsonADSB)
			print("==================================================")
			print("ADSB List element added.")
			print("==================================================\n")
		else:
			# Update ADSB data
			# First remove data
			adsb_list = [item for item in adsb_list if item.get('adsb_icao') != icao]
			# Add updated ADSB data to the list
			adsb_list.append(jsonADSB)
			print("==================================================")
			print("ADSB List element updated.")
			print("==================================================\n")

		print("ADSB list")
		print("==================================================")
		for adsb_callsign in adsb_list:
			print("Last Update :", adsb_callsign["adsb_last_update"], "Callsign :",adsb_callsign["adsb_icao"], adsb_callsign["adsb_alt_type"], adsb_callsign["adsb_emitter"])
		print("\n")

	# Test servo set position
	#
	#servo.set(droneID, config.url_device, random.randrange(5,8), random.randrange(1000,2000, step=250))



	# Wait for next update
	time.sleep(config.wait_time)
