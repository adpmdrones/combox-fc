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


import time
import requests
import logging
import json
import os
import random
import math

# Create logger
logger = logging.getLogger('CBFC')
logging.basicConfig(level=logging.INFO, filename='/var/log/CBFC-data.log', \
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
					datefmt='%d/%m/%Y %I:%M:%S %p')

# Device Token CM4 Test - ThingsBoard ADPM
device_token = "EeLqJHNQgWR4FtycieRD"

# Drone ID
droneID = "1"

# Wait time between reads (seconds)
wait_time = 1.0

# Decimals to show
dcm = "2"

# Endpoints
#
# Mavlink2rest
url_uav = f"http://localhost:8088/mavlink/vehicles/{droneID}/components/1/messages"
url_vehicle = "http://localhost:8088/mavlink/vehicles/"

#
# ThingsBoard ADPM
url_dashboard = f"http://dashboard.adpmdrones.com:8080/api/v1/{device_token}/telemetry"

# Reading mavlink stream
def read_mavlink(droneID, url_uav):
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
def write_telemetry(data, url_dashboard):
		try:
			# POST Telemetry data
			r = requests.post(url_dashboard, timeout=2, json=data)
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
	droneid = 1				# DroneID
	timestamp = ''			# timestamp

# Finding mav id
for n in range (255):
	# Request Mavlink data from UAV
	print(url_vehicle + str(n))
	r = requests.get(url_vehicle + str(n) , timeout=2)
	#data = r.json()
	print(r)
	print("==========")
	print(n)
	print("==========")
	if mavid != "None":
		print("droneID : " + str(n))
		droneID = str(n)
		break

# Read mavlink for autopilot, mavtype
data = read_mavlink(droneID, url_uav)
#
# Check autopilot
#
#  3 - MAV_AUTOPILOT_ARDUPILOTMEGA
# 12 - MAV_AUTOPILOT_PX4

autopilot = data["HEARTBEAT"]["message"]["autopilot"]["type"]		# https://mavlink.io/en/messages/common.html#MAV_AUTOPILOT

# Check mavtype
#
#  1 - MAV_TYPE_FIXED_WING
#  2 - MAV_TYPE_QUADROTOR
# 13 - MAV_TYPE_HEXAROTOR
# 14 - MAV_TYPE_OCTOROTOR

mavtype_multirotor = ["MAV_TYPE_QUADROTOR", "MAV_TYPE_HEXAROTOR", "MAV_TYPE_OCTOROTOR"]
mavtype_wing = ["MAV_TYPE_FIXED_WING"]

mavtype = data["HEARTBEAT"]["message"]["mavtype"]["type"]			# https://mavlink.io/en/messages/common.html#MAV_TYPE

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

