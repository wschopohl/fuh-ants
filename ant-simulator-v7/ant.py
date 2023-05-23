import pygame as pg
import numpy as np
import math
import random

from math import pi, sin, cos, atan2, radians, degrees
from random import randint

from constants import *

SPEED = 100.0
TURN_RATE = 120.0

FOOD_PICKUP_RANGE = 10

PH_MAX_STRENGTH = 10
# PH_CHECK_RANGE = 100
# PH_CHECK_ANGLE = 90     # in degrees, should be >= 1 and <= 180
PH_CHECK_RANGE = 50
PH_CHECK_ANGLE = 90     # in degrees, should be >= 1 and <= 180

IMG_ROT_STEP = 1   # must be divisor of 360
# IMG_ROT_STEP = 10   # must be divisor of 360
IMG_LIST_SIZE = 360 // IMG_ROT_STEP


class Ant(pg.sprite.Sprite):

    img_no_food_list = []
    img_with_food_list = []
    ph_check_mask_list = []  # default angle corresponds to the middle sensor
    ph_check_mask_arrays = []  # default angle corresponds to the middle sensor

    @staticmethod
    def init():
        img_no_food = pg.image.load('img/ant_no_food_red.png').convert_alpha()
        img_with_food = pg.image.load('img/ant_with_food_red.png').convert_alpha()
        for i in range(IMG_LIST_SIZE):
            # pg.transform.rotate rotates counterclockwise, so a negative angle is used to match
            # the clockwise rotations used everywhere else
            Ant.img_no_food_list.append(Ant._rotate_around_center_and_crop(img_no_food, -i * IMG_ROT_STEP))
            Ant.img_with_food_list.append(Ant._rotate_around_center_and_crop(img_with_food, -i * IMG_ROT_STEP))

    def __init__(self, world, pos, angle, colony, phero):
        pg.sprite.Sprite.__init__(self)

        self.world = world
        self.colony = colony
        self.pos = pos.copy()
        self.angle = angle          # in degrees
        self.timer = 0
        # self.mode = AntMode.TO_FOOD
        self.wander_strength = 0.1
        # self.just_found_food = False

        self.image = Ant.img_no_food_list[round(self.angle / IMG_ROT_STEP) % IMG_LIST_SIZE]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # =====

        self.drawSurf = world.screen
        self.curW, self.curH = self.drawSurf.get_size()
        self.pgSize = (int(self.curW/CELL_SIZE), int(self.curH/CELL_SIZE))
        self.isMyTrail = np.full(self.pgSize, False)
        self.phero = phero
        self.nest = self.colony.pos

        # self.image = pg.Surface((12, 21)).convert()
        # self.image.set_colorkey(0)
        # cBrown = (100,42,42)
        # # Draw Ant
        # pg.draw.aaline(self.image, cBrown, [0, 5], [11, 15])
        # pg.draw.aaline(self.image, cBrown, [0, 15], [11, 5]) # legs
        # pg.draw.aaline(self.image, cBrown, [0, 10], [12, 10])
        # pg.draw.aaline(self.image, cBrown, [2, 0], [4, 3]) # antena l
        # pg.draw.aaline(self.image, cBrown, [9, 0], [7, 3]) # antena r
        # pg.draw.ellipse(self.image, cBrown, [3, 2, 6, 6]) # head
        # pg.draw.ellipse(self.image, cBrown, [4, 6, 4, 9]) # body
        # pg.draw.ellipse(self.image, cBrown, [3, 13, 6, 8]) # rear
        # # save drawing for later
        # self.orig_img = pg.transform.rotate(self.image.copy(), -90)
        # # save drawing for later
        # # self.orig_img = self.image
        # # self.orig_img = pg.image.load('img/ant_no_food_red.png').convert_alpha()
        # self.rect = self.image.get_rect(center=self.nest)

        self.ang = self.angle
        self.desireDir = pg.Vector2(cos(radians(self.ang)),sin(radians(self.ang)))
        self.pos = pg.Vector2(self.rect.center)
        self.vel = pg.Vector2(0,0)
        self.last_sdp = (self.nest[0]/10/2,self.nest[1]/10/2)
        self.mode = AntMode.TO_FOOD

    
    # def update(self, dt):
    #     pass

    def update(self, dt):  # behavior
        

        # =====

        mid_result = left_result = right_result = 0
        mid_GA_result = left_GA_result = right_GA_result = CellType.EMPTY
        randAng = randint(0,360)
        accel = pg.Vector2(0,0)
        foodColor = CellType.FOOD  # color of food to look for
        # foodColor = (0, 255, 0)  # color of food to look for
        wandrStr = .12  # how random they walk around
        maxSpeed = 12  # 10-12 seems ok
        steerStr = 3  # 3 or 4, dono
        # Converts ant's current screen coordinates, to smaller resolution of pherogrid.
        scaledown_pos = (int(self.pos.x/CELL_SIZE), int(self.pos.y/CELL_SIZE))
        #scaledown_pos = (int((self.pos.x/self.curW)*self.pgSize[0]), int((self.pos.y/self.curH)*self.pgSize[1]))
        # Get locations to check as sensor points, in pairs for better detection.
        mid_sens = self.pos + pg.Vector2(20, 0).rotate(self.ang)
        left_sens = self.pos + pg.Vector2(18, -8).rotate(self.ang)
        right_sens = self.pos + pg.Vector2(18, 8).rotate(self.ang)
        # mid_sens = Vec2.vint(self.pos + pg.Vector2(20, 0).rotate(self.ang))
        # left_sens = Vec2.vint(self.pos + pg.Vector2(18, -8).rotate(self.ang)) # -9
        # right_sens = Vec2.vint(self.pos + pg.Vector2(18, 8).rotate(self.ang)) # 9

        if self.drawSurf.get_rect().collidepoint(mid_sens):
            mspos = (mid_sens[0]//CELL_SIZE,mid_sens[1]//CELL_SIZE)
            mid_result, mid_isID, mid_GA_result = self.sensCheck(mid_sens)
            # mid_result = self.phero.img_array[mspos]
            # mid_isID = self.isMyTrail[mspos]
            # mid_GA_result = self.drawSurf.get_at(mid_sens)[:3]
        if self.drawSurf.get_rect().collidepoint(left_sens):
            left_result, left_isID, left_GA_result = self.sensCheck(left_sens)
        if self.drawSurf.get_rect().collidepoint(right_sens):
            right_result, right_isID, right_GA_result = self.sensCheck(right_sens)
        # print(mid_result, left_result, right_result, mid_GA_result, left_GA_result, right_GA_result)

        pg.draw.circle(self.drawSurf, (200,0,200), mid_sens, 1)
        pg.draw.circle(self.drawSurf, (200,0,200), left_sens, 1)
        pg.draw.circle(self.drawSurf, (200,0,200), right_sens, 1)

        # if self.mode == 0 and self.pos.distance_to(self.nest) > 21:
        #     self.mode = 1

        if self.mode == AntMode.TO_FOOD:  # Look for food, or trail to food.
            setAcolor = (0,0,100)
            if scaledown_pos != self.last_sdp and scaledown_pos[0] in range(0,self.pgSize[0]) and scaledown_pos[1] in range(0,self.pgSize[1]):
                ph_strength = 0.5 ** (self.timer / 5000)
                self.colony.add_pheromone(scaledown_pos, ph_strength, 1 - self.mode)
                # self.phero.img_array[scaledown_pos] += setAcolor
                self.isMyTrail[scaledown_pos] = True
                self.last_sdp = scaledown_pos
            if mid_result > max(left_result, right_result):
                self.desireDir += pg.Vector2(1,0).rotate(self.ang).normalize()
                wandrStr = .1
                # wandrStr = .2
            elif left_result > right_result:
                self.desireDir += pg.Vector2(1,-2).rotate(self.ang).normalize() #left (0,-1)
                wandrStr = .1
                # wandrStr = .2
            elif right_result > left_result:
                self.desireDir += pg.Vector2(1,2).rotate(self.ang).normalize() #right (0, 1)
                wandrStr = .1
                # wandrStr = .2
            if left_GA_result == foodColor and right_GA_result != foodColor:
                self.desireDir += pg.Vector2(0,-1).rotate(self.ang).normalize() #left (0,-1)
                wandrStr = .1
            elif right_GA_result == foodColor and left_GA_result != foodColor:
                self.desireDir += pg.Vector2(0,1).rotate(self.ang).normalize() #right (0, 1)
                wandrStr = .1
            elif mid_GA_result == foodColor: # if food
                self.desireDir = pg.Vector2(-1,0).rotate(self.ang).normalize() #pg.Vector2(self.nest - self.pos).normalize()
                #self.lastFood = self.pos + pg.Vector2(21, 0).rotate(self.ang)
                maxSpeed = 5
                wandrStr = .01
                steerStr = 5
                self.mode = AntMode.TO_HOME
                self.timer = 0

        elif self.mode == AntMode.TO_HOME:  # Once found food, either follow own trail back to nest, or head in nest's general direction.
            setAcolor = (0,80,0)
            if scaledown_pos != self.last_sdp and scaledown_pos[0] in range(0,self.pgSize[0]) and scaledown_pos[1] in range(0,self.pgSize[1]):
                ph_strength = 0.5 ** (self.timer / 5000)
                self.colony.add_pheromone(scaledown_pos, ph_strength, 1 - self.mode)
                # self.phero.img_array[scaledown_pos] += setAcolor
                self.last_sdp = scaledown_pos
            if self.pos.distance_to(self.nest) < 24:
                #self.desireDir = pg.Vector2(self.lastFood - self.pos).normalize()
                self.desireDir = pg.Vector2(-1,0).rotate(self.ang).normalize()
                self.isMyTrail[:] = False #np.full(self.pgSize, False)
                maxSpeed = 5
                wandrStr = .01
                steerStr = 5
                self.mode = AntMode.TO_FOOD
                self.timer = 0
            elif mid_result > max(left_result, right_result) and mid_isID: #and mid_result[:2] == (0,0):
                self.desireDir += pg.Vector2(1,0).rotate(self.ang).normalize()
                wandrStr = .1
                # wandrStr = .2
            elif left_result > right_result and left_isID: #and left_result[:2] == (0,0):
                self.desireDir += pg.Vector2(1,-2).rotate(self.ang).normalize() #left (0,-1)
                wandrStr = .1
                # wandrStr = .2
            elif right_result > left_result and right_isID: #and right_result[:2] == (0,0):
                self.desireDir += pg.Vector2(1,2).rotate(self.ang).normalize() #right (0, 1)
                wandrStr = .1
                # wandrStr = .2
            # else:  # maybe first add ELSE FOLLOW OTHER TRAILS?
            #     self.desireDir += pg.Vector2(self.nest - self.pos).normalize() * .08
            #     wandrStr = .1   #pg.Vector2(self.desireDir + (1,0)).rotate(pg.math.Vector2.as_polar(self.nest - self.pos)[1])

        wallColor = CellType.WALL  # avoid walls of this color
        # wallColor = (127, 127, 127)  # avoid walls of this color
        if left_GA_result == wallColor:
            self.desireDir += pg.Vector2(0,2).rotate(self.ang) #.normalize()
            wandrStr = .1
            steerStr = 7
        elif right_GA_result == wallColor:
            self.desireDir += pg.Vector2(0,-2).rotate(self.ang) #.normalize()
            wandrStr = .1
            steerStr = 7
        elif mid_GA_result == wallColor:
            self.desireDir = pg.Vector2(-2,0).rotate(self.ang) #.normalize()
            maxSpeed = 4
            wandrStr = .1
            steerStr = 7

        # Avoid edges
        if not self.drawSurf.get_rect().collidepoint(left_sens) and self.drawSurf.get_rect().collidepoint(right_sens):
            self.desireDir += pg.Vector2(0,1).rotate(self.ang) #.normalize()
            wandrStr = .01
            steerStr = 5
        elif not self.drawSurf.get_rect().collidepoint(right_sens) and self.drawSurf.get_rect().collidepoint(left_sens):
            self.desireDir += pg.Vector2(0,-1).rotate(self.ang) #.normalize()
            wandrStr = .01
            steerStr = 5
        elif not self.drawSurf.get_rect().collidepoint(Vec2.vint(self.pos + pg.Vector2(21, 0).rotate(self.ang))):
            self.desireDir += pg.Vector2(-1,0).rotate(self.ang) #.normalize()
            maxSpeed = 5
            wandrStr = .01
            steerStr = 5

        randDir = pg.Vector2(cos(radians(randAng)),sin(radians(randAng)))
        self.desireDir = pg.Vector2(self.desireDir + randDir * wandrStr).normalize()
        dzVel = self.desireDir * maxSpeed
        dzStrFrc = (dzVel - self.vel) * steerStr
        accel = dzStrFrc if pg.Vector2(dzStrFrc).magnitude() <= steerStr else pg.Vector2(dzStrFrc.normalize() * steerStr)
        velo = self.vel + accel * dt
        self.vel = velo if pg.Vector2(velo).magnitude() <= maxSpeed else pg.Vector2(velo.normalize() * maxSpeed)
        self.pos += self.vel * dt
        self.ang = degrees(atan2(self.vel[1],self.vel[0]))

        img_index = round(self.ang / IMG_ROT_STEP) % IMG_LIST_SIZE
        if self.mode == AntMode.TO_FOOD:
            self.image = Ant.img_no_food_list[img_index]
        else:
            self.image = Ant.img_with_food_list[img_index]

        # # adjusts angle of img to match heading
        # self.image = pg.transform.rotate(self.orig_img, -self.ang)

        self.rect = self.image.get_rect(center=self.rect.center)  # recentering fix
        # actually update position
        self.rect.center = self.pos

        # =====

        self.timer += dt

    def sensCheck(self, sensor_pos): #, pos2): # checks given points in Array, IDs, and pixels on screen.
        sensor_coords = self.world.pos_to_coords(sensor_pos)
        # array_r = 0
        # ga_r = 0
        array_r = self.colony.get_ph_strength(sensor_coords, self.mode)
        ga_r = self.world.get_cell_type(sensor_coords)
        return array_r, True, ga_r
    
        # sdpos = (int(pos[0]/CELL_SIZE),int(pos[1]/CELL_SIZE))
        # array_r = self.phero.img_array[sdpos]
        # ga_r = self.drawSurf.get_at(pos)[:3]
        # return array_r, self.isMyTrail[sdpos], ga_r
    
    # ===========================
    
    def get_sensor_data(self, sensor_pos):
        sensor_coords = self.world.pos_to_coords(sensor_pos)
        return self.world.get_cell_type(sensor_coords), self.colony.get_ph_strength(sensor_coords, self.mode)

    def determine_desired_dir(self):
        sample_count = 20
        max_ph_strength = 0
        desired_dir = self.angle

        for _ in range(sample_count):
            sample_dir = self.angle - PH_CHECK_ANGLE + random.random() * PH_CHECK_ANGLE * 2
            sample_dist = random.random() * PH_CHECK_RANGE
            sensor_pos = self.pos + pg.Vector2.from_polar((sample_dist, sample_dir))

            if self.world.is_in_bounds(sensor_pos):
                cell_type, ph_strength = self.get_sensor_data(sensor_pos)
                if cell_type == CellType.WALL:
                    continue
                elif cell_type == CellType.FOOD and self.mode == AntMode.TO_FOOD:
                    desired_dir = sample_dir
                    break
                elif self.pos.distance_to(self.colony.pos) < 50 and self.mode == AntMode.TO_HOME:
                    desired_dir = sample_dir
                    break
                elif ph_strength > max_ph_strength:
                    max_ph_strength = ph_strength
                    desired_dir = sample_dir

        random_dir = random.random() * 360 - 180
        desired_dir += random_dir * self.wander_strength
        desired_dir %= 360

        return desired_dir

    def move(self, frame_counter, dt):
        desired_dir = self.determine_desired_dir()
        if (desired_dir - self.angle) % 360 > 180:
            self.angle -= TURN_RATE * dt / 1000
        else:
            self.angle += TURN_RATE * dt / 1000
        self.angle %= 360
        # print(self.angle, desired_dir)
        self.pos += pg.Vector2(SPEED * dt / 1000, 0).rotate(self.angle)
        self.rect.center = self.pos

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
        
        if self.mode == AntMode.TO_FOOD:
            if self.world.is_in_bounds(self.pos):
                coords = self.world.pos_to_coords(self.pos)
                if self.world.get_cell_type(coords) == CellType.FOOD:
                    self.mode = AntMode.TO_HOME
                    self.angle += 180
                    self.timer = 0
        elif self.mode == AntMode.TO_HOME:
            if self.pos.distance_to(self.colony.pos) < 25:
                self.mode = AntMode.TO_FOOD
                self.angle += 180
                self.timer = 0

        img_index = round(self.angle / IMG_ROT_STEP) % IMG_LIST_SIZE
        if self.mode == AntMode.TO_FOOD:
            self.image = Ant.img_no_food_list[img_index]
        else:
            self.image = Ant.img_with_food_list[img_index]

    def update_old(self, frame_counter, dt):
        if frame_counter % PH_DROP_INTERVAL == 0:
            if self.world.is_in_bounds(self.pos):
                coords = self.world.pos_to_coords(self.pos)
                ph_strength = 0.5 ** (self.timer / 5000)
                self.colony.add_pheromone(coords, ph_strength, 1 - self.mode)

        self.move(frame_counter, dt)
        self.timer += dt

    # image must be square
    @staticmethod
    def _rotate_around_center_and_crop(img, angle):
        img_size = img.get_rect().size
        img_rotated = pg.transform.rotate(img, angle)
        crop_offset = (img_rotated.get_rect().width - img_size[0]) // 2
        img_cropped = pg.Surface(img_size, flags=pg.SRCALPHA)
        img_cropped.blit(img_rotated, (0, 0), ((crop_offset, crop_offset), img_size))
        return img_cropped
    

# ===========================


class PheroGrid():
    def __init__(self, bigSize):
        self.surfSize = (int(bigSize[0]/CELL_SIZE), int(bigSize[1]/CELL_SIZE))
        self.image = pg.Surface(self.surfSize).convert()
        self.img_array = np.array(pg.surfarray.array3d(self.image),dtype=float)#.astype(np.float64)
    def update(self, dt):
        self.img_array -= .2 * (60/FPS) * ((dt/10) * FPS) #[self.img_array > 0] # dt might not need FPS parts
        self.img_array = self.img_array.clip(0,255)
        pg.surfarray.blit_array(self.image, self.img_array)
        return self.image


class Food(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pg.Surface((16, 16))
        self.image.fill(0)
        self.image.set_colorkey(0)
        pg.draw.circle(self.image, [20,150,2], [8, 8], 4)
        self.rect = self.image.get_rect(center=pos)
    def pickup(self):
        self.kill()


class Vec2():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	def vint(self):
		return (int(self.x), int(self.y))