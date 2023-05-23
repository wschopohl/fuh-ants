import pygame as pg
import numpy as np
# import math
# import random
# import enum

from constants import *

CELL_SIZE = 5   # in pixels, must be divisor of window width and height
# CELL_SIZE = 10   # in pixels, must be divisor of window width and height
PH_MAX_STRENGTH = 250
PH_DECAY_AMOUNT = 2
PH_ADD_AMOUNT = 50
# PH_DECAY_INTERVAL = FPS_LIMIT  # in frames


class PheromoneMap:

    def __init__(self):
        self.cols = WINDOW_WIDTH // CELL_SIZE
        self.rows = WINDOW_HEIGHT // CELL_SIZE
        self.grids = []
        self.imgs = []
        for _ in range(len(PH_TYPES)):
            self.grids.append(np.zeros((self.cols, self.rows), dtype=np.int16))
            self.imgs.append(pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pg.SRCALPHA).convert())
    
    def update(self, frame_counter):
        if frame_counter % PH_DECAY_INTERVAL == 0:
            for grid in self.grids:
                np.subtract(grid, PH_DECAY_AMOUNT, grid)
                grid[grid < 0] = 0
        if frame_counter % PH_DECAY_INTERVAL == 0 or frame_counter % PH_DROP_INTERVAL == 0:
            for i, img in enumerate(self.imgs):
                img_pre_scaling = pg.Surface((self.cols, self.rows), flags=pg.SRCALPHA).convert_alpha()
                img_pre_scaling.fill(PH_COLORS[i])
                alpha_array = pg.surfarray.pixels_alpha(img_pre_scaling)
                alpha_array[:] = self.grids[i] * (127 / PH_MAX_STRENGTH)
                # print(self.grids[i])
                del alpha_array
                self.imgs[i] = pg.transform.scale(img_pre_scaling, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def draw(self, screen):
        pass
        for i, img in enumerate(self.imgs):
            screen.blit(img, (0, 0))

    # def drop_pheromone(self, pos, strength, ph_type):
    #     if self.is_in_bounds(pos):
    #         self.grids[ph_type.value][self.pos_to_coords(pos)] += strength * PH_ADD_AMOUNT
    #         if self.grids[ph_type.value][self.pos_to_coords(pos)] > PH_MAX_STRENGTH:
    #             self.grids[ph_type.value][self.pos_to_coords(pos)] = PH_MAX_STRENGTH

    # def get_pheromone_strength(self, pos, ph_type):
    #     if self.is_in_bounds(pos):
    #         return self.grids[ph_type][self.pos_to_coords(pos)]
    #     else:
    #         return 0
    
    def is_in_bounds(self, pos):
        return 0 <= pos.x and pos.x < WINDOW_WIDTH and pos.y >= 0 and pos.y < WINDOW_HEIGHT

    def pos_to_coords(self, pos):
        coords_x = int(pos.x / CELL_SIZE)
        coords_y = int(pos.y / CELL_SIZE)
        # coords_x = max(coords_x, 0)
        # coords_x = min(coords_x, self.cols - 1)
        # coords_y = max(coords_y, 0)
        # coords_y = min(coords_y, self.rows - 1)
        return coords_x, coords_y