# Start loop
while True:
	#
	telem = telemetry()
	#
	# Reading mavlink data
	data = read_mavlink(droneID, url_uav)
	telem.timestamp = data["ATTITUDE"]["status"]["time"]["last_update"]
	telem.droneid = droneID
	telem.autopilot = autopilot
	telem.mavtype = mavtype

	# Check if ADSB data is available
	if "ADSB_VEHICLE" in data:
		# Read ADSB data
		data_adsb = data["ADSB_VEHICLE"]["message"]					# https://mavlink.io/en/messages/common.html#ADSB_VEHICLE
		# Update
		telem.adsb_lat = data_adsb["lat"] / 10000000				# Latitude  (WGS84, EGM96 ellipsoid) degE7
		telem.adsb_lon = data_adsb["lon"] / 10000000				# Longitude (WGS84, EGM96 ellipsoid) degE7
		telem.adsb_heading = data_adsb["heading"] / 100				# Course over ground cDeg
		telem.adsb_hor_velocity = data_adsb["hor_velocity"] /100 	# The horizontal velocity cm/s
		telem.adsb_ver_velocity = data_adsb["ver_velocity"] / 100	# The vertical velocity. Positive is up
		telem.adsb_squawk = data_adsb["squawk"]						# Squawk code
		telem.adsb_type = data_adsb["type"]							# 
		telem.adsb_tslc = data_adsb["tslc"]							# Time since last communication in seconds
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
	data_gps_raw_int = data["GPS_RAW_INT"]["message"]				# https://mavlink.io/en/messages/common.html#GPS_RAW_INT
	telem.vel = data_gps_raw_int["vel"] / 100						# GPS ground speed cm/s
	telem.satellites = data_gps_raw_int["satellites_visible"]		# Number of satellites visible
	#
	data_gps_int = data["GLOBAL_POSITION_INT"]["message"]			# https://mavlink.io/en/messages/common.html#GLOBAL_POSITION_INT
	telem.altitude_msl = data_gps_int["alt"] / 1000					# Altitude  (MSL). Positive for up. mm
	telem.altitude = data_gps_int["relative_alt"] / 1000			# Altitude above ground
	telem.latitude = data_gps_int["lat"] / 10000000					# Latitude  (WGS84, EGM96 ellipsoid) degE7
	telem.longitude = data_gps_int["lon"] / 10000000				# Longitude (WGS84, EGM96 ellipsoid) degE7
	telem.heading = data_gps_int["hdg"]								# Vehicle heading (yaw angle), 0.0..359.99 degrees
	telem.vx = float("{:.4f}".format(data_gps_int["vx"] / 100))								# Ground X Speed (Latitude, positive north) cm/s
	telem.vy = float("{:.4f}".format(data_gps_int["vy"] / 100))								# Ground Y Speed (Longitude, positive east) cm/s
	telem.vz = float("{:.4f}".format(data_gps_int["vz"] / 100))								# Ground Z Speed (Altitude, positive down) cm/s
	#
	data_attitude = data["ATTITUDE"]["message"]						# https://mavlink.io/en/messages/common.html#ATTITUDE
	telem.pitch = float("{:.4f}".format(math.degrees(data_attitude["pitch"])))				# Pitch angle (-pi..+pi) radians
	telem.roll = float("{:.4f}".format(math.degrees(data_attitude["roll"])))				# Roll  angle (-pi..+pi) radians
	telem.yaw = float("{:.4f}".format(math.degrees(data_attitude["yaw"])))					# Yaw   angle (-pi..+pi) radians
	telem.pitch_speed = float("{:.4f}".format(data_attitude["pitchspeed"]))					# Ground X Speed (Latitude, positive north) cm/s
	telem.roll_speed = float("{:.4f}".format(data_attitude["rollspeed"]))					# Ground Y Speed (Longitude, positive east) cm/s
	telem.yaw_speed = float("{:.4f}".format(data_attitude["yawspeed"]))						# Ground Z Speed (Altitude, positive down) cm/s
	#
	data_vibration = data["VIBRATION"]["message"]					# https://mavlink.io/en/messages/common.html#VIBRATION 
	telem.vibration_x = float("{:.4f}".format(data_vibration["vibration_x"]))				# Vibration levels on X-axis
	telem.vibration_y = float("{:.4f}".format(data_vibration["vibration_y"]))				# Vibration levels on Y-axis
	telem.vibration_z = float("{:.4f}".format(data_vibration["vibration_z"]))				# Vibration levels on Z-axis
	#
	data_servo = data["SERVO_OUTPUT_RAW"]["message"]				# https://mavlink.io/en/messages/common.html#SERVO_OUTPUT_RAW
	telem.servo1 = data_servo["servo1_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.servo2 = data_servo["servo2_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.servo3 = data_servo["servo3_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.servo4 = data_servo["servo4_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.servo5 = data_servo["servo5_raw"]							# Value 900-2100 ms
	telem.servo6 = data_servo["servo6_raw"]							# Value 900-2100 ms
	telem.servo7 = data_servo["servo7_raw"]							# Value 900-2100 ms
	telem.servo8 = data_servo["servo8_raw"]							# Value 900-2100 ms
	telem.servo9 = data_servo["servo9_raw"]							# Value 900-2100 ms
	telem.servo10 = data_servo["servo10_raw"]						# Value 900-2100 ms
	telem.servo11 = data_servo["servo11_raw"]						# Value 900-2100 ms
	telem.servo12 = data_servo["servo12_raw"]						# Value 900-2100 ms
	telem.servo13 = data_servo["servo13_raw"]						# Value 900-2100 ms
	telem.servo14 = data_servo["servo14_raw"]						# Value 900-2100 ms
	telem.servo15 = data_servo["servo15_raw"]						# Value 900-2100 ms
	telem.servo16 = data_servo["servo16_raw"]						# Value 900-2100 ms
	#
	data_vfr = data["VFR_HUD"]["message"]							# https://mavlink.io/en/messages/common.html#VFR_HUD
	telem.vfr_airspeed = data_vfr["airspeed"]						# Vehicle speed in form appropriate for vehicle type.
																	# For standard aircraft this is typically calibrated airspeed (CAS)
																	# or indicated airspeed (IAS) - either of which can be used by a pilot
																	# to estimate stall speed. m/s
	telem.vfr_alt = data_vfr["alt"]									# Current altitude (MSL) m
	telem.vfr_climb = data_vfr["climb"]								# Current climb rate m/s
	telem.vfr_speed = data_vfr["groundspeed"]						# Current ground speed m/s
	telem.vfr_heading = data_vfr["heading"]							# Current heading in compass units (0-360, 0=north) Deg

	data_pressure = data["SCALED_PRESSURE"]["message"] 				# https://mavlink.io/en/messages/common.html#SCALED_PRESSURE
	telem.press_abs = float("{:.4f}".format(data_pressure["press_abs"]))	# Absolute pressure hPa
	telem.press_dif = float("{:.4f}".format(data_pressure["press_diff"]))	# Differential pressure hPa
	telem.press_tmp = data_pressure["temperature"] / 100			# Absolute pressure temperature cdegC

	# jsonTelem = json.dumps(telem.__dict__)
	# jsonTelem will be dumped in write_telemetry

	jsonTelem = (telem.__dict__)
	print(jsonTelem)
	print(url_dashboard)

	write_telemetry(jsonTelem, url_dashboard)

	# Wait for next read
	time.sleep(wait_time)
