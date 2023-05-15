import pygame as pg
import math
import random

from constants import *
import pheromone

SPEED = 2.0
TURN_RATE = 2.0

PHEROMONE_CHECK_RANGE = 120
PHEROMONE_CHECK_ANGLE = 60

IMG_NO_FOOD = pg.image.load('img/ant.png')
IMG_WITH_FOOD = pg.image.load('img/ant_with_food.png')


class Ant(pg.sprite.Sprite):
    def __init__(self, world, pos, angle, colony_id):
        # pg.sprite.Sprite.__init__(self, self.containers)
        pg.sprite.Sprite.__init__(self)

        self.world = world
        self.colony_id = colony_id
        self.pos = pos.copy()
        self.angle = angle  # in degrees
        self.turn_direction = 0   # -1 = turn left; 0 = straight ahead; 1 = turn right

        self.carries_food = False

        self.image = pg.transform.rotate(IMG_NO_FOOD, self.angle)
        self.rect = self.image.get_rect(center=pos)
        self.radius = PHEROMONE_CHECK_RANGE

    def determine_turn_direction(self):
        if not self.carries_food:
            relevant_pheromones = self.world.food_pheromones
        else:
            relevant_pheromones = self.world.home_pheromones

        pheromones_in_range = pg.sprite.spritecollide(self, relevant_pheromones, False, pg.sprite.collide_circle)
        ph_counter_left = 0
        ph_counter_right = 0
        for ph in pheromones_in_range:
            relative_angle = ((ph.pos - self.pos).as_polar()[1] - self.angle) % 360
            if relative_angle >= 360 - PHEROMONE_CHECK_ANGLE:
                # ph_counter_left += 1
                ph_counter_left += ph.strength
            elif relative_angle > 0 and relative_angle <= PHEROMONE_CHECK_ANGLE:
                # ph_counter_right += 1
                ph_counter_right += ph.strength
        
        r = random.random()
        if ph_counter_left > ph_counter_right:
            if r < 0.1:
                self.turn_direction = 1
            elif r < 0.2:
                self.turn_direction = 0
            else:
                self.turn_direction = -1
        elif ph_counter_left < ph_counter_right:
            if r < 0.1:
                self.turn_direction = -1
            elif r < 0.2:
                self.turn_direction = 0
            else:
                self.turn_direction = 1
        else:
            if r < 0.2:
                self.turn_direction = -1
            elif r > 0.8:
                self.turn_direction = 1
            else:
                self.turn_direction = 0

    def drop_pheromone(self):
        if not self.carries_food:
            self.world.home_pheromones.add(pheromone.Pheromone(pheromone.PheromoneType.HOME, self.pos))
        else:
            self.world.food_pheromones.add(pheromone.Pheromone(pheromone.PheromoneType.FOOD, self.pos))

    def update(self, frame_counter):
        # if random.random() < 0.05:
        #     self.turn_direction *= -1

        if frame_counter % ANT_TURN_INTERVAL == 0:
            self.determine_turn_direction()

        if self.pos[0] < 0 or self.pos[0] > WINDOW_WIDTH or self.pos[1] < 0 or self.pos[1] > WINDOW_HEIGHT:
            self.angle += 180
        self.angle += self.turn_direction * TURN_RATE
        self.angle %= 360

        if not self.carries_food:
            self.image = pg.transform.rotate(IMG_NO_FOOD, (-1) * self.angle)
        else:
            self.image = pg.transform.rotate(IMG_WITH_FOOD, (-1) * self.angle)

        # self.pos += pg.math.Vector2(0, SPEED).rotate(self.angle * (-1))
        self.pos += pg.math.Vector2(SPEED, 0).rotate(self.angle)
        self.rect.center = self.pos

        if frame_counter % PHEROMONE_DROP_INTERVAL == 0:
            self.drop_pheromone()

        if frame_counter % ANT_COLLISION_CHECK_INTERVAL == 0:
            if not self.carries_food:
                food_in_range = pg.sprite.spritecollide(self, self.world.food, False)
                if food_in_range:
                    self.carries_food = True
                    self.angle = (self.angle + 180) % 360
                    food_in_range[0].kill()
            else:
                colonies_in_range = pg.sprite.spritecollide(self, self.world.colonies, False)
                if colonies_in_range:
                    self.carries_food = False
                    self.angle = (self.angle + 180) % 360
                    colonies_in_range[0].add_food()
