#!/bin/bash

echo "Install base packages..."
sudo apt-get update
sudo apt install -y screen owfs imagemagick python3-venv python3-pip sqlite3 git

echo "Create virtual environment..."
python -m venv env --system-site-packages
source env/bin/activate

echo "Install Adafruit Python Shell..."
pip3 install --upgrade adafruit-python-shell click

echo "Install Adafruit Pi Installer..."
git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd Raspberry-Pi-Installer-Scripts

echo "Setup display..."
sudo -E env PATH=$PATH python3 adafruit-pitft.py --display=35r --rotation=180 --install-type=console

echo "Setup One Wire..."
sudo mkdir /mnt/1wire

cat >> /etc/owfs.conf << EOF
  server: device = /dev/ttyUSB0

  mountpoint = /mnt/1wire
  allow_other
EOF

cat >> ~/.profile << EOF
if [ "$SSH_TTY"x == "x" ] ; then
	echo "Running on tty"
	screen -S display  bash -c "cd office-pi-display; ./show-temp"
fi
EOF

cat >> ~/.screenrc << EOF
# don't display the copyright page
startup_message off
EOF

./create-db