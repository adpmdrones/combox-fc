#!/bin/env bash
# Modified on July 31, 2022 by ADPM Drones (adpmdrones)
#
# master, out  connections
#
#####################
# - MAV_MASTER ($1 parametro passato da MAVGATEWAY_OPTS)
#  Connessione alla Flight Control
#  /dev/ttyACM2 -> USB
#  /dev/ttyAMA0 -> UART
#
# - MAV_LOCAL ($2 parametro passato da MAVGATEWAY_OPTS)
#  EndPoint locale per script Dronekit locale
#
# - MAV_GCS ($3 parametro passato da MAVGATEWAY_OPTS)
#  EndPoint GCS di controllo ADPM/T-DROMES
#
#####################
#MAV_MASTER=serial:/dev/TTYMAVLINK:115200
#MAV_LOCAL=udpc:localhost:14550
#MAV_GCS=udpc:100.96.1.2:14550
#
cd /home/pi/combox-fc/mavlink
/home/pi/combox-fc/mavlink/mav2rest.sh $1 $2 $3