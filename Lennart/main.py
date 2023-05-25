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
    clock = pg.time.Clock()
    frame_counter = 0

    # food_spawns = [(pg.Vector2(WINDOW_WIDTH / 10, 2 * WINDOW_HEIGHT / 10), 400),
    #             #    (pg.Vector2(3 * WINDOW_WIDTH / 10, 8 * WINDOW_HEIGHT / 10), 800),
    #                (pg.Vector2(7 * WINDOW_WIDTH / 10, 7 * WINDOW_HEIGHT / 10), 300),
    #                (pg.Vector2(8 * WINDOW_WIDTH / 10, 3 * WINDOW_HEIGHT / 10), 100)]
    # w = world.World(screen, food_spawns)
    w = world.World(screen)

    FONT = pg.freetype.SysFont('Arial', 30)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # dt = clock.tick(FPS_LIMIT)  # dt = time passed since last tick (in milliseconds)
        dt = clock.tick(FPS_LIMIT) / 100     # dt = time passed since last tick (in milliseconds)
        # print(dt)

        w.update(frame_counter, dt)
        w.draw()
        FONT.render_to(screen, (20, 20), str(round((clock.get_fps()), 1)) + ' - ' + str(len(w.ants)), 'white')

        pg.display.update()
        frame_counter += 1


if __name__ == "__main__":
    main()
