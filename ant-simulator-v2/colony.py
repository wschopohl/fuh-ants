import pygame as pg

from constants import *
import ant

IMG = pg.image.load('img/colony.png')


class Colony(pg.sprite.Sprite):

    def __init__(self, world, pos, id):
        pg.sprite.Sprite.__init__(self)

        self.world = world
        self.pos = pos.copy()
        self.id = id
        self.food_counter = 0

        self.image = IMG
        self.rect = self.image.get_rect(center=pos)

        for i in range(MAX_ANTS_PER_COLONY):
            self.world.ants.add(ant.Ant(self.world, self.pos, i / MAX_ANTS_PER_COLONY * 360, self.id))
        
    def add_food(self):
        self.food_counter += 1
