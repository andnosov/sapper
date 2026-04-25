import pygame, math, random, os
import pygame.freetype
from pygraph import *

square_size = 10
cell_size = 72
nmines = 10
screen_width = cell_size * square_size
screen_height = cell_size * square_size

# pygame setup
pygame.init()
pygame.display.set_caption('Игра Сапер Андрея')
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# fill the screen with a color to wipe away anything from last frame
screen.fill("white")

f = field(screen, 0, 0, screen_width, screen_height, square_size, square_size, cell_size, nmines)
f.draw("grey")

dt = 0
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            buttons = pygame.mouse.get_pressed()
            if buttons[0] == True or buttons[2] == True:
                pos = pygame.mouse.get_pos()
                print("Mouse keys pressed:", buttons, "At position:", pos)
                f.on_click(pos[0], pos[1], buttons)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
