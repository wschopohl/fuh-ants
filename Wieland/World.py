from random import randrange
import threading
import time

from Nest import Nest
from Ant import Ant
from FoodCluster import FoodCluster
from Pheromone import Pheromone
import Config
import ThreadHelper
import Collision

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nests = []
        self.ants = []
        self.foodclusters = []
        self.pheromones = []

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
            self.pheromones.append(object)
        
    def run(self):
        for nest in self.nests:
            nest.run()
        
        ThreadHelper.start("ants", self.antLoop)
        ThreadHelper.start("collisions", self.collisionLoop)

    def stop(self):
        for nest in self.nests:
            nest.stop()

        ThreadHelper.stop("collisions")
        ThreadHelper.stop("ants")


    def antLoop(self, running):
        while running[0]:
            for ant in self.ants:
                ant.move()
        
            time.sleep(Config.AntSleepTime)

    def collisionLoop(self, running):
        while running[0]:
            for nest in self.nests:
                ants = Collision.check(nest, self.ants)

    def randomPosition(self, margin=0):
        return (randrange(margin, self.width - margin), randrange(margin, self.height - margin))
