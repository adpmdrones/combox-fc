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