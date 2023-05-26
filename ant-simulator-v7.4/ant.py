import pygame as pg
import numpy as np
import random

from constants import *


class Ant(pg.sprite.Sprite):

    # contains rotated versions of ant images with / without food
    img_no_food_list = []
    img_with_food_list = []
    # contains rotated versions of "bitmasks" consisting of numpy array indices used for counting pheromones
    # in areas shaped like circle sectors
    phero_mask_list = []

    @staticmethod
    def init():
        '''Creates and saves rotated versions of ant images and phero masks, so that it doesn't need to be done
        anew each frame. The rotation step in degrees is specified by IMG_ROT_STEP.
        '''
        img_no_food = pg.image.load('img/ant_no_food_red.png').convert_alpha()
        img_with_food = pg.image.load('img/ant_with_food_red.png').convert_alpha()
        for i in range(IMG_LIST_SIZE):
            # pg.transform.rotate rotates counterclockwise, so a negative angle is used to match the clockwise
            # rotations used everywhere else
            Ant.img_no_food_list.append(Ant._rotate_around_center_and_crop(img_no_food, -i * IMG_ROT_STEP))
            Ant.img_with_food_list.append(Ant._rotate_around_center_and_crop(img_with_food, -i * IMG_ROT_STEP))
        for i in range(PHERO_MASK_LIST_SIZE):
            indices = [[], []]
            r = PHERO_SENSOR_DIST // CELL_SIZE
            for x in range(-r, r + 1):
                for y in range(-r, r + 1):
                    v = pg.Vector2(x, y)
                    if v.magnitude() * CELL_SIZE <= PHERO_SENSOR_DIST:
                        angle_diff = (v.as_polar()[1] - i) % 360
                        if angle_diff < PHERO_SENSOR_ANGLE / 2 or angle_diff >= 360 - PHERO_SENSOR_ANGLE / 2:
                            indices[0].append(x + r)
                            indices[1].append(y + r)
            Ant.phero_mask_list.append(tuple(indices))


    def __init__(self, world, pos, angle, colony):
        pg.sprite.Sprite.__init__(self)
        self.world = world
        self.colony = colony
        self.mode = AntMode.TO_FOOD

        # movement / position
        self.pos = pos.copy()
        self.forward_dir = pg.Vector2(1, 0).rotate(angle)
        self.velo = self.forward_dir * MAX_SPEED
        self.turning_around = False

        # steering direction update times
        self.next_random_steer_update = self.world.time
        self.next_target_steer_update = self.world.time + random.random() * TARGET_STEER_UPDATE_INTERVAL
        self.next_obstacle_steer_update = self.world.time * random.random() * OBSTACLE_STEER_UPDATE_INTERVAL
        
        # steering vectors
        self.random_steer_force = pg.Vector2(0, 0)
        self.phero_steer_force = pg.Vector2(0, 0)
        self.obstacle_steer_force = pg.Vector2(0, 0)
        self.turn_around_force = pg.Vector2(0, 0)

        # pheromone placing / food targeting
        self.last_phero_event_time = self.world.time
        self.last_phero_pos = self.pos
        self.target_food_pos = None

        # visual representation
        self.image = Ant.img_no_food_list[round(angle / IMG_ROT_STEP) % IMG_LIST_SIZE]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # debugging
        self.debug_sensor_coords = []

    def update(self, dt):
        self.place_phero()
        self.handle_random_steering()
        if self.mode == AntMode.TO_FOOD:
            self.handle_food_search()
        elif self.mode == AntMode.TO_HOME:
            self.handle_return_to_colony()
        self.handle_obstacle_steering()
        self.move(dt)

    def move(self, dt):
        # combine the different steering vectors
        steer_force = self.random_steer_force + self.phero_steer_force + self.obstacle_steer_force

        if self.turning_around:
            steer_force += self.turn_around_force * TARGET_STEER_STRENGTH
            if self.world.time > self.turn_around_end_time:
                self.turning_around = False
                # print('stop turning around')

        if steer_force.magnitude() > 0:
            desired_velo = steer_force.normalize() * MAX_SPEED
        else:
            desired_velo = pg.Vector2(0, 0)
        self.steer_towards(desired_velo, dt)

        self.forward_dir = self.velo.normalize()
        move_dist = self.velo.magnitude() * dt
        desired_pos = self.pos + self.velo * dt

        # if wall close ahead, turn around and "teleport" back a little
        if not self.world.is_traversable(self.pos + self.forward_dir * OBSTACLE_SPOT_DIST / 2):
            if not self.turning_around:
                self.start_turn_around(2)
            desired_pos = self.pos - self.forward_dir * max(COLLISION_RADIUS, move_dist)
        self.pos = desired_pos

        # apply newly changed position and direction to the visual representation of the ant
        img_index = round(self.forward_dir.as_polar()[1] / IMG_ROT_STEP) % IMG_LIST_SIZE
        if self.mode == AntMode.TO_FOOD:
            self.image = Ant.img_no_food_list[img_index]
        else:
            self.image = Ant.img_with_food_list[img_index]
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = self.pos
    
    '''Modifies the ants current velocity vector towards its desired velocity vector.'''
    def steer_towards(self, desired_velo, dt):
        steering_force = desired_velo - self.velo

        accel = steering_force * ACCEL
        if accel.magnitude() > 0:
            accel.clamp_magnitude(ACCEL)
        self.velo += accel * dt
        self.velo.clamp_magnitude(MAX_SPEED)

    def place_phero(self):
        # can't place pheromone to close to the last spot
        if self.world.is_in_bounds(self.pos) and self.pos.distance_to(self.last_phero_pos) > DIST_BETWEEN_MARKERS:
            coords = self.world.pos_to_coords(self.pos)
            # the ant's pheromone strength halves every PHERO_PLACEMENT_AMOUNT_HALVING_TIME seconds
            phero_strength = 0.5 ** ((self.world.time - self.last_phero_event_time) / PHERO_PLACEMENT_AMOUNT_HALVING_TIME)
            if self.mode == AntMode.TO_FOOD:
                self.colony.add_phero(coords, phero_strength, PheroType.TO_HOME)
            elif self.mode == AntMode.TO_HOME:
                self.colony.add_phero(coords, phero_strength, PheroType.TO_FOOD)
            self.last_phero_pos = self.pos
    
    '''Determines the random steering vector.'''
    def handle_random_steering(self):
        if self.target_food_pos is not None:
            self.random_steer_force = pg.Vector2(0, 0)
            return
        if self.world.time > self.next_random_steer_update:
            self.next_random_steer_update = self.world.time + random.uniform(RANDOM_STEER_UPDATE_MAX_INTERVAL / 3, RANDOM_STEER_UPDATE_MAX_INTERVAL)
            self.random_steer_force = self.get_random_dir(self.forward_dir) * RANDOM_STEER_STRENGTH

    def get_random_dir(self, reference_dir):
        smallest_random_dir = pg.Vector2(0, 0)
        change = -1.0
        iterations = 4
        for i in range(iterations):
            random_dir = pg.Vector2(1, 0).rotate(random.random() * 360)
            dot = reference_dir.dot(random_dir)
            if dot > change:
                change = dot
                smallest_random_dir = random_dir
        return smallest_random_dir
    
    def handle_food_search(self):
        # checks a single cell for each sensor - might be better to also do this via circle sector shapes
        map_sensor_pos_m = self.pos + self.forward_dir * MAP_SENSOR_DIST
        map_sensor_pos_l = self.pos + self.forward_dir.rotate(-MAP_SENSOR_ANGLE) * MAP_SENSOR_DIST
        map_sensor_pos_r = self.pos + self.forward_dir.rotate(MAP_SENSOR_ANGLE) * MAP_SENSOR_DIST
        map_sensor_data_m = self.world.get_cell_type(map_sensor_pos_m)
        map_sensor_data_l = self.world.get_cell_type(map_sensor_pos_l)
        map_sensor_data_r = self.world.get_cell_type(map_sensor_pos_r)

        # if very close to colony again, reset pheromone strength
        if pg.Vector2(self.pos - self.colony.pos).magnitude_squared() < self.colony.radius ** 2:
            self.last_phero_event_time = self.world.time

        # if no food found yet, look for it
        if self.target_food_pos is None:
            if map_sensor_data_m == CellType.FOOD:
                self.target_food_pos = map_sensor_pos_m.copy()
            elif map_sensor_data_l == CellType.FOOD:
                self.target_food_pos = map_sensor_pos_l.copy()
            elif map_sensor_data_r == CellType.FOOD:
                self.target_food_pos = map_sensor_pos_r.copy()

        # if food targeted already, move towards it (uses the pheromone steer vector)
        if self.target_food_pos is not None:
            # check if targeted food still exists (it might have been depleted by another ant in the meantime)
            if self.world.get_cell_type(self.target_food_pos) == CellType.FOOD:
                offset_to_food = self.target_food_pos - self.pos
                dist_to_food = offset_to_food.magnitude()
                dir_to_food = offset_to_food / dist_to_food
                self.phero_steer_force = dir_to_food * TARGET_STEER_STRENGTH
                # if very close to targeted food, pick it up and return to colony
                if dist_to_food < 5:
                    self.mode = AntMode.TO_HOME
                    self.next_target_steer_update = 0
                    self.world.take_food(self.target_food_pos)
                    self.target_food_pos = None
                    self.start_turn_around()
                    self.last_phero_event_time = self.world.time
            # if targeted food has already been depleted, target other random nearby food (if there is any)
            else:
                self.target_food_pos = self.world.get_nearby_food_pos(self.target_food_pos, 20)
        # if still no food found, follow pheromone trail
        else:
            self.handle_phero_steering()
    
    def handle_return_to_colony(self):
        # if on food tile again, reset pheromone strength
        if self.world.get_cell_type(self.pos) == CellType.FOOD:
            self.last_phero_event_time = self.world.time
        # if colony nearby, steer towards it
        if self.pos.distance_to(self.colony.pos) <= 3 * self.colony.radius:
            self.phero_steer_force = pg.Vector2(self.colony.pos - self.pos).normalize() * TARGET_STEER_STRENGTH
            # when arriving at colony, give food to it and start searching for food again
            if self.pos.distance_to(self.colony.pos) <= self.colony.radius:
                self.mode = AntMode.TO_FOOD
                self.next_target_steer_update = 0
                self.start_turn_around()
                self.colony.add_food()
                self.last_phero_event_time = self.world.time
        # if colony not nearby, follow pheromone trail
        else:
            self.handle_phero_steering()

    def handle_phero_steering(self):
        '''Determines the pheromone trail steering vector.'''
        if self.world.time > self.next_target_steer_update:
            self.phero_steer_force = pg.Vector2(0, 0)
            self.next_target_steer_update = self.world.time + TARGET_STEER_UPDATE_INTERVAL

            if USE_SIMPLE_PHERO_STEERING:
                sector_value_l, sector_value_m, sector_value_r = self.get_phero_sector_values_simple()
            else:
                sector_value_l, sector_value_m, sector_value_r = self.get_phero_sector_values()

            # steer towards direction of the sensor corresponding to the highest value
            if sector_value_m >= max(sector_value_l, sector_value_r):
                self.phero_steer_force = self.forward_dir
            elif sector_value_l >= sector_value_r:
                self.phero_steer_force = self.forward_dir.rotate(-PHERO_SENSOR_ANGLE)
            elif sector_value_r > sector_value_l:
                self.phero_steer_force = self.forward_dir.rotate(PHERO_SENSOR_ANGLE)
            self.phero_steer_force *= PHERO_WEIGHT

    def handle_obstacle_steering(self):
        '''Determines the obstacle avoidance steering vector.'''
        blocked_l = not self.world.is_traversable(
            self.pos + self.forward_dir.rotate(-OBSTACLE_SPOT_ANGLE) * OBSTACLE_SPOT_DIST)
        blocked_r = not self.world.is_traversable(
            self.pos + self.forward_dir.rotate(OBSTACLE_SPOT_ANGLE) * OBSTACLE_SPOT_DIST)

        if self.world.time > self.next_obstacle_steer_update:
            self.obstacle_steer_force = pg.Vector2(0, 0)

        if blocked_l or blocked_r:
            if blocked_l:
                self.obstacle_steer_force = self.forward_dir.rotate(90) * OBSTACLE_STEER_STRENGTH
            elif blocked_r:
                self.obstacle_steer_force = self.forward_dir.rotate(-90) * OBSTACLE_STEER_STRENGTH
            
            self.next_obstacle_steer_update = self.world.time + OBSTACLE_STEER_UPDATE_INTERVAL
            if self.obstacle_steer_force.magnitude() > 0:
                self.random_steer_force = self.obstacle_steer_force.normalize() * RANDOM_STEER_STRENGTH
            else:
                self.random_steer_force = pg.Vector2(0, 0)

    def start_turn_around(self, random_strength=0.2):
        '''Used when running straight into a wall or after picking up food / bringing food to the colony.'''
        # print('start turning around')
        return_dir = - self.forward_dir
        self.turning_around = True
        self.turn_around_end_time = self.world.time + 1.5
        perp_axis = pg.Vector2(-return_dir.y, return_dir.x)
        self.turn_around_force = return_dir + perp_axis * (random.random() - 0.5) * 2 * random_strength
    
    '''Computes the phero values for the left, right and center sensors using circle sector shapes for each.

    The ant always faces towards the center of the middle sensor sector shape. Each sector is PHERO_SENSOR_ANGLE
    degrees wide and the outer sensors are rotated PHERO_SENSOR_ANGLE degrees away from the middle sensor.
    '''
    def get_phero_sector_values(self):
        angle = self.forward_dir.as_polar()[1]
        values = [0, 0, 0]
        r = PHERO_SENSOR_DIST // CELL_SIZE
        phero_grid_vicinity = self.colony.get_phero_grid_vicinity(self.pos, r, self.mode)

        if USE_PHERO_MASK_MAX_INSTEAD_OF_SUM:
            # uses phero mask as filter for np array slice
            values[0] = phero_grid_vicinity[Ant.phero_mask_list[int(angle - PHERO_SENSOR_ANGLE) % 360]].max()
            values[1] = phero_grid_vicinity[Ant.phero_mask_list[int(angle) % 360]].max()
            values[2] = phero_grid_vicinity[Ant.phero_mask_list[int(angle + PHERO_SENSOR_ANGLE) % 360]].max()
        else:
            # uses phero mask as filter for np array slice
            values[0] = np.sum(phero_grid_vicinity[Ant.phero_mask_list[int(angle - PHERO_SENSOR_ANGLE) % 360]])
            values[1] = np.sum(phero_grid_vicinity[Ant.phero_mask_list[int(angle) % 360]])
            values[2] = np.sum(phero_grid_vicinity[Ant.phero_mask_list[int(angle + PHERO_SENSOR_ANGLE) % 360]])
        return values

    def get_phero_sector_values_simple(self):
        '''Computes the phero values for the left, right and center sensors using single phero grid cells for each.'''
        sensor_pos_l = self.pos + PHERO_SENSOR_DIST * self.forward_dir.rotate(- PHERO_SENSOR_ANGLE)
        sensor_pos_m = self.pos + PHERO_SENSOR_DIST * self.forward_dir
        sensor_pos_r = self.pos + PHERO_SENSOR_DIST * self.forward_dir.rotate(PHERO_SENSOR_ANGLE)

        results = [0, 0, 0]
        if self.world.is_in_bounds(sensor_pos_l):
            results[0] = self.colony.get_phero_strength(self.world.pos_to_coords(sensor_pos_l), self.mode)
        if self.world.is_in_bounds(sensor_pos_m):
            results[1] = self.colony.get_phero_strength(self.world.pos_to_coords(sensor_pos_m), self.mode)
        if self.world.is_in_bounds(sensor_pos_r):
            results[2] = self.colony.get_phero_strength(self.world.pos_to_coords(sensor_pos_r), self.mode)
        return results

    # doesn't work atm
    '''Draws visual representations of the shapes used for pheromone sensors.'''
    def draw_debug_sensor_coords(self, screen):
        if self.debug_sensor_coords:
            for coords in self.debug_sensor_coords[0]:
                s = pg.Surface((CELL_SIZE, CELL_SIZE), pg.SRCALPHA)
                s.fill(((127, 127, 127, 80)))
                screen.blit(s, (coords[0] * CELL_SIZE, coords[1] * CELL_SIZE))
            for coords in self.debug_sensor_coords[1]:
                s = pg.Surface((CELL_SIZE, CELL_SIZE), pg.SRCALPHA)
                s.fill(((255, 255, 255, 80)))
                screen.blit(s, (coords[0] * CELL_SIZE, coords[1] * CELL_SIZE))
            for coords in self.debug_sensor_coords[2]:
                s = pg.Surface((CELL_SIZE, CELL_SIZE), pg.SRCALPHA)
                s.fill(((127, 127, 127, 80)))
                screen.blit(s, (coords[0] * CELL_SIZE, coords[1] * CELL_SIZE))

    # image must be square
    @staticmethod
    def _rotate_around_center_and_crop(img, angle):
        '''Rotates a given image around its center by a given angle, then crops the result to the original image size.

        The image must be square for this to work properly.
        '''
        img_size = img.get_rect().size
        img_rotated = pg.transform.rotate(img, angle)
        crop_offset = (img_rotated.get_rect().width - img_size[0]) // 2
        img_cropped = pg.Surface(img_size, flags=pg.SRCALPHA)
        img_cropped.blit(img_rotated, (0, 0), ((crop_offset, crop_offset), img_size))
        return img_cropped

    # The masks' orientation looks wrong because the numpy array orientation differs from the pygame 
    # screen orientation
    @staticmethod
    def _debug_print_phero_mask(angle):
        r = PHERO_SENSOR_DIST // CELL_SIZE
        size = 2*r + 1
        a = np.zeros((size, size))
        a[Ant.phero_mask_list[angle]] = 1
        print(np.roll(a, r, (0, 1)))
