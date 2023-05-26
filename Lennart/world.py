import pygame as pg
import numpy as np

from constants import *
import colony


class World:

    def __init__(self, screen):
        self.screen = screen
        self.screen_size = screen.get_size()
        self.grid_size = (screen.get_rect().width // CELL_SIZE, screen.get_rect().height // CELL_SIZE)
        self.FONT = pg.freetype.SysFont('Arial', 18)
        self.time = 0

        # could probably just use python lists instead of sprite groups
        self.ants = pg.sprite.Group()
        self.colonies = pg.sprite.Group()

        self.cell_grid = self.load_grid_from_src(pg.image.load(WORLD_PATH))
        # also store cell grid as list to allow for faster requests of single values
        self.cell_grid_list = self.cell_grid.tolist()

        self.food_grid = np.zeros(self.grid_size, dtype=np.int16)
        self.food_grid[np.where(self.cell_grid == CellType.FOOD)] = INIT_FOOD_PER_CELL
        self.draw_food_img()
        self.food_grid_changed = False

        # draw the cell grid consisting empty cells and walls once at the beginning and save it
        self.bg_img = pg.Surface(self.screen.get_size())
        self.bg_img.fill(BG_COLOR)
        for x, y in np.transpose((self.cell_grid == CellType.WALL).nonzero()):
            draw_rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(self.bg_img, (127, 127, 127), draw_rect)
    
    def load_grid_from_src(self, grid_src):
        '''Loads wall and food position information from an image into the world cell grid.
        
        The image size must be equal to self.grid_size. Walls must have the color (0, 0, 255) 
        and food must have the color (0, 255, 0), all other colors will be turned into empty 
        tiles.
        '''
        src_array = pg.surfarray.array3d(grid_src)
        # load cell grid
        cell_grid = np.zeros(self.grid_size, dtype=np.int16)
        cell_grid[np.where(np.all(src_array == (0, 0, 255), axis=-1))] = CellType.WALL
        cell_grid[np.where(np.all(src_array == (0, 255, 0), axis=-1))] = CellType.FOOD
        # load colony positions and add the colonies to the world
        for id, colony_coords in enumerate(np.argwhere(np.all(src_array == (255, 0, 0), axis=-1)).tolist()):
            self.colonies.add(colony.Colony(self, self.coords_to_pos(colony_coords), id))
        return cell_grid

    def update(self, dt):
        self.time += dt
        self.colonies.update()
        self.ants.update(dt)
        if self.food_grid_changed:
            self.draw_food_img()
            self.food_grid_changed = False

    def draw(self):
        # draw world cell grid (= background + walls)
        self.screen.blit(self.bg_img, (0, 0))
        # draw food grid
        self.screen.blit(self.food_img, (0, 0))
        # draw phero grids
        for col in self.colonies.sprites():
            for phero_img in col.phero_imgs:
                self.screen.blit(phero_img, (0, 0))
        # draw colonies with food counters
        self.colonies.draw(self.screen)
        for col in self.colonies.sprites():
            text, text_rect = self.FONT.render(str(col.food_counter))
            self.screen.blit(text, col.pos - pg.Vector2(text_rect.size) / 2)
        # draw ants
        self.ants.draw(self.screen)
        # draw sensor masks (for debugging, doesn't work atm)
        if DEBUG_DRAW_SENSOR_MASKS:
            for ant in self.ants.sprites():
                ant.draw_debug_sensor_coords(self.screen)
    
    def draw_food_img(self):
        '''If food has been taken by ants, redraw the food image.'''
        food_img_pre_scaling = pg.Surface(self.grid_size, flags=pg.SRCALPHA).convert_alpha()
        food_img_pre_scaling.fill((0, 255, 0))
        alpha_array = pg.surfarray.pixels_alpha(food_img_pre_scaling)
        alpha_array[:] = self.food_grid * (255 / INIT_FOOD_PER_CELL)
        del alpha_array
        self.food_img = pg.transform.scale(food_img_pre_scaling, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def take_food(self, pos):
        if FOOD_DEPLETABLE:
            coords = self.pos_to_coords(pos)
            self.food_grid[coords] = max(self.food_grid[coords] - 1, 0)
            self.food_grid_changed = True
            if self.food_grid[coords] == 0:
                self.cell_grid[coords] = CellType.EMPTY
                self.cell_grid_list[coords[0]][coords[1]] = CellType.EMPTY
    
    def get_nearby_food_pos(self, pos, max_dist):
        '''Is needed when the food cell an ant has targeted is depleted before the ant reaches it.'''
        coords = self.pos_to_coords(pos)
        max_cell_dist = max_dist // CELL_SIZE
        x_min = max(coords[0] - max_cell_dist, 0)
        x_max = min(coords[0] + max_cell_dist, self.grid_size[0] - 1)
        y_min = max(coords[1] - max_cell_dist, 0)
        y_max = min(coords[1] + max_cell_dist, self.grid_size[1] - 1)
        food_coords_list = np.argwhere(self.food_grid[x_min : x_max, y_min : y_max]).tolist()
        if len(food_coords_list):
            food_coords = food_coords_list[np.random.randint(len(food_coords_list))]
            return self.coords_to_pos(food_coords)
        else:
            return None

    def get_cell_type(self, pos):
        '''Returns the cell type at a given screen position as a CellType enum value.'''
        if self.is_in_bounds(pos):
            coords = self.pos_to_coords(pos)
            # using a list instead of a numpy array here is much faster for single values
            return self.cell_grid_list[coords[0]][coords[1]]
        else:
            return CellType.OUT_OF_BOUNDS

    # def get_cell_type_coords(self, coords):
    #     if self.is_in_bounds_coords(coords):
    #         return self.cell_grid_list[coords[0]][coords[1]]
    #     else:
    #         return CellType.OUT_OF_BOUNDS

    def is_in_bounds(self, pos):
        '''Returns True if the given position is inside the screen.'''
        return 0 <= pos.x and pos.x < WINDOW_WIDTH and pos.y >= 0 and pos.y < WINDOW_HEIGHT

    # def is_in_bounds_coords(self, coords):
    #     return (0 <= coords[0] and coords[0] < self.grid_size[0]
    #             and coords[1] >= 0 and coords[1] < self.grid_size[1])

    def pos_to_coords(self, pos):
        '''Converts a given screen position to cell / phero grid coords.'''
        coords_x = int(pos.x / CELL_SIZE)
        coords_y = int(pos.y / CELL_SIZE)
        return coords_x, coords_y
    
    def coords_to_pos(self, coords):
        '''Converts given cell / phero grid coords to a screen position.'''
        return CELL_SIZE * pg.Vector2(coords) + pg.Vector2(CELL_SIZE, CELL_SIZE) / 2

    def is_traversable(self, pos):
        '''Returns True if the given screen position is in bounds and not on a wall cell.'''
        return self.get_cell_type(pos) not in [CellType.OUT_OF_BOUNDS, CellType.WALL]
