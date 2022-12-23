#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import logging
import json

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

while True:
	try:
		# Request Mavlink data from UAV
		r = requests.get(url_uav , timeout=2)
		data = r.json()
		break
	except KeyboardInterrupt:
		break
	except:
		print("Error reading mavlink data.")
		print("Retrying...")
		logger.error("Error reading mavlink data.")
		time.sleep(5.0)
		pass

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
	quit()

if (mavtype in mavtype_wing):	
	print(mavtype)
elif (mavtype in mavtype_multirotor):
	print(mavtype)
else:
	print("mavtype not supported. Exiting.")
	logger.error("mavtype not supported")
	quit()


while True:
	time.sleep(wait_time)
	try:
		print(f"Start local request to {url_uav}")
		r = requests.get(url_uav , timeout=2)
		data = r.json()

		# Extract data groups form mavlink
		#
		data_adsb = data["ADSB_VEHICLE"]["message"]
		data_gps_raw_int = data["GPS_RAW_INT"]["message"]			# https://mavlink.io/en/messages/common.html#GPS_RAW_INT
		data_gps_int = data["GLOBAL_POSITION_INT"]["message"]		# https://mavlink.io/en/messages/common.html#GLOBAL_POSITION_INT
		data_attitude = data["ATTITUDE"]["message"]					# https://mavlink.io/en/messages/common.html#ATTITUDE
		data_vibration = data["VIBRATION"]["message"]				# https://mavlink.io/en/messages/common.html#VIBRATION
		#data_wind = data["WIND"]["message"]						# 
		data_servo = data["SERVO_OUTPUT_RAW"]["message"]			#
		data_vfr = data["VFR_HUD"]["message"]						# https://mavlink.io/en/messages/common.html#VFR_HUD
		data_pressure = data["SCALED_PRESSURE"]["message"] 		#

		# Assign data
		#
		TIS = data["ATTITUDE"]["status"]["time"]["last_update"]	# Timestamp
		#
		ALT_MSL = data_gps_int["alt"]								# Altitude  (MSL). Positive for up. mm
		ALT_REL = data_gps_int["relative_alt"]						# Altitude above ground
		LAT = data_gps_int["lat"]									# Latitude  (WGS84, EGM96 ellipsoid) degE7
		LON = data_gps_int["lon"]									# Longitude (WGS84, EGM96 ellipsoid) degE7
		HDG = data_gps_int["hdg"]									# Vehicle heading (yaw angle), 0.0..359.99 degrees
		GSPD_X = data_gps_int["vx"]									# Ground X Speed (Latitude, positive north) cm/s
		GSPD_Y = data_gps_int["vy"]									# Ground Y Speed (Longitude, positive east) cm/s
		GSPD_Z = data_gps_int["vz"]									# Ground Z Speed (Altitude, positive down) cm/s
		#
		VEL = data_gps_raw_int["vel"]								# GPS ground speed cm/s
		SAT = data_gps_raw_int["satellites_visible"]				# Number of satellites visible
		#
		PIT = data_attitude["pitch"]								# Pitch angle (-pi..+pi) radians
		RLL = data_attitude["roll"]									# Roll  angle (-pi..+pi) radians
		YAW = data_attitude["yaw"]									# Yaw   angle (-pi..+pi) radians
		SPD_P = data_attitude["pitchspeed"]									# Ground X Speed (Latitude, positive north) cm/s
		SPD_R = data_attitude["rollspeed"]									# Ground Y Speed (Longitude, positive east) cm/s
		SPD_Y = data_attitude["yawspeed"]									# Ground Z Speed (Altitude, positive down) cm/s
		#
		VIX = data_vibration["vibration_x"]							# Vibration levels on X-axis
		VIY = data_vibration["vibration_y"]							# Vibration levels on Y-axis
		VIZ = data_vibration["vibration_z"]							# Vibration levels on Z-axis
		#
		#WDIR = data_wind["direction"]								#
		#WSPD = data_wind["speed"]									#
		#WSPDZ = data_wind["speed_z"]								#
		WDIR = 10													#
		WSPD = 10													#
		WSPDZ = 10													#
		#
		VFR_ARSPD = data_vfr["airspeed"]										#
		VFR_ALT = data_vfr["alt"]									#
		VFR_CLIMB = data_vfr["climb"]								#
		VFR_GSPD = data_vfr["groundspeed"]							#
		VFR_HDG = data_vfr["heading"]								#
		#
		SRV01 = data_servo["servo1_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
		SRV02 = data_servo["servo2_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
		SRV03 = data_servo["servo3_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
		SRV04 = data_servo["servo4_raw"]							# Value 900-2100 ms (DO NOT USE- ASSIGNED TO FC controls)
		SRV05 = data_servo["servo5_raw"]							# Value 900-2100 ms
		SRV06 = data_servo["servo6_raw"]							# Value 900-2100 ms
		SRV07 = data_servo["servo7_raw"]							# Value 900-2100 ms
		SRV08 = data_servo["servo8_raw"]							# Value 900-2100 ms
		SRV09 = data_servo["servo9_raw"]							# Value 900-2100 ms
		SRV10 = data_servo["servo10_raw"]							# Value 900-2100 ms
		SRV11 = data_servo["servo11_raw"]							# Value 900-2100 ms
		SRV12 = data_servo["servo12_raw"]							# Value 900-2100 ms
		SRV13 = data_servo["servo13_raw"]							# Value 900-2100 ms
		SRV14 = data_servo["servo14_raw"]							# Value 900-2100 ms
		SRV15 = data_servo["servo15_raw"]							# Value 900-2100 ms
		SRV16 = data_servo["servo16_raw"]							# Value 900-2100 ms
		#
		PRS_ABS = data_pressure["press_abs"]						#
		PRS_DIF = data_pressure["press_diff"]						#
		PRS_TMP = data_pressure["temperature"]						#
		#
		ADSB_LAT = data_adsb["lat"]
		ADSB_LON = data_adsb["lon"]	
		ADSB_HDG = data_adsb["heading"]	
		ADSB_HSP = data_adsb["hor_velocity"]
		ADSB_VSP = data_adsb["ver_velocity"]
		ADSB_SQW = data_adsb["squawk"]
		ADSB_TYP = data_adsb["type"]
		ADSB_TSL = data_adsb["tslc"]

		data = '{' + \
			'\"droneid\":' + str(droneID) + \
			',\"timestamp\":\"' + TIS + '\"' + \
			',\"latitude\":' + str(LAT / 10000000) + \
			',\"longitude\":' + str(LON / 10000000) + \
			',\"altitude\":' + str(VFR_ALT) + \
			',\"altitude_msl\":' + str(ALT_MSL) + \
			',\"speed\":' + str(VFR_GSPD) + \
			',\"airspeed\":' + str(VFR_ARSPD) + \
			',\"climb\":' + str(VFR_CLIMB) + \
			',\"satellites\":' + str(SAT) + \
			',\"pitch\":' + str(PIT) + \
			',\"roll\":' + str(RLL) + \
			',\"yaw\":' + str(YAW) + \
			',\"heading\":' + str(VFR_HDG) + \
			',\"vibration_x\":' +str(VIX) + \
			',\"vibration_y\":' +str(VIY) + \
			',\"vibration_z\":' +str(VIZ) + \
			',\"pitch_speed\":' +str(SPD_P) + \
			',\"roll_speed\":' +str(SPD_R) + \
			',\"yaw_speed\":' +str(SPD_Y) + \
			',\"wind_speed\":' + str(WSPD) + \
			',\"wind_dir\":' + str(WDIR) + \
			',\"wind_speed_z\":' + str(WSPDZ) + \
			',\"press_abs\":' + str(PRS_ABS) + \
			',\"press_dif\":' + str(PRS_DIF) + \
			',\"press_tmp\":' + str(PRS_TMP) + \
			',\"servo1\":' + str(SRV01) + \
			',\"servo2\":' + str(SRV02) + \
			',\"servo3\":' + str(SRV03) + \
			',\"servo4\":' + str(SRV04) + \
			',\"servo5\":' + str(SRV05) + \
			',\"servo6\":' + str(SRV06) + \
			',\"servo7\":' + str(SRV07) + \
			',\"servo8\":' + str(SRV08) + \
			',\"servo9\":' + str(SRV09) + \
			',\"servo10\":' + str(SRV10) + \
			',\"servo11\":' + str(SRV11) + \
			',\"servo12\":' + str(SRV12) + \
			',\"servo13\":' + str(SRV13) + \
			',\"servo14\":' + str(SRV14) + \
			',\"servo15\":' + str(SRV15) + \
			',\"servo16\":' + str(SRV16) + \
			',\"adsb_lat\":' + str(ADSB_LAT) + \
			',\"adsb_lon\":' + str(ADSB_LON) + \
			',\"adsb_lheading\":' + str(ADSB_HDG) + \
			',\"adsb_hor_velocity\":' + str(ADSB_HSP) + \
			',\"adsb_ver_velocity\":' + str(ADSB_VSP) + \
			',\"adsb_squawk\":' + str(ADSB_SQW) + \
			',\"adsb_tslc\":' + str(ADSB_TSL) + \
			'}'
		print("HERE4")
		print(data)
		data = json.loads(data)
		logger.info(data)
		print(data)

		r = requests.post(url_dashboard, timeout=2, json=data)
		#logger.info(r.status_code)
		print(r.status_code)

	except KeyboardInterrupt:
		break
	except:
		logger.error("POST Issue")
		pass
