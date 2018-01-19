import pygame
from pygame.locals import *
import os
from time import sleep
import RPi.GPIO as GPIO

#Colours
White = (255, 255, 255)
Black = (0, 0, 0)

os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((320, 480))

lcd.fill(Black)
img = pygame.image.load('background.png')
lcd.blit(img,(0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 50)

touch_buttons = {
    'Q1':(80, 60), 'Q2':(240, 60), 'Q3':(80, 180), 'Q4':(240, 180)
}

for k, v in touch_buttons.items():
    text_surface = font_big.render('%s'%k, True, WHITE)
    rect = text_surface.get_rect(center=v)
    lcd.blit(text_surface, rect)

pygame.display.update()

while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            print pos
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            print pos

    sleep(0.1)