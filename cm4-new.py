#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import logging
import json
import os

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
wait_time = 0.25

# Endpoints
#
# Mavlink2rest
url_uav = f"http://localhost:8088/mavlink/vehicles/{droneID}/components/1/messages"
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
	UAV = 1				# DroneID
	TIS = ''			# timestamp
	#
	ALT_MSL = 0.0		# Altitude  (MSL). Positive for up. mm
	ALT_REL = 0.0		# Altitude above ground
	LAT = 0.0			# Latitude  (WGS84, EGM96 ellipsoid) degE7
	LON = 0.0			# Longitude (WGS84, EGM96 ellipsoid) degE7
	HDG = 0.0			# Vehicle heading (yaw angle), 0.0..359.99 degrees
	GSPD_X = 0.0		# Ground X Speed (Latitude, positive north) cm/s
	GSPD_Y = 0.0		# Ground Y Speed (Longitude, positive east) cm/s
	GSPD_Z = 0.0		# Ground Z Speed (Altitude, positive down) cm/s
	#
	VEL = 0.0			# GPS ground speed cm/s
	SAT = 0				# Number of satellites visible
	#
	PIT = 0.0			# Pitch angle (-pi..+pi) radians
	RLL = 0.0			# Roll  angle (-pi..+pi) radians
	YAW = 0.0			# Yaw   angle (-pi..+pi) radians
	SPD_P = 0.0			# Ground X Speed (Latitude, positive north) cm/s
	SPD_R = 0.0			# Ground Y Speed (Longitude, positive east) cm/s
	SPD_Y = 0.0			# Ground Z Speed (Altitude, positive down) cm/s
	#
	VIX = 0.0			# Vibration levels on X-axis
	VIY = 0.0			# Vibration levels on Y-axis
	VIZ = 0.0			# Vibration levels on Z-axis
	#
	WDIR = 0.0			#
	WSPD = 0.0			#
	WSPDZ = 0.0			#
	#
	VFR_ARSPD = 0.0		#
	VFR_ALT = 0.0		#
	VFR_CLIMB = 0.0		#
	VFR_GSPD = 0.0		#
	VFR_HDG = 0.0		#
	#
	SRV01 = 0			# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	SRV02 = 0			# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	SRV03 = 0			# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	SRV04 = 0			# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	SRV05 = 0			# Value 900-2100 ms
	SRV06 = 0			# Value 900-2100 ms
	SRV07 = 0			# Value 900-2100 ms
	SRV08 = 0			# Value 900-2100 ms
	SRV09 = 0			# Value 900-2100 ms
	SRV10 = 0			# Value 900-2100 ms
	SRV11 = 0			# Value 900-2100 ms
	SRV12 = 0			# Value 900-2100 ms
	SRV13 = 0			# Value 900-2100 ms
	SRV14 = 0			# Value 900-2100 ms
	SRV15 = 0			# Value 900-2100 ms
	SRV16 = 0			# Value 900-2100 ms
	#
	PRS_ABS = 0			# Value 900-2100 ms
	PRS_DIF = 0			# Value 900-2100 ms
	PRS_TMP = 0			# Value 900-2100 ms
	#
	ADSB_LAT = 0.0
	ADSB_LON = 0.0
	ADSB_HDG = 0.0
	ADSB_HSP = 0.0
	ADSB_VSP = 0.0
	ADSB_SQW = 0.0
	ADSB_TYP = 0.0
	ADSB_TSL = 0.0

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

	telem.TIS = data["ATTITUDE"]["status"]["time"]["last_update"]
	telem.UAV = droneID

	# Check if ADSB data is available
	if "ADSB_VEHICLE" in data:
		# Read ADSB data
		data_adsb = data["ADSB_VEHICLE"]["message"]					# https://mavlink.io/en/messages/common.html#ADSB_VEHICLE
		# Update 
		telem.ADSB_LAT = data_adsb["lat"] / 10000000
		telem.ADSB_LON = data_adsb["lon"] / 10000000
		telem.ADSB_HDG = data_adsb["heading"]
		telem.ADSB_HSP = data_adsb["hor_velocity"]
		telem.ADSB_VSP = data_adsb["ver_velocity"]
		telem.ADSB_SQW = data_adsb["squawk"]
		telem.ADSB_TYP = data_adsb["type"]
		telem.ADSB_TSL = data_adsb["tslc"]
	#
	# Check if WIND data is available
	if "WIND" in data:
		# Read wind data
		data_wind = data["WIND"]["message"]	
		# Update
		telem.WDIR = data_wind["direction"]
		telem.WSPD = data_wind["speed"]
		telem.WSPDZ = data_wind["speed_z"]
	#
	data_gps_raw_int = data["GPS_RAW_INT"]["message"]				# https://mavlink.io/en/messages/common.html#GPS_RAW_INT
	telem.VEL = data_gps_raw_int["vel"]								# GPS ground speed cm/s
	telem.SAT = data_gps_raw_int["satellites_visible"]				# Number of satellites visible
	#
	data_gps_int = data["GLOBAL_POSITION_INT"]["message"]			# https://mavlink.io/en/messages/common.html#GLOBAL_POSITION_INT
	telem.ALT_MSL = data_gps_int["alt"]								# Altitude  (MSL). Positive for up. mm
	telem.ALT_REL = data_gps_int["relative_alt"]					# Altitude above ground
	telem.LAT = data_gps_int["lat"] / 10000000						# Latitude  (WGS84, EGM96 ellipsoid) degE7
	telem.LON = data_gps_int["lon"]	/ 10000000						# Longitude (WGS84, EGM96 ellipsoid) degE7
	telem.HDG = data_gps_int["hdg"]									# Vehicle heading (yaw angle), 0.0..359.99 degrees
	telem.GSPD_X = data_gps_int["vx"]								# Ground X Speed (Latitude, positive north) cm/s
	telem.GSPD_Y = data_gps_int["vy"]								# Ground Y Speed (Longitude, positive east) cm/s
	telem.GSPD_Z = data_gps_int["vz"]								# Ground Z Speed (Altitude, positive down) cm/s
	#
	data_attitude = data["ATTITUDE"]["message"]						# https://mavlink.io/en/messages/common.html#ATTITUDE
	telem.PIT = data_attitude["pitch"]								# Pitch angle (-pi..+pi) radians
	telem.RLL = data_attitude["roll"]								# Roll  angle (-pi..+pi) radians
	telem.YAW = data_attitude["yaw"]								# Yaw   angle (-pi..+pi) radians
	telem.SPD_P = data_attitude["pitchspeed"]						# Ground X Speed (Latitude, positive north) cm/s
	telem.SPD_R = data_attitude["rollspeed"]						# Ground Y Speed (Longitude, positive east) cm/s
	telem.SPD_Y = data_attitude["yawspeed"]							# Ground Z Speed (Altitude, positive down) cm/s
	#
	data_vibration = data["VIBRATION"]["message"]					# https://mavlink.io/en/messages/common.html#VIBRATION 
	telem.VIX = data_vibration["vibration_x"]						# Vibration levels on X-axis
	telem.VIY = data_vibration["vibration_y"]						# Vibration levels on Y-axis
	telem.VIZ = data_vibration["vibration_z"]						# Vibration levels on Z-axis
	#
	data_servo = data["SERVO_OUTPUT_RAW"]["message"]				# https://mavlink.io/en/messages/common.html#SERVO_OUTPUT_RAW
	telem.SRV01 = data_servo["servo1_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.SRV02 = data_servo["servo2_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.SRV03 = data_servo["servo3_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.SRV04 = data_servo["servo4_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
	telem.SRV05 = data_servo["servo5_raw"]							# Value 900-2100 ms
	telem.SRV06 = data_servo["servo6_raw"]							# Value 900-2100 ms
	telem.SRV07 = data_servo["servo7_raw"]							# Value 900-2100 ms
	telem.SRV08 = data_servo["servo8_raw"]							# Value 900-2100 ms
	telem.SRV09 = data_servo["servo9_raw"]							# Value 900-2100 ms
	telem.SRV10 = data_servo["servo10_raw"]							# Value 900-2100 ms
	telem.SRV11 = data_servo["servo11_raw"]							# Value 900-2100 ms
	telem.SRV12 = data_servo["servo12_raw"]							# Value 900-2100 ms
	telem.SRV13 = data_servo["servo13_raw"]							# Value 900-2100 ms
	telem.SRV14 = data_servo["servo14_raw"]							# Value 900-2100 ms
	telem.SRV15 = data_servo["servo15_raw"]							# Value 900-2100 ms
	telem.SRV16 = data_servo["servo16_raw"]							# Value 900-2100 ms
	#
	data_vfr = data["VFR_HUD"]["message"]							# https://mavlink.io/en/messages/common.html#VFR_HUD
	telem.VFR_ARSPD = data_vfr["airspeed"]							#
	telem.VFR_ALT = data_vfr["alt"]									#
	telem.VFR_CLIMB = data_vfr["climb"]								#
	telem.VFR_GSPD = data_vfr["groundspeed"]						#
	telem.VFR_HDG = data_vfr["heading"]								#

	data_pressure = data["SCALED_PRESSURE"]["message"] 				# https://mavlink.io/en/messages/common.html#SCALED_PRESSURE
	telem.PRS_ABS = data_pressure["press_abs"]						#
	telem.PRS_DIF = data_pressure["press_diff"]						#
	telem.PRS_TMP = data_pressure["temperature"]					#

	jsonTelem = json.dumps(telem.__dict__)
	write_telemetry(jsonTelem, url_dashboard)
	time.sleep(wait_time)
