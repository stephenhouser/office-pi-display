#!/usr/bin/env python
# coding: utf-8

#https://web.archive.org/web/20151027165018/http://jeremyblythe.blogspot.com/2014/09/raspberry-pi-pygame-ui-basics.html
import os
import pygame
import socket
from pygame.locals import *
from time import sleep
from datetime import datetime
from onewire import Onewire
from threading import Thread
import paho.mqtt.client as mqtt

#import RPi.GPIO as GPIO

ow_device_temp = "26.103D15000000"
ow_device = "localhost:4304"
ow_read_period = 10 # seconds

mqtt_server = "paris"
mqtt_port = 1883
mqtt_topic = "living-room/status/temperature"

current_temperature = None

font_preferences = ["roboto", "droidsans", "sans"]
FONT_XLARGE = 132
FONT_LARGE = 68
FONT_NORMAL = 36
FONT_SMALL = 24

White = (255, 255, 255)
Black = (0, 0, 0)
SkyBlue = (135, 206, 235)
Yellow = (255, 255, 0)

def main():
    initialize_sensors()
    #initialize_mqtt()
    initialize_display()

    clock = pygame.time.Clock()
    while True:
        # Check for Events
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                print pos
            elif(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                print pos

        # Update Display
        draw_background()
        if current_temperature != None:
            draw_string('{0:0.1f}'.format(current_temperature), (160, 340), FONT_XLARGE, White)
            draw_string(u'°F', (300, 320), FONT_SMALL, White)

        if local_ip != None:
            draw_string("{}".format(local_ip()), (160, 470), FONT_SMALL, SkyBlue)

        draw_string(date_string(), (160, FONT_NORMAL), FONT_NORMAL, Yellow)
        draw_string(time_string(), (160, FONT_NORMAL*2.5), FONT_LARGE, Yellow)

        pygame.display.flip()
        #pygame.display.update()
        sleep(0.1)

    pygame.quit()

def initialize_display():
    global display
    os.putenv('SDL_FBDEV', '/dev/fb1')
    #os.putenv('SDL_MOUSEDRV', 'TSLIB')
    #os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

    pygame.init()
    pygame.mouse.set_visible(False)
    display = pygame.display.set_mode((320, 480))

def initialize_mqtt():
    global mqttc
    mqttc = mqtt.Client()
    mqttc.on_message = on_mqtt_message

    mqttc.connect(mqtt_server, mqtt_port, 60)
    mqttc.subscribe(mqtt_topic, qos=0)

    mqttc.loop_start()

def initialize_sensors():
    ow_thread = Thread(target = read_onewire)
    ow_thread.daemon = True
    ow_thread.start()

def read_onewire():
    global current_temperature
    with Onewire(ow_device) as ow:
        while True:
            current_temperature = ow.sensor(ow_device_temp).temperature
            current_temperature = float(current_temperature) * 1.8 + 32
            sleep(ow_read_period)
	
def on_mqtt_message(client, userdata, message):
    global current_temperature
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    current_temperature = float(message.payload) * 1.8 + 32

def time_string():
    now = datetime.now()
    return now.strftime("%-I:%M:%S")

def date_string():
    now = datetime.now()
    return now.strftime("%a, %b %d, %Y")

def draw_background():
    display.fill(Black)
    img = pygame.image.load('background.png')
    display.blit(img,(0,0))

def draw_string(text, centerPoint, font_size, color):
    #if font_size == FONT_LARGE:
    #    font = pygame.font.Font("droid-sans-mono/DroidSansMono.ttf", font_size)
    #else:
    font = get_font(font_preferences, font_size)

    text_image = font.render(text, True, color)
    rect = text_image.get_rect(center=centerPoint)
    display.blit(text_image, rect)

def local_ip():
    return socket.gethostbyname(socket.gethostname())

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names 
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size, bold=True)
    return pygame.font.Font(None, size)

_cached_fonts = {}
def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

if __name__ == "__main__":
    main()
