import pygame
from pygame.locals import *
import sys, os
import time

pygame.init()

mouse = pygame.mouse
fpsClock = pygame.time.Clock()

width = 320
height = 240

window = pygame.display.set_mode((width, height))
canvas = window.copy()
#                     R    G    B
BLACK = pygame.Color( 0 ,  0 ,  0 )
WHITE = pygame.Color(255, 255, 255)

pygame.display.update()

window.fill(WHITE)

pygame.draw.circle(window, BLACK, (pygame.mouse.get_pos()), 5)

left_pressed, middle_pressed, right_pressed = mouse.get_pressed()

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif left_pressed:
        pygame.draw.circle(canvas, BLACK, (pygame.mouse.get_pos()),5)



window.blit(canvas, (0, 0))

canvas.fill(WHITE)

pygame.display.set_caption('Paintme')