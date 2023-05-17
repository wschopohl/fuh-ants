import pygame as pg
import numpy as np
import math
import random

from constants import *

SPEED = 2.0
TURN_RATE = 5.0
# SPEED = 8.0
# TURN_RATE = 16.0

FOOD_PICKUP_RANGE = 10

PH_MAX_STRENGTH = 10
# PH_CHECK_RANGE = 100
# PH_CHECK_ANGLE = 90     # in degrees, should be >= 1 and <= 180
PH_CHECK_RANGE = 50
PH_CHECK_ANGLE = 60     # in degrees, should be >= 1 and <= 180


class Ant(pg.sprite.Sprite):

    img_no_food_list = []
    img_with_food_list = []
    ph_check_mask_list = []  # corresponds to the sensor on the right

    @staticmethod
    def init():
        img_no_food = pg.image.load('img/ant_no_food.png').convert_alpha()
        img_with_food = pg.image.load('img/ant_with_food.png').convert_alpha()
        ph_check_surf = Ant._draw_ph_check_surf()
        for i in range(360):
            # pg.transform.rotate rotates counterclockwise, so a negative angle is used to match
            # the clockwise rotations used everywhere else
            Ant.img_no_food_list.append(Ant._rotate_around_center_and_crop(img_no_food, -i))
            Ant.img_with_food_list.append(Ant._rotate_around_center_and_crop(img_with_food, -i))
            Ant.ph_check_mask_list.append(pg.mask.from_surface(
                Ant._rotate_around_center_and_crop(ph_check_surf, -i)))

    def __init__(self, world, pos, angle, colony_id):
        pg.sprite.Sprite.__init__(self)

        self.world = world
        self.colony_id = colony_id
        self.pos = pos.copy()
        self.angle = angle          # in degrees
        self.turn_direction = 0     # -1 = turn left; 0 = straight ahead; 1 = turn right
        self.carries_food = False

        self.image = Ant.img_no_food_list[round(self.angle) % 360]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # self.rect = self.image.get_rect(center=self.pos)
        self.radius = PH_CHECK_RANGE

    def determine_turn_direction(self):
        if not self.carries_food:
            relevant_ph_id = 1
        else:
            relevant_ph_id = 0

        ph_mask = self.world.ph_masks[relevant_ph_id]
        ph_count_l = ph_mask.overlap_area(self.ph_check_mask_l, self.pos - pg.Vector2(PH_CHECK_RANGE, PH_CHECK_RANGE))
        ph_count_r = ph_mask.overlap_area(self.ph_check_mask_r, self.pos - pg.Vector2(PH_CHECK_RANGE, PH_CHECK_RANGE))

        # p_turn_away = 0.05
        # p_ignore = 0.05
        p_turn_away = 0.1
        p_ignore = 0.1
        p_turn_if_even = 0.15

        r = random.random()
        if ph_count_l > ph_count_r:
            if r < p_turn_away:
                self.turn_direction = 1
            elif r > 1 - p_ignore:
                self.turn_direction = 0
            else:
                self.turn_direction = -1
        elif ph_count_l < ph_count_r:
            if r < p_turn_away:
                self.turn_direction = -1
            elif r > 1 - p_ignore:
                self.turn_direction = 0
            else:
                self.turn_direction = 1
        else:
            if r < p_turn_if_even:
                self.turn_direction = -1
            elif r > 1 - p_turn_if_even:
                self.turn_direction = 1
            else:
                self.turn_direction = 0

    def drop_ph(self):
        if not self.carries_food:
            self.world.ph_maps[0][self.world.pos_to_index(self.pos)] = PH_MAX_STRENGTH
        else:
            self.world.ph_maps[1][self.world.pos_to_index(self.pos)] = PH_MAX_STRENGTH

    def update(self, frame_counter):
        if self.pos.x < 0:
            # self.pos.x = 0
            self.angle = 180 - self.angle
        if self.pos.x >= WINDOW_WIDTH:
            # self.pos.x = WINDOW_WIDTH - 1
            self.angle = 180 - self.angle
        if self.pos.y < 0:
            # self.pos.y = 0
            self.angle = 360 - self.angle
        if self.pos.y >= WINDOW_HEIGHT:
            # self.pos.y = WINDOW_WIDTH - 1
            self.angle = 360 - self.angle

        self.angle += self.turn_direction * TURN_RATE
        self.angle %= 360

        if not self.carries_food:
            self.image = Ant.img_no_food_list[round(self.angle) % 360]
        else:
            self.image = Ant.img_with_food_list[round(self.angle) % 360]
        self.ph_check_mask_l = Ant.ph_check_mask_list[round(self.angle - PH_CHECK_ANGLE) % 360]
        self.ph_check_mask_r = Ant.ph_check_mask_list[round(self.angle) % 360]

        self.pos += pg.Vector2(SPEED, 0).rotate(self.angle)
        self.rect.center = self.pos

        if frame_counter % ANT_TURN_INTERVAL == 0:
            self.determine_turn_direction()

        if frame_counter % PH_DROP_INTERVAL == 0:
            self.drop_ph()

        if frame_counter % ANT_COLLISION_CHECK_INTERVAL == 0:
            x, y = self.world.pos_to_index(self.pos)
            if not self.carries_food:
                food_in_range = np.where(self.world.food_map[x - FOOD_PICKUP_RANGE : x + FOOD_PICKUP_RANGE,
                                                             y - FOOD_PICKUP_RANGE : y + FOOD_PICKUP_RANGE])
                if food_in_range[0].size:
                    self.world.food_map[x - FOOD_PICKUP_RANGE + food_in_range[0][0],
                                          y - FOOD_PICKUP_RANGE + food_in_range[1][0]] = False
                    self.carries_food = True
                    self.angle = (self.angle + 180) % 360
            else:
                colonies_in_range = pg.sprite.spritecollide(self, self.world.colonies, False)
                if colonies_in_range:
                    self.carries_food = False
                    self.angle = (self.angle + 180) % 360
                    colonies_in_range[0].add_food()

    # for debugging purposes
    def draw_ph_check_masks(self):
        self.world.screen.blit(self.ph_check_mask_r.to_surface(
            setcolor=(255, 0, 0, 63), unsetcolor=(0, 0, 255, 0)), self.pos - pg.Vector2(PH_CHECK_RANGE, PH_CHECK_RANGE))
        self.world.screen.blit(self.ph_check_mask_l.to_surface(
            setcolor=(255, 255, 0, 63), unsetcolor=(0, 0, 255, 0)), self.pos - pg.Vector2(PH_CHECK_RANGE, PH_CHECK_RANGE))

    # image must be square
    @staticmethod
    def _rotate_around_center_and_crop(img, angle):
        img_size = img.get_rect().size
        img_rotated = pg.transform.rotate(img, angle)
        crop_offset = (img_rotated.get_rect().width - img_size[0]) // 2
        img_cropped = pg.Surface(img_size, flags=pg.SRCALPHA)
        img_cropped.blit(img_rotated, (0, 0), ((crop_offset, crop_offset), img_size))
        return img_cropped

    @staticmethod
    def _draw_ph_check_surf():
        cx, cy, r = PH_CHECK_RANGE, PH_CHECK_RANGE, PH_CHECK_RANGE
        angle = PH_CHECK_ANGLE
        # Start list of polygon points
        p = [(cx, cy)]
        # Get points on arc
        for n in range(0, angle):
            x = cx + int(r * math.cos(n * math.pi / 180))
            y = cy + int(r * math.sin(n * math.pi / 180))
            p.append((x, y))
        p.append((cx, cy))
        # Draw pie segment
        surf = pg.Surface((2 * PH_CHECK_RANGE, 2 * PH_CHECK_RANGE)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        pg.draw.polygon(surf, (255, 0, 0, 128), p)
        return surf
