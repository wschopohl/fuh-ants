from random import randint
import math

from Pheromone import Pheromone, Type as PheromoneType

import Config

class Ant:
    def __init__(self, nest):
        self.nest = nest
        self.position = nest.position
        self.direction = randint(0,360)
        self.carry_food = 0
        self.max_carry = 1
        self.step = 0
        self.sprite = None
        self.randomChangeDirection(True)

    def setSprite(self, sprite):
        self.sprite = sprite

    def move(self):
        self.position = (self.position[0] + self.dx, self.position[1] + self.dy)
        self.randomChangeDirection()
        self.dropPheromone()

    def take(self, foodcluster):
        if self.carry_food >= self.max_carry: return
        self.carry_food += 1
        foodcluster.take(1)
        self.sprite.updateImage()

    def deliver(self, nest):
        if self.carry_food == 0: return
        if self.nest != nest: return # don't deliver to unknown nests
        nest.deliver(self.carry_food)
        self.carry_food = 0
        self.sprite.updateImage()

    def dropPheromone(self):
        if self.step % Config.AntPheromoneDrop != 0: return
        pheromnoe_type = PheromoneType.HOME
        if self.carry_food > 0: pheromnoe_type = PheromoneType.FOOD
        self.nest.world.add(Pheromone(self.position, pheromnoe_type, Config.PheromoneIntensity))

    def randomChangeDirection(self, now=False):
        self.step += 1
        if not now and self.step % Config.AntAngleStep != 0: return
        
        da = randint(-Config.AntAngleVariation, Config.AntAngleVariation)
        self.direction = (self.direction + da) % 360

        if self.sprite != None:
            self.sprite.updateImage()

        self.dx = Config.AntMoveDistance * math.cos(math.radians(self.direction))
        self.dy = -Config.AntMoveDistance * math.sin(math.radians(self.direction))