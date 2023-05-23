import pygame as pg
import numpy as np
import math
import random
import enum

from constants import *
# import pheromone_map
import colony
# from food import Food


# img_food = None


class World:

    def __init__(self, screen):
        self.screen = screen

        self.img_food = pg.image.load('img/food.png').convert_alpha()
        self.FONT = pg.freetype.SysFont('Arial', 18)

        self.grid_size = (screen.get_rect().width // CELL_SIZE, screen.get_rect().height // CELL_SIZE)
        self.cell_grid = np.zeros(self.grid_size, dtype=np.int16)
        self.load_grid_from_src(pg.image.load('img/world02.png'))
        self.cell_grid_list = self.cell_grid.tolist()

        self.ants = pg.sprite.Group()
        self.colonies = pg.sprite.Group()
        self.colonies.add(colony.Colony(self, pg.Vector2(600, 300), 0))

        # self.food_map = np.zeros(self.screen.get_size(), dtype=bool)
        # for food_spawn in food_spawns:
        #     self.spawn_food(food_spawn[0], food_spawn[1])

        self.surf = pg.Surface(self.screen.get_size())
        self.surf.fill(BG_COLOR)
        self.wall_coords = []
        for x, y in np.transpose((self.cell_grid == CellType.WALL).nonzero()):
            draw_rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            self.wall_coords.append((x, y))
            pg.draw.rect(self.surf, (127, 127, 127), draw_rect)
        for x, y in np.transpose((self.cell_grid == CellType.FOOD).nonzero()):
            draw_rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(self.surf, (0, 255, 0), draw_rect)
    
    def load_grid_from_src(self, grid_src):
        src_array = pg.surfarray.array3d(grid_src)
        # self.cell_grid[np.where(np.all(src_array == (0, 0, 0), axis=-1))] = CellType.EMPTY
        self.cell_grid[np.where(np.all(src_array == (0, 0, 255), axis=-1))] = CellType.WALL
        self.cell_grid[np.where(np.all(src_array == (0, 255, 0), axis=-1))] = CellType.FOOD

    def spawn_food(self, pos, food_amount):
        max_dist = 3 * math.sqrt(food_amount)
        for _ in range(food_amount):
            spot_found = False

            while not spot_found:
                dist = np.random.random() * max_dist
                angle = np.random.random() * 360

                x = int(pos.x + dist * math.cos(angle))
                y = int(pos.y + dist * math.sin(angle))

                # x = cx + int(r * math.cos(n * math.pi / 180))
                # y = cy + int(r * math.sin(n * math.pi / 180))

                # x, y = int(pos.x + x_dist), int(pos.y + y_dist)
                if not self.food_map[x, y]:
                    self.food_map[x, y] = True
                    spot_found = True

            # while not spot_found:
            #     x_dist = np.random.choice([-1, 1]) * (random.random() * math.sqrt(max_dist)) ** 2
            #     y_dist = np.random.choice([-1, 1]) * (random.random() * math.sqrt(max_dist)) ** 2
            #     x, y = int(pos.x + x_dist), int(pos.y + y_dist)
            #     if not self.food_map[x, y]:
            #         self.food_map[x, y] = True
            #         spot_found = True

    def update(self, frame_counter, dt):
        # if frame_counter % PH_DECAY_INTERVAL == 0:
        #     # apply pheromone decay to pheromone maps
        #     for ph_map in self.ph_maps:
        #         np.subtract(ph_map, 1, ph_map)
        #         ph_map[ph_map < 0] = 0

        # if (frame_counter % PH_DROP_INTERVAL == 0) or (frame_counter % PH_DECAY_INTERVAL == 0):
        #     # update pheromone masks
        #     for i, ph_mask in enumerate(self.ph_masks):
        #         ph_mask.clear()
        #         for ph_pos in np.column_stack(np.where(self.ph_maps[i])):
        #             ph_mask.set_at(ph_pos)

        # self.ph_map.update(frame_counter)
        # self.ants.update(frame_counter, dt)
        self.colonies.update(frame_counter)
        self.ants.update(dt)

    def draw(self):
        self.screen.blit(self.surf, (0, 0))
        # self.screen.fill(BG_COLOR)
        # print(self.grid.values.shape, self.grid.values.shape[0])
        # for x in range(self.grid.values.shape[0]):
        #     for y in range(self.grid.values.shape[1]):
        #         draw_rect = (x * grid.CELL_SIZE, y * grid.CELL_SIZE, grid.CELL_SIZE, grid.CELL_SIZE)
        #         if self.grid.values[x, y] == CellType.WALL:
        #             pg.draw.rect(self.screen, (127, 127, 127), draw_rect)
        #         elif self.grid.values[x, y] == CellType.FOOD:
        #             pg.draw.rect(self.screen, (0, 255, 0), draw_rect)

        # pg.draw.rect(self.screen, (50, 50, 50), (300, 0, 100, 500))
        # pg.draw.rect(self.screen, (50, 50, 50), (700, 400, 50, 400))
        # pg.draw.rect(self.screen, (50, 50, 50), (700, 400, 300, 50))

        # self.ph_map.draw(self.screen)

        # for food_pos in np.column_stack(np.where(self.food_map)):
        #     self.screen.blit(self.img_food, food_pos)

        # for col in self.colonies.sprites():
        #     for i, ph_grid in enumerate(col.ph_grids):
        #         ph_surf = pg.Surface(ph_grid.shape, flags=pg.SRCALPHA)
        #         # ph_surf = pg.Surface(self.screen.get_size(), flags=pg.SRCALPHA)
        #         ph_surf.fill(PH_COLORS[i])
        #         alpha_array = pg.surfarray.pixels_alpha(ph_surf)
        #         alpha_array[:] = ph_grid * (255 // colony.PH_MAX_STRENGTH)
        #         del alpha_array
        #         ph_surf = pg.transform.scale(ph_surf, self.screen.get_size())
        #         self.screen.blit(ph_surf, (0, 0))

        for col in self.colonies.sprites():
            for i, ph_img in enumerate(col.ph_imgs):
                # ph_surf = pg.Surface(ph_grid.shape, flags=pg.SRCALPHA)
                # # ph_surf = pg.Surface(self.screen.get_size(), flags=pg.SRCALPHA)
                # ph_surf.fill(PH_COLORS[i])
                # alpha_array = pg.surfarray.pixels_alpha(ph_surf)
                # alpha_array[:] = ph_grid * (255 // colony.PH_MAX_STRENGTH)
                # del alpha_array
                # ph_surf = pg.transform.scale(ph_surf, self.screen.get_size())
                # self.screen.blit(ph_surf, (0, 0))
                self.screen.blit(ph_img, (0, 0))

        self.colonies.draw(self.screen)

        for col in self.colonies.sprites():
            text, text_rect = self.FONT.render(str(col.food_counter))
            self.screen.blit(text, col.pos - pg.Vector2(text_rect.size) / 2)

        self.ants.draw(self.screen)
    
    def get_cell_type(self, coords):
        return self.cell_grid_list[coords[0]][coords[1]]
        # return self.cell_grid[coords]
    
    def is_in_bounds(self, pos):
        return 0 <= pos.x and pos.x < WINDOW_WIDTH and pos.y >= 0 and pos.y < WINDOW_HEIGHT

    def pos_to_coords(self, pos):
        coords_x = int(pos.x / CELL_SIZE)
        coords_y = int(pos.y / CELL_SIZE)
        return coords_x, coords_y


