import pygame
import os
from pygame.locals import*
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

screen = pygame.display.set_mode((320, 480))
img = pygame.image.load('display.png')
screen.blit(img,(0,0))
pygame.display.update()
