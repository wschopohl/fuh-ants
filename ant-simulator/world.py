import pygame as pg
import numpy as np
import math
import random

from constants import *
import colony
from food import Food


class World:

    def __init__(self, screen, food_spawns):
        self.FONT = pg.freetype.SysFont('Arial', 18)
        self.screen = screen

        self.ants = pg.sprite.Group()
        self.colonies = pg.sprite.Group()
        self.food = pg.sprite.Group()
        self.home_pheromones = pg.sprite.Group()
        self.food_pheromones = pg.sprite.Group()

        self.colonies.add(colony.Colony(self, pg.math.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 0))

        self.food_pheromone_map = np.zeros((WINDOW_WIDTH, WINDOW_HEIGHT), dtype=int)
        self.home_pheromone_map = np.zeros((WINDOW_WIDTH, WINDOW_HEIGHT), dtype=int)
        self.food_map = np.zeros((WINDOW_WIDTH, WINDOW_HEIGHT), dtype=bool)
        for food_spawn in food_spawns:
            self.spawn_food(food_spawn[0], food_spawn[1])


    def spawn_food(self, pos, food_amount):
        max_dist = 2 * math.sqrt(food_amount)
        for _ in range(food_amount):
            spot_found = False
            while not spot_found:
                x_dist = np.random.choice([-1, 1]) * (random.random() * math.sqrt(max_dist)) ** 2
                y_dist = np.random.choice([-1, 1]) * (random.random() * math.sqrt(max_dist)) ** 2
                x, y = int(pos.x + x_dist), int(pos.y + y_dist)
                if not self.food_map[x, y]:
                    self.food_map[x, y] = True
                    self.food.add(Food(pg.math.Vector2(x, y)))
                    spot_found = True
    
    def update(self, frame_counter):
        self.home_pheromones.update(frame_counter)
        self.food_pheromones.update(frame_counter)
        self.ants.update(frame_counter)

    def draw(self):
        self.screen.fill('dark green')
        self.home_pheromones.draw(self.screen)
        self.food_pheromones.draw(self.screen)
        self.food.draw(self.screen)
        self.colonies.draw(self.screen)
        for col in self.colonies.sprites():
            self.FONT.render_to(self.screen, col.pos - pg.math.Vector2(6, 6), str(col.food_counter), 'black')
        self.ants.draw(self.screen)

        # self.food_group.draw(screen)