# office-pi-display

NodeJS Script to generate 320x480 display for Raspberry Pi in my office

![Sample generated image](display.png)

[background.jpg](http://adafruit-download.s3.amazonaws.com/adapiluv320x240.jpg) is copied and modifiled from [Adafruit PiTFT 3.5" Touch Screen for Raspberry Pi](https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/displaying-images).

## To run
```
# Install NodeJS packages
npm install
# Run script and generate image (display.png)
npm start
# Display on screen
sudo fbi -T 2 -d /dev/fb1 -noverbose -a display.png 2>/dev/null
```
