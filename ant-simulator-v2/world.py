import pygame as pg
import numpy as np
import math
import random
import enum

from constants import *
import colony
# from food import Food


# img_food = None


class World:

    def __init__(self, screen, food_spawns):
        self.screen = screen

        self.FONT = pg.freetype.SysFont('Arial', 18)
        self.img_food = pg.image.load('img/food.png').convert_alpha()

        self.ants = pg.sprite.Group()

        self.colonies = pg.sprite.Group()
        self.colonies.add(colony.Colony(self, pg.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 0))

        self.ph_maps = []
        self.ph_masks = []
        for _ in range(len(PH_TYPES)):
            self.ph_maps.append(np.zeros(self.screen.get_size(), dtype=np.int8))
            self.ph_masks.append(pg.Mask(self.screen.get_size(), fill=False))

        self.food_map = np.zeros(self.screen.get_size(), dtype=bool)
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
                    # self.food_list.append((x, y))
                    # self.food.add(Food(pg.Vector2(x, y)))
                    spot_found = True

    def update(self, frame_counter):
        if frame_counter % PH_DECAY_INTERVAL == 0:
            # apply pheromone decay to pheromone maps
            for ph_map in self.ph_maps:
                np.subtract(ph_map, 1, ph_map)
                ph_map[ph_map < 0] = 0

        if (frame_counter % PH_DROP_INTERVAL == 0) or (frame_counter % PH_DECAY_INTERVAL == 0):
            # update pheromone masks
            for i, ph_mask in  enumerate(self.ph_masks):
                ph_mask.clear()
                for ph_pos in np.column_stack(np.where(self.ph_maps[i])):
                    ph_mask.set_at(ph_pos)

        self.ants.update(frame_counter)

    def draw(self):
        for i, ph_map in enumerate(self.ph_maps):
            ph_surf = pg.Surface(self.screen.get_size(), flags=pg.SRCALPHA)
            ph_surf.fill(PH_COLORS[i])
            alpha_array = pg.surfarray.pixels_alpha(ph_surf)
            alpha_array[:] = ph_map * (255 // PH_MAX_STRENGTH)
            del alpha_array
            self.screen.blit(ph_surf, (0, 0))

        for food_pos in np.column_stack(np.where(self.food_map)):
            self.screen.blit(self.img_food, food_pos)

        self.colonies.draw(self.screen)
        for col in self.colonies.sprites():
            self.FONT.render_to(self.screen, col.pos - pg.Vector2(6, 6), str(col.food_counter), 'black')

        self.ants.draw(self.screen)
        
        if SHOW_PHEROMONE_CHECK_MASKS:
            for ant in self.ants.sprites():
                ant.draw_ph_check_masks()

    @staticmethod
    def pos_to_index(pos):
        x, y = int(pos.x), int(pos.y)
        if x < 0:
            x = 0
        if x >= WINDOW_WIDTH:
            x = WINDOW_WIDTH - 1
        if y < 0:
            y = 0
        if y >= WINDOW_HEIGHT:
            y = WINDOW_HEIGHT - 1
        return x, y
