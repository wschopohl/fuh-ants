from constants import *
import world
from pathlib import Path
# import antsprite
import pygame
import colour

PIXELSIZE = 4
FPS = 10
WIN_TITLE = "Ant Simulator"
MAX_PHEROMONE_COLORS = 10


def colorstr2rgb(colorstr):
    color = colour.Color(colorstr)
    return (int(color.red*255), int(color.green*255), int(color.blue*255))


def color2rgb(color):
    return (int(color.red*255), int(color.green*255), int(color.blue*255))


YELLOW = colorstr2rgb("yellow")
GOLD = colorstr2rgb("gold")
BLUE = colorstr2rgb("blue")
GREEN = colorstr2rgb("limegreen")
RED = colorstr2rgb("red")
MAGENTA = colorstr2rgb("magenta")
WHITE = colorstr2rgb("white")
BLACK = colorstr2rgb("black")
GRAY = colorstr2rgb("gray")

COLOR1 = colour.Color("yellow")
COLOR2 = colour.Color("gold")
COLORS = list(COLOR1.range_to(COLOR2, MAX_PHEROMONE_COLORS))
RGBS = [color2rgb(c) for c in COLORS]


### class GraphicView ###


class GraphicView:

    # initialize PyGame graphic view
    def __init__(self, world):
        self.__world = world
        self.__winwidth = world.width() * PIXELSIZE
        self.__winheight = world.height() * PIXELSIZE
        self.__win = pygame.display.set_mode(
            (self.__winwidth, self.__winheight))
        # pygame.display.set_icon(self.ant_sprite)
        pygame.display.set_caption(WIN_TITLE)
        # self.font = pygame.font.SysFont('Consolas', 20)

    def getPheromoneColor(self, pos):
        level = self.__world.getPheromone(pos)  # in range(0,MAX_PHEROMONE)
        colorlevel = int(level * MAX_PHEROMONE_COLORS / MAX_PHEROMONE)
        if(colorlevel <= 0):
            color = WHITE
        elif(colorlevel >= MAX_PHEROMONE_COLORS):
            color = GOLD
        else:
            color = RGBS[colorlevel]
            # color = YELLOW
        return color

    # render world
    def renderWorld(self):
        self.__win.fill(WHITE)
        # draw block, food and pheromone
        for y in range(self.__world.height()):
            for x in range(self.__world.width()):
                if(self.__world.getFood((x, y)) > 0):
                    pygame.draw.rect(self.__win, GREEN, pygame.Rect(
                        (x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))
                elif(self.__world.isBlock((x, y))):
                    pygame.draw.rect(self.__win, BLACK, pygame.Rect(
                        (x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))
                elif(self.__world.getPheromone((x, y)) > 0):
                    color = self.getPheromoneColor((x, y))
                    pygame.draw.rect(self.__win, color, pygame.Rect(
                        (x*PIXELSIZE, y*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))

    # draw colony home
    def renderHome(self):
        for colony in self.__world.getColonies():
            colonypos = colony.getPos()
            pygame.draw.rect(self.__win, RED, pygame.Rect(
                (colonypos[0]*PIXELSIZE, colonypos[1]*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))

    def renderAnts(self):
        for colony in self.__world.getColonies():
            ants = colony.getAnts()
            antcolor = colorstr2rgb(colony.getColor())
            for ant in ants:
                antpos = ant.getPos()
                antimg = pygame.image.load(Path(__file__).parent / "ant.png")
                # imgrect = antimg.get_rect()
                self.__win.blit(antimg, (antpos[0]*PIXELSIZE, antpos[1]*PIXELSIZE))
                # pygame.draw.rect(self.__win, antcolor, pygame.Rect(
                #     (antpos[0]*PIXELSIZE, antpos[1]*PIXELSIZE), (PIXELSIZE, PIXELSIZE)))

    # render PyGame graphic view at each clock tick

    def update(self, dt):
        self.renderWorld()
        self.renderAnts()
        self.renderHome()
        pygame.display.flip()
