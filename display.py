#!/usr/bin/env python
# coding: utf-8

#https://web.archive.org/web/20151027165018/http://jeremyblythe.blogspot.com/2014/09/raspberry-pi-pygame-ui-basics.html
import os
import socket
import sqlite3
import logging
from time import sleep
from datetime import datetime
from threading import Thread
import pyownet
import pygame
from pygame.locals import *

ow_server = "localhost"
ow_port = 4304
ow_sensor = "26.103D15000000"
ow_read_period = 30 # seconds

current_temperature = None
current_humidity = None

logging.basicConfig(filename='office-pi.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(message)s')
logging.info('Startup...')

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
    initialize_display()

    clock = pygame.time.Clock()
    while True:
        # Check for Events
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                print(pos)
            elif(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                print(pos)

        # Update Display
        draw_background()
        if current_temperature != None:
            draw_string('{0:0.1f}'.format(c2f(current_temperature)), (160, 340), FONT_XLARGE, White)
            draw_string(u'°F', (300, 320), FONT_SMALL, White)

        draw_string(date_string(), (160, FONT_NORMAL), FONT_NORMAL, Yellow)
        draw_string(time_string(), (160, FONT_NORMAL*2.5), FONT_LARGE, Yellow)

        pygame.display.flip()
        #pygame.display.update()
        sleep(0.5)

    pygame.quit()

def initialize_display():
    global display
    os.putenv('SDL_FBDEV', '/dev/fb1')
    #os.putenv('SDL_MOUSEDRV', 'TSLIB')
    #os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

    pygame.init()
    pygame.mouse.set_visible(False)
    display = pygame.display.set_mode((320, 480))

def initialize_sensors():
    ow_thread = Thread(target = read_onewire)
    ow_thread.daemon = True
    ow_thread.start()

def read_onewire():
    global current_temperature, current_humidity

    logdb = sqlite3.connect("office-pi.db")

    ow_proxy = pyownet.protocol.proxy(host=ow_server, port=ow_port)
    #owproxy.dir() -> [u'/28.000028D70000/', u'/26.000026D90100/']
    ow_t = "/" + ow_sensor + "/temperature"
    ow_h = "/" + ow_sensor + "/humidity"
    while True:
        current_temperature = float(ow_proxy.read(ow_t))
        current_humidity = float(ow_proxy.read(ow_h))

        print("/{}/temperature => {}".format(ow_sensor, current_temperature))
        print("/{}/humidity => {}".format(ow_sensor, current_humidity))

        logging.info("temperature={}c/{}f".format(current_temperature, c2f(current_temperature)))
        logging.info("humidity={}".format(current_humidity))

        now = datetime.now()
        temp_data = [now, current_temperature, 'C']
        logdb.execute('insert into temperature values(?, ?, ?)', temp_data)
        humi_data = [now, current_humidity, '%']
        logdb.execute('insert into humidity values(?, ?, ?)', humi_data)
        logdb.commit()

        sleep(ow_read_period)
	
def time_string():
    now = datetime.now()
    return now.strftime("%-I:%M:%S")

def date_string():
    now = datetime.now()
    return now.strftime("%a, %b %d, %Y")

background_image = None
def draw_background():
    global background_image

    if background_image == None: # only load at start
        background_image = pygame.image.load('background.png')

    #display.fill(Black)
    display.blit(background_image,(0,0))

def draw_string(text, centerPoint, font_size, color):
    font = get_font(font_preferences, font_size)
    text_image = font.render(text, True, color)
    rect = text_image.get_rect(center=centerPoint)
    display.blit(text_image, rect)

def local_ip():
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if not ip.startswith("127."):
            return ip

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 53))
    ip = s.getsockname()[0]
    s.close()
    return ip

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

def c2f(c):
    return c * 1.8 + 32 # convert to F for display

if __name__ == "__main__":
    main()
