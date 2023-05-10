from constants import *
import world
import brain
import random
import numpy
import math


class Ant:

    def __init__(self, world, colony):
        self.__world = world
        self.__colony = colony
        self.__pos = colony.getPos()
        self.__brain = brain.Brain(world, colony, self)
        self.__food = 0

    def getBrain(self):
        return self.__brain

    def getPos(self):
        return self.__pos

    def getFood(self):
        return self.__food

    def move(self, direction):
        if direction == -1:
            return False
        newpos = self.__world.getNeighbor(self.__pos, direction)
        if not self.__world.isValidPos(newpos):
            return False
        self.__pos = newpos
        return True

    def onFood(self):
        return (self.__world.getFood(self.__pos) > 0)

    def onPheromone(self):
        return (self.__world.getPheromone(self.__pos) > 0)

    def nearFood(self):
        for pos in self.__world.getNeighbors(self.__pos, onlyvalid=True):
            if self.__world.getFood(pos) > 0:
                return True
        return False

    def nearPheromone(self):
        for pos in self.__world.getNeighbors(self.__pos, onlyvalid=True):
            if self.__world.getPheromone(pos) > 0:
                return True
        return False

    def atHome(self):
        return (self.__pos == self.__colony.getPos())

    def getHomePos(self):
        return self.__colony.getPos()

    def takeFood(self):
        if(self.__food < FOOD_CAPACITY and self.onFood()):
            available = self.__world.getFood(self.__pos)
            need = FOOD_CAPACITY - self.__food
            self.__food = min(available, need)
            self.__world.removeFood(self.__pos, self.__food)
            return True
        return False

    def releaseFood(self):
        if(self.__food > 0 and self.atHome()):
            self.__colony.addFood(self.__food)
            self.__food = 0
            return True
        return False

    def dropPheromone(self):
        self.__world.addPheromone(self.__pos, PHEROMONE_DROP/2)
        for pos in self.__world.getNeighbors(self.__pos, onlyvalid=True):
            self.__world.addPheromone(pos, PHEROMONE_DROP/16)

    def update(self, dt):
        self.__brain.act()

### Class Colony ###


class Colony:

    def __init__(self, world, pos, color="blue"):
        self.__world = world
        self.__color = color
        self.__pos = pos
        self.__ants = []
        self.__food = 0

    def getPos(self):
        return self.__pos

    def getFood(self):
        return self.__food

    def addFood(self, level=1):
        self.__food += level

    def getAnts(self):
        return self.__ants

    def addAnt(self):
        ant = Ant(self.__world, self)
        self.__ants.append(ant)
        return ant

    def addAnts(self, nb):
        for _ in range(nb):
            self.addAnt()

    def getColor(self):
        return self.__color

    def update(self, dt):
        for ant in self.__ants:
            ant.update(dt)
