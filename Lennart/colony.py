import pygame as pg
import numpy as np

from constants import *
import ant


class Colony(pg.sprite.Sprite):
    '''Spawns ants, counts food and handles pheromone trail data and images.'''

    def __init__(self, world, pos, id):
        pg.sprite.Sprite.__init__(self)

        self.world = world
        self.pos = pos.copy()
        self.id = id
        self.food_counter = 0

        self.image = pg.image.load('img/colony.png')
        self.rect = self.image.get_rect(center=pos)
        self.radius = 20

        self.next_phero_decay_update = self.world.time + PHERO_DECAY_UPDATE_INTERVAL
        self.next_phero_img_update = self.world.time + PHERO_IMG_UPDATE_INTERVAL

        # phero grids are padded with zeroes at the bottom and right, so that get_phero_grid_vicinity() 
        # works properly
        self.phero_grids = []
        for _ in range(len(PheroType)):
            grid_size = (self.world.grid_size[0] + 2 * PHERO_ARR_OFFSET,
                            self.world.grid_size[1] + 2 * PHERO_ARR_OFFSET)
            self.phero_grids.append(np.zeros(grid_size, dtype=np.int16))
        
        # phero images are used to display the phero trails on the screen, these are not updated every frame
        self.phero_imgs = []
        for _ in range(len(PheroType)):
            surf = pg.Surface(self.world.grid_size, flags=pg.SRCALPHA)
            surf.fill((0, 0, 0, 0))
            self.phero_imgs.append(surf)

        for i in range(MAX_ANTS_PER_COLONY):
            self.world.ants.add(ant.Ant(self.world, self.pos, i / MAX_ANTS_PER_COLONY * 360, self))

    def update(self):
        # apply a decay tick to phero grid
        if self.world.time > self.next_phero_decay_update:
            for i, phero_grid in enumerate(self.phero_grids):
                np.subtract(phero_grid, PHERO_DECAY_AMOUNT, phero_grid)
                phero_grid[phero_grid < 0] = 0
            self.next_phero_decay_update = self.world.time + PHERO_DECAY_UPDATE_INTERVAL

        # redraw the image representing the pheromone trails for the colony
        if self.world.time > self.next_phero_img_update:
            for i, phero_img in enumerate(self.phero_imgs):
                phero_img_pre_scaling = pg.Surface(self.world.grid_size, flags=pg.SRCALPHA).convert_alpha()
                phero_img_pre_scaling.fill(PHERO_COLORS[self.id][i])
                alpha_array = pg.surfarray.pixels_alpha(phero_img_pre_scaling)
                # sliced to not include the padding at the bottom and right
                alpha_array[:] = (self.phero_grids[i][: -2 * PHERO_ARR_OFFSET, : -2 * PHERO_ARR_OFFSET]
                                  * (127 / PHERO_MAX_STRENGTH))
                del alpha_array
                self.phero_imgs[i] = pg.transform.scale(phero_img_pre_scaling, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.next_phero_img_update = self.world.time + PHERO_IMG_UPDATE_INTERVAL

    def get_phero_strength(self, coords, phero_type):
        return self.phero_grids[phero_type][coords]
        
    def get_phero_grid_vicinity(self, pos, max_dist, phero_type):
        '''Returns a phero grid square slice corresponding to the given pheromone type.
        
        Contains the cell corresponding to the given screen pos and all cells that are no further than max_dist 
        away from that cell horizontally and vertically. The returned slice contains zeroes at indices outside 
        of the world grid size.
        '''
        coords_x, coords_y = self.world.pos_to_coords(pos)
        coords_x = int(pg.math.clamp(coords_x, 0, self.world.grid_size[0] - 1))
        coords_y = int(pg.math.clamp(coords_y, 0, self.world.grid_size[1] - 1))
        if coords_x - max_dist >= 0 and coords_y - max_dist >= 0:
            # if the ant is at the very bottom / right of the screen, indices larger than the world grid size 
            # will fall into the zero padding on the bottom / right
            return self.phero_grids[phero_type][coords_x - max_dist : coords_x + max_dist + 1,
                                                coords_y - max_dist : coords_y + max_dist + 1]
        else:
            # if the ant is at the very top / left of the screen, the vicinity may contain negative indices, by 
            # using numpy.take these indices can be 'rolled over' to the zero padding on the bottom / right
            range_x = range(coords_x - max_dist, coords_x + max_dist + 1)
            range_y = range(coords_y - max_dist, coords_y + max_dist + 1)
            return self.phero_grids[phero_type].take(range_x, mode='wrap', axis=0).take(range_y, mode='wrap', axis=1)

    def add_phero(self, coords, strength, phero_type):
        '''Adds pheromone of a given type to the given coords of the corresponding phero grid.
        
        strength should be a value between 0 and 1.
        '''
        self.phero_grids[phero_type][coords] += strength * PHERO_ADD_AMOUNT
        if self.phero_grids[phero_type][coords] > PHERO_MAX_STRENGTH:
            self.phero_grids[phero_type][coords] = PHERO_MAX_STRENGTH

    def add_food(self):
        self.food_counter += 1
