from random import randint
import math
import numpy as np

from Pheromone import Pheromone, Type
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
        self.pheromone_intensity = 1
        self.sprite = None
        self.calculateMoveVectors()

    def setSprite(self, sprite):
        self.sprite = sprite

    def move(self):
        self.pheromone_intensity -= (Config.PheromoneDecay / 2)
        self.step += 1
        self.position = (self.position[0] + self.dx, self.position[1] + self.dy)
        self.randomChangeDirection()
        self.dropPheromone()

    def turnaround(self):
        self.direction = (self.direction + 180) % 360
        self.calculateMoveVectors()

    def take(self, foodcluster):
        if self.carry_food >= self.max_carry: return
        self.pheromone_intensity = 1
        self.carry_food += foodcluster.take(self.max_carry)
        self.turnaround()
        self.sprite.updateImage()

    def deliver(self, nest):
        if self.nest != nest: return # don't deliver to unknown nests
        self.pheromone_intensity = 1
        if self.carry_food == 0: return
        nest.deliver(self.carry_food)
        self.carry_food = 0
        # self.turnaround()
        self.position = self.nest.position
        self.direction = randint(0,360)
        self.sprite.updateImage()

    def dropPheromone(self):
        if self.step % Config.AntPheromoneDrop != 0: return
        if self.pheromone_intensity <= 0: return
        pheromnoe_type = Type.HOME if self.carry_food == 0 else Type.FOOD
        self.nest.world.add(Pheromone(self.position, pheromnoe_type, self.pheromone_intensity))

    def randomChangeDirection(self):
        if self.step % Config.AntAngleStep != 0: return

        sense_angle = self.sense()
        da = randint(-Config.AntAngleVariation, Config.AntAngleVariation)
        if sense_angle != None:
            self.direction = (sense_angle + da * 1) % 360
        else:   
            self.direction = (self.direction + da) % 360

        if self.sprite != None:
            self.sprite.updateImage()

        self.calculateMoveVectors()

    def calculateMoveVectors(self):
        self.dx = Config.AntMoveDistance * math.cos(math.radians(self.direction))
        self.dy = -Config.AntMoveDistance * math.sin(math.radians(self.direction))

    def sense(self):
        pheromone_type = Type.FOOD if self.carry_food == 0 else Type.HOME

        # if near to nest ignore pheromones and go directly in direction of nest
        if pheromone_type == Type.HOME:
            dnest = calculate_distance(self.position, self.nest.position)
            if dnest <= Config.AntSenseRadius:
                return fast_angle(self.position[0] - self.nest.position[0], self.position[1] - self.nest.position[1])
            
        # if near to food ignore pheromones and go directly in direction of food
        if pheromone_type == Type.FOOD:
            for foodcluster in self.nest.world.foodclusters:
                if foodcluster.amount <= 0: continue
                dfood = calculate_distance(self.position, foodcluster.position)
                if dfood <= Config.AntSenseRadius:
                    return fast_angle(self.position[0] - foodcluster.position[0], self.position[1] - foodcluster.position[1])
        
        near_pheromones = Ant.collision.getNearby(self, self.nest.world.pheromones, Config.AntSenseRadius, pheromone_type.value)
        
        return self.calculate_pheromone_vector(near_pheromones)

    def calculate_pheromone_vector(self, pheromones):
        if len(pheromones) == 0: return None

        vector = {'x': 0, 'y': 0}
        for p in pheromones:
            dx = self.position[0] - p.position[0]
            dy = self.position[1] - p.position[1]
            length = math.sqrt(dx*dx + dy*dy)
            if length <= Config.AntSenseRadius:
                angle = fast_angle(dx, dy)
                if angle != None and abs(angle - self.direction) <= Config.AntFieldOfView:
                    angle_factor = (1 - abs(angle - self.direction) / Config.AntFieldOfView)
                    length_factor = 1 # (1 - length / Config.AntSenseRadius)
                    vector['x'] += (dx * p.intensity * length_factor * angle_factor)
                    vector['y'] += (dy * p.intensity * length_factor * angle_factor)
        
        if vector['x'] == 0 == vector['y']: return None
        return fast_angle(vector['x'], vector['y'])


def calculate_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx*dx + dy*dy)

def fast_angle(dx, dy):
    if dx == 0 == dy: return None
    if dx == 0:
        if dy > 0: return 90
        else: return 270
    a = math.degrees(math.atan(dy/-dx))
    if dx > 0: return (180 + a) % 360
    return a % 360