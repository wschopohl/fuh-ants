import pygame as pg

IMG = pg.image.load('img/food.png')


class Food(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)

        self.pos = pos.copy()

        self.image = IMG
        self.rect = self.image.get_rect(center=pos)