from random import randrange
import time

from Nest import Nest
from Ant import Ant
from FoodCluster import FoodCluster
from Pheromone import Pheromone
from CollisionPygame import CollisionPygame
from PheromoneMap import PheromoneMap
from Map import Map
import Config
import ThreadHelper

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nests = []
        self.ants = []
        self.foodclusters = []
        self.pheromones = []
        self.pheromoneMap = PheromoneMap(self)
        self.collision = CollisionPygame()
        self.map = None

    def setup(self, render_engine):
        self.render_engine = render_engine

    def add(self, object):
        if type(object) is Nest:
            object.setWorld(self)
            self.nests.append(object)
            self.render_engine.add(object)
        elif type(object) is Ant:
            self.ants.append(object)
            self.render_engine.add(object)
        elif type(object) is FoodCluster:
            self.foodclusters.append(object)
            self.render_engine.add(object)
        elif type(object) is Pheromone:
            if self.pheromoneMap.add(object) == True:
                object.setWorld(self)
                self.pheromones.append(object)
                self.render_engine.add(object)
        elif type(object) is Map:
            self.map = object
            self.render_engine.add(object)

    def remove(self, object):
        if type(object) is Pheromone:
            self.pheromoneMap.remove(object)
            self.pheromones.remove(object)
            self.render_engine.remove(object)
        if type(object) is Ant:
            self.ants.remove(object)
            object.sprite.kill()

    def run(self):
        for nest in self.nests:
            nest.run()

        ThreadHelper.start("ants", self.antLoop)
        ThreadHelper.start("collisions", self.collisionLoop)
        ThreadHelper.start("pheromones", self.pheromoneLoop)

    def update(self):
        for nest in self.nests: nest.update()
        for ant in self.ants: ant.move()

        self.checkFoodClusterCollision()
        self.checkNestCollision()
        for pheromone in self.pheromones: pheromone.decay(Config.PheromoneDecay)
        if Config.UseNumpy:
            self.pheromoneMap.update()


    def stop(self):
        for nest in self.nests:
            nest.stop()

        ThreadHelper.stop("collisions")
        ThreadHelper.stop("ants")
        ThreadHelper.stop("pheromones")


    def antLoop(self, running):
        while running[0]:
            for ant in self.ants:
                ant.move()
                # ant.sense(self.pheromones)
            time.sleep(Config.AntSleepTime)

    def collisionLoop(self, running):
        while running[0]:
            self.checkFoodClusterCollision()
            self.checkNestCollision()
            time.sleep(Config.AntSleepTime)

    def pheromoneLoop(self, running):
        while running[0]:
            for pheromone in self.pheromones:
                pheromone.decay(Config.PheromoneDecay)
            time.sleep(Config.AntSleepTime)

    def checkFoodClusterCollision(self):
        for foodcluster in self.foodclusters:
            if foodcluster.amount == 0: 
                continue
            ants = self.collision.check(foodcluster, self.ants)
            if ants == []: continue
            for ant in ants: ant.take(foodcluster)

    def checkNestCollision(self):
        for nest in self.nests:
            ants = self.collision.check(nest, self.ants)
            if ants == []: continue
            for ant in ants: ant.deliver(nest)


    def randomPosition(self, margin=0):
        return (randrange(margin, self.width - margin), randrange(margin, self.height - margin))
