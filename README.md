# office-pi-display

Script to display time and temperature on [Adafruit 3.5" Display](https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi) connected to a Raspberry Pi 3B and OneWire Temperature sensor in my office.

![Sample generated image](display.png)

## Operation

The script reads the temperature from a OneWire sensor (via `owfs`), uses ImageMagick to place text (time, date, temperature, and ip address) over a background image. ImageMagick can also create the image in a BMP3 format that is the same as the framebuffer, so we just dump that right to the framebuffer device (after a little magic)

Launch the script `show-temp` on startup or login of the default user. (to be written).

## Components

* [Adafruit 3.5" Display](https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi); 320x480 screen.
* OneWire Temperature Sensor
* OneWire Serial Bus Hub (via USB Serial)

## Configuration

* Follow Adafruit's [Easy Install](https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/easy-install-2) for the display with 90-degree rotation.
* Configure Raspberry Pi with `raspi-config` **NOTE: Don't enable 1Wire**
* Install `owfs` and `imagemagick`
* Clone this repo and tweak any parameters needed in `show-temp`
* Run!

[background.jpg](http://adafruit-download.s3.amazonaws.com/adapiluv320x240.jpg) is copied and modifiled from [Adafruit PiTFT 3.5" Touch Screen for Raspberry Pi](https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/displaying-images).


The screen/framebuffer is:

```

mode "320x480"
    geometry 320 480 320 480 32
    timings 0 0 0 0 0 0 0
    rgba 8/16,8/8,8/0,0/0
endmode

Frame buffer device information:
    Name        : hx8357ddrmfb
    Address     : 0
    Size        : 614400
    Type        : PACKED PIXELS
    Visual      : TRUECOLOR
    XPanStep    : 1
    YPanStep    : 1
    YWrapStep   : 0
    LineLength  : 1280
    Accelerator : No
```

This [stack overflow article](https://raspberrypi.stackexchange.com/questions/125125/how-can-i-write-an-image-to-the-rpi4-framebuffer-in-raspbian-lite) had the clues to use ImageMagick directly and to trim the headers off the generated BMP file and write directly to the framebuffer.

Specifically

```bash
convert background.png -flip -alpha set -define bmp:format=bmp3 -define bmp3:alpha=true bmp3:- | tail -c 614400 > /dev/fb1
```
