import pygame as pg
import numpy as np
import math
import random
import sys

from constants import *
from world import World
import ant
import colony
import pheromone


def main():

    # pygame setup
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    clock = pg.time.Clock()
    frame_counter = 0

    # all_ants = pg.sprite.Group()
    # food_group = pg.sprite.Group()
    # home_pheromones = pg.sprite.Group()
    # food_pheromones = pg.sprite.Group()

    food_spawns = [(pg.math.Vector2(WINDOW_WIDTH / 10, WINDOW_HEIGHT / 10), 500),
                   (pg.math.Vector2(7 * WINDOW_WIDTH / 10, 7 * WINDOW_HEIGHT / 10), 200)]

    world = World(screen, food_spawns)

    FONT = pg.freetype.SysFont('Arial', 30)

    
    while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # fill the screen with a color to wipe away anything from last frame
        # screen.fill('dark green')

        # RENDER YOUR GAME HERE
        world.update(frame_counter)
        world.draw()

        # for ant in all_ants.sprites():
        #     print(ant.pos, ant.angle)
        # print('======================================')

        FONT.render_to(screen, (20, 20), str(round((clock.get_fps()), 1)) + ' - ' + str(len(world.ants)), 'red')

        # flip() the display to put your work on screen
        # pg.display.flip()
        pg.display.update()

        clock.tick(FPS_LIMIT)  # limits FPS to 60
        frame_counter += 1

        # print(str(len(world.ants)) + ' - ' + str(clock.get_fps()))
        # print(str(len(world.home_pheromones)))


if __name__ == "__main__":
    main()
    # pg.quit()
