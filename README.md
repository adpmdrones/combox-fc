# combox-fc
COMBOX with Flight Control Hardware



# raspiOS installation

1. Install raspiOS 64bit from scratch
with Raspberry Pi Imager

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get clean
```

disable login shell to be accessible over serial
and enable UART with raspi-config

2. Install OS dependencies

```bash
sudo apt-get install -yq --no-install-recommends \
  git \
  make \
  curl \
  minicom \
  raspi-gpio \
  picocom \
  screen

sudo apt install cockpit

sudo apt-get install -y pcsc-tools
```

Controllare un servocomando

```bash
msg = vehicle.message_factory.command_long_encode(
0, 0,    # target_system, target_component
mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
0, #confirmation
1,    # servo number
1500,          # servo position between 1000 and 2000
0, 0, 0, 0, 0)    # param 3 ~ 7 not used

# send command to vehicle
vehicle.send_mavlink(msg)
```
