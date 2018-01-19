import os
import pygame
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
lcd = pygame.display.set_mode((320, 240))
lcd.fill(Black)
pygame.display.update()

font_big = pygame.font.Font(None, 100)

touch_buttons = {'17 on':(80,60), '4 on':(240,60), '17 off':(80,180), '4 off':(240,180)}

for k,v in touch_buttons.items():
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
            #Find which quarter of the screen we're in
            x,y = pos
            if y < 120:
                if x < 160:
                    GPIO.output(17, False)
                else:
                    GPIO.output(4, False)
            else:
                if x < 160:
                    GPIO.output(17, True)
                else:
                    GPIO.output(4, True)
    sleep(0.1)