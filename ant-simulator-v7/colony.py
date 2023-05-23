import pygame as pg
import numpy as np

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

        self.ph_grids = []
        for _ in range(len(PheromoneType)):
            self.ph_grids.append(np.zeros(self.world.grid_size, dtype=np.int16))
        
        self.ph_grid_lists = []
        for _ in range(len(PheromoneType)):
            self.ph_grid_lists.append(np.zeros(self.world.grid_size, dtype=np.int16).tolist())
        
        self.ph_imgs = []
        for _ in range(len(PheromoneType)):
            surf = pg.Surface(self.world.grid_size, flags=pg.SRCALPHA)
            surf.fill((0, 0, 0, 0))
            self.ph_imgs.append(surf)

        self.image = IMG
        self.rect = self.image.get_rect(center=pos)

        # for i in range(MAX_ANTS_PER_COLONY):
        #     self.world.ants.add(ant.Ant(self.world, self.pos, i / MAX_ANTS_PER_COLONY * 360, self))
        phero = ant.PheroGrid(self.world.screen.get_size())
        for i in range(MAX_ANTS_PER_COLONY):
            self.world.ants.add(ant.Ant(self.world, self.pos, i / MAX_ANTS_PER_COLONY * 360, self, phero))

    def update(self, frame_counter):
        if frame_counter % PH_DECAY_INTERVAL == 0:
            # for ph_grid_list in self.ph_grid_lists:
            #     for x in range(self.world.grid_size[0]):
            #         for y in range(self.world.grid_size[1]):
            #             ph_grid_list[x][y] -= PH_DECAY_AMOUNT
            #             ph_grid_list[x][y] = max(ph_grid_list[x][y], 0)
            for i, ph_grid_list in enumerate(self.ph_grid_lists):
                ph_grid = np.array(ph_grid_list)
                np.subtract(ph_grid, PH_DECAY_AMOUNT, ph_grid)
                ph_grid[ph_grid < 0] = 0
                self.ph_grid_lists[i] = ph_grid.tolist()
        # if frame_counter % PH_DECAY_INTERVAL == 0:
        #     for ph_grid in self.ph_grids:
        #         np.subtract(ph_grid, PH_DECAY_AMOUNT, ph_grid)
        #         ph_grid[ph_grid < 0] = 0

        if frame_counter % PH_IMG_UPDATE_INTERVAL == 0:
        # if frame_counter % PH_DECAY_INTERVAL == 0:
        # if frame_counter % PH_DECAY_INTERVAL == 0 or frame_counter % PH_DROP_INTERVAL == 0:
            for i, ph_img in enumerate(self.ph_imgs):
                ph_img_pre_scaling = pg.Surface(self.world.grid_size, flags=pg.SRCALPHA).convert_alpha()
                ph_img_pre_scaling.fill(PH_COLORS[i])
                alpha_array = pg.surfarray.pixels_alpha(ph_img_pre_scaling)
                # print(np.array(self.ph_grid_lists[i]))
                alpha_array[:] = np.array(self.ph_grid_lists[i]) * (127 / PH_MAX_STRENGTH)
                # print(self.grids[i])
                del alpha_array
                self.ph_imgs[i] = pg.transform.scale(ph_img_pre_scaling, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def get_ph_strength(self, coords, ph_type):
        return self.ph_grid_lists[ph_type][coords[0]][coords[1]]

    def add_pheromone(self, coords, strength, ph_type):
        self.ph_grid_lists[ph_type][coords[0]][coords[1]] += strength * PH_ADD_AMOUNT
        if self.ph_grid_lists[ph_type][coords[0]][coords[1]] > PH_MAX_STRENGTH:
            self.ph_grid_lists[ph_type][coords[0]][coords[1]] = PH_MAX_STRENGTH

    # def get_ph_strength(self, coords, ph_type):
    #     return self.ph_grids[ph_type][coords]

    # def add_pheromone(self, coords, strength, ph_type):
    #     self.ph_grids[ph_type][coords] += strength * PH_ADD_AMOUNT
    #     if self.ph_grids[ph_type][coords] > PH_MAX_STRENGTH:
    #         self.ph_grids[ph_type][coords] = PH_MAX_STRENGTH
    
    def add_food(self):
        self.food_counter += 1
