#!/bin/bash

# Prepare background image
#convert adapiluv320x240.jpg -resize 320x480 \
#		-gravity center -background black -extent 320x480 \
#		background.png

kill $(pgrep fbi)
while /bin/true
do
	ip_addr=$(ifconfig wlan0 | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p')
	now=$(date +%-I:%M:%S)
	today=$(date "+%a, %b %-d")
	temp_c=$(/opt/vc/bin/vcgencmd measure_temp|sed -En 's/temp=([0-9]*\.[0-9]*).*/\1/p')
	temp_f=$(echo "$temp_c * 1.8 + 32" | bc)

	convert -size 320x480 background.png \
        	-font Roboto-Regular -fill yellow -pointsize 64  -gravity north  -draw "text 0,0 '$now'" \
        	-font Roboto-Regular -fill yellow -pointsize 48  -gravity north  -draw "text 0,75 '$today'" \
        	-font Roboto-Bold    -fill white -pointsize 120 -gravity center -draw "text 0,125 '$temp_f'" \
        	-font Roboto-Regular -fill skyblue   -pointsize 24  -gravity south  -draw "text 0,0 '$ip_addr'" \
        	display320x480.jpg

	fbi -T 2 -d /dev/fb1 -noverbose -a display320x480.jpg 2> /dev/null

	sleep 0.75
	kill $(pgrep fbi)
done

