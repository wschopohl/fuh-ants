import pygame as pg

img = None


class Food(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)

        self.pos = pos.copy()

        self.image = img
        self.rect = self.image.get_rect(center=pos)
