from random import randint
import math
import numpy as np

from Pheromone import Pheromone, Type as PheromoneType
from CollisionPygame import CollisionPygame

import Config

class Ant:
    collision = CollisionPygame()

    def __init__(self, nest):
        self.nest = nest
        self.position = nest.position
        self.direction = randint(0,360)
        self.carry_food = 0
        self.max_carry = 1
        self.step = 0
        self.sprite = None
        self.calculateMoveVectors()

    def setSprite(self, sprite):
        self.sprite = sprite

    def move(self):
        self.position = (self.position[0] + self.dx, self.position[1] + self.dy)
        self.randomChangeDirection()
        self.dropPheromone()

    def turnaround(self):
        self.direction = (self.direction + 180) % 360
        self.calculateMoveVectors()

    def take(self, foodcluster):
        if self.carry_food >= self.max_carry: return
        self.carry_food += foodcluster.take(self.max_carry)
        self.turnaround()
        self.sprite.updateImage()

    def deliver(self, nest):
        if self.carry_food == 0: return
        if self.nest != nest: return # don't deliver to unknown nests
        nest.deliver(self.carry_food)
        self.carry_food = 0
        self.turnaround()
        self.sprite.updateImage()

    def dropPheromone(self):
        if self.step % Config.AntPheromoneDrop != 0: return
        pheromnoe_type = PheromoneType.HOME
        if self.carry_food > 0: pheromnoe_type = PheromoneType.FOOD
        self.nest.world.add(Pheromone(self.position, pheromnoe_type, Config.PheromoneIntensity))

    def randomChangeDirection(self):
        self.step += 1
        if self.step % Config.AntAngleStep != 0: return

        sense_angle = self.sense()
        da = randint(-Config.AntAngleVariation, Config.AntAngleVariation)
        if sense_angle != None:
            self.direction = sense_angle
            
        self.direction = (self.direction + da) % 360

        if self.sprite != None:
            self.sprite.updateImage()

        self.calculateMoveVectors()

    def calculateMoveVectors(self):
        self.dx = Config.AntMoveDistance * math.cos(math.radians(self.direction))
        self.dy = -Config.AntMoveDistance * math.sin(math.radians(self.direction))

    def sense(self):
        pheromone_type = PheromoneType.FOOD
        if self.carry_food > 0: pheromone_type = PheromoneType.HOME

        if pheromone_type == PheromoneType.HOME:
            dnest = calculate_distance(self.position, self.nest.position)
            if dnest <= Config.AntSenseRadius:
                return calculate_angle(self.position, self.nest.position)
            
        if pheromone_type == PheromoneType.FOOD:
            for foodcluster in self.nest.world.foodclusters:
                if foodcluster.amount <= 0: continue
                dfood = calculate_distance(self.position, foodcluster.position)
                if dfood <= Config.AntSenseRadius:
                    return calculate_angle(self.position, foodcluster.position)
        
        near_pheromones = Ant.collision.getNearby(self, self.nest.world.pheromones, Config.AntSenseRadius, pheromone_type.value)
        if len(near_pheromones) == 0: return None
        combined_angle = 0
        angle_count = 0
        for pheromone in near_pheromones:
            angle = (calculate_angle(self.position, pheromone.position))# * pheromone.intensity / Config.PheromoneIntensity)

            if angle != None: 
                if abs(self.direction - angle) < Config.AntFieldOfView:
                    combined_angle += angle
                    angle_count += 1
        
        if angle_count == 0: return None
        return (combined_angle / angle_count)


def calculate_angle(p1, p2):
    dist = calculate_distance(p1, p2)
    if dist < 2: return None

    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    if dx == 0:
        if dy > 0: return 90
        else: return 270
    if dy == 0:
        if dx > 0: return 180
        else: return 0

    deg = math.degrees(math.atan(dy/dx))
    if dx < 0:
        return (deg * -1) % 360
    return (180 - deg) % 360


def calculate_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx*dx + dy*dy)