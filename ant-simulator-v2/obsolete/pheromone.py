import pygame as pg
from enum import Enum
import random

from constants import *

MAX_STRENGTH = 10

IMG_HOME = []
IMG_FOOD = []
for i in range(MAX_STRENGTH + 1):
    IMG_HOME.append(pg.image.load('img/home_pheromone.png'))
    IMG_HOME[i].set_alpha(int(i / MAX_STRENGTH * 255))
    IMG_FOOD.append(pg.image.load('img/food_pheromone.png'))
    IMG_FOOD[i].set_alpha(int(i / MAX_STRENGTH * 255))


class Pheromone(pg.sprite.Sprite):
    def __init__(self, pheromone_type, pos):
        pg.sprite.Sprite.__init__(self)

        self.pheromone_type = pheromone_type
        self.strength = MAX_STRENGTH
        self.pos = pos.copy()

        if self.pheromone_type == PheromoneType.HOME:
            self.image = IMG_HOME[self.strength]
        else:
            self.image = IMG_FOOD[self.strength]
        self.rect = self.image.get_rect(center=pos)
        self.radius = 1

    def update(self, frame_counter):
        if frame_counter % PHEROMONE_DECAY_INTERVAL == 0:
            self.strength -= 1
            if self.strength <= 0:
                self.kill()
            else:
                if self.pheromone_type == PheromoneType.HOME:
                    self.image = IMG_HOME[self.strength]
                else:
                    self.image = IMG_FOOD[self.strength]
