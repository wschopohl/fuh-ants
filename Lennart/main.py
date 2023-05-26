import pygame as pg
import sys

from constants import *
import world
import ant


def main():
    '''Handles initialisation and main game loop'''
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    ant.Ant.init()
    clock = pg.time.Clock()
    w = world.World(screen)
    FONT = pg.freetype.SysFont('Arial', 30)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # dt = time passed since last frame in seconds
        dt = clock.tick(FPS_LIMIT) / 1000
        w.update(dt)
        w.draw()
        FONT.render_to(screen, (20, 20), str(round((clock.get_fps()), 1)) + ' - ' + str(len(w.ants)), 'white')
        pg.display.update()


if __name__ == "__main__":
    main()
