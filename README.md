# office-pi-display

Python2 script to generate 320x480 display for Raspberry Pi in my office.

This script reads data from a connected OneWire temperature sensor and displays its value (in F) on the PiTFT screen.

![Sample generated image](display.png)

[background.jpg](http://adafruit-download.s3.amazonaws.com/adapiluv320x240.jpg) is copied and modifiled from [Adafruit PiTFT 3.5" Touch Screen for Raspberry Pi](https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/displaying-images).

## To run
```
# Install Python packages
pip install -r requirements.txt
# Run script and generate image (display.png)
python display.py
```
