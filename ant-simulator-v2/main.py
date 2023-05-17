import pygame as pg
# import numpy as np
import math
# import random
import sys

from constants import *
import world
import ant
import colony


def main():
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    ant.Ant.init()
    # load_images()

    clock = pg.time.Clock()
    frame_counter = 0

    food_spawns = [(pg.Vector2(WINDOW_WIDTH / 10, WINDOW_HEIGHT / 10), 500),
                   (pg.Vector2(7 * WINDOW_WIDTH / 10, 7 * WINDOW_HEIGHT / 10), 500),
                   (pg.Vector2(7 * WINDOW_WIDTH / 10, 2 * WINDOW_HEIGHT / 10), 500),
                   (pg.Vector2(3 * WINDOW_WIDTH / 10, 8 * WINDOW_HEIGHT / 10), 1000)]

    w = world.World(screen, food_spawns)

    FONT = pg.freetype.SysFont('Arial', 30)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        w.update(frame_counter)
        screen.fill('dark green')
        w.draw()

        FONT.render_to(screen, (20, 20), str(round((clock.get_fps()), 1)) + ' - ' + str(len(w.ants)), 'red')

        # draw_ph_collision_mask(screen)

        pg.display.update()

        clock.tick(FPS_LIMIT)  # limits FPS to 60
        frame_counter += 1

        # print(str(len(world.ants)) + ' - ' + str(clock.get_fps()))
        # print(str(len(world.home_phs)))


if __name__ == "__main__":
    main()
