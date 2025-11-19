
Adafruit RGB Matrix + for hub75 panel.

https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi

## With "cheap" board
 ./demo -D 7 --led-rows=32 --led-cols=64 --led-panel-type=FM6127 --led-no-hardware-pulse --led-slowdown-gpio=4 -m 500 --led-brightness=10

## With Adafruit Hat
 sudo ./demo -D 10 --led-rows=32 --led-cols=64 --led-panel-type=FM6127 --led-no-hardware-pulse --led-slowdown-gpio=4 -m 500 --led-brightness=64 --led-gpio-mapping=adafruit-hat