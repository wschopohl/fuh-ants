from constants import *
import ants

import numpy
import random


class World:

    # initialize world
    def __init__(self, width, height):
        self.__pause = False
        self.__width = width
        self.__height = height
        self.__block = numpy.zeros((height, width), dtype=int)
        self.__food = numpy.zeros((height, width), dtype=int)
        self.__pheromone = numpy.zeros((height, width), dtype=int)
        self.__colonies = []
        print("=> create new world {}x{}".format(width, height))

    def pauseresume(self):
        if self.__pause:
            self.__pause = False
        else:
            self.__pause = True

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def getNeighbor(self, pos, direction):
        return (pos[0] + DIRS[direction][0], pos[1] + DIRS[direction][1])

    def getNeighbors(self, pos, shuffle=False, onlyvalid=False, allowblock=False, allowfood=True, returndir=False):
        neighbors = []
        for direction in range(NBDIRS):
            neighborpos = self.getNeighbor(pos, direction)
            if onlyvalid and not self.isValidPos(neighborpos, allowblock, allowfood):
                continue
            if returndir:
                neighbors.append(direction)     # add neighbor direction
            else:
                neighbors.append(neighborpos)   # add neighbor position
        if shuffle:
            random.shuffle(neighbors)
        return neighbors

    def isValidPos(self, pos, allowblock=False, allowfood=True):
        # check position is valid
        if pos[0] >= self.__width or pos[0] < 0 or pos[1] >= self.__height or pos[1] < 0:
            return False
        # check block
        if allowblock == False and self.isBlock(pos):
            return False
        # check food
        if allowfood == False and (self.getFood(pos) > 0):
            return False
        return True

    def isBlock(self, pos):
        if self.__block[pos[1]][pos[0]] == 0:
            return False
        return True

    def getFood(self, pos):
        return self.__food[pos[1]][pos[0]]

    def getPheromone(self, pos):
        return self.__pheromone[pos[1]][pos[0]]

    def addBlock(self, pos, dim):
        posx = pos[0]
        posy = pos[1]
        for y in range(dim[1]):
            for x in range(dim[0]):
                self.__block[posy + y][posx + x] = 1
        print("=> add block at position ({},{}) of dimension ({},{})".format(
            pos[0], pos[1], dim[0], dim[1]))

    def addFood(self, pos, dim=(1, 1), level=1):
        if dim is None:
            dim = (10, 10)
        for y in range(dim[1]):
            for x in range(dim[0]):
                self.__food[pos[1] + y][pos[0] + x] += level
        print("=> add food at position ({},{}) of dimension ({},{})".format(
            pos[0], pos[1], dim[0], dim[1]))

    def removeFood(self, pos, level=1):
        self.__food[pos[1]][pos[0]] -= level
        if self.__food[pos[1]][pos[0]] < 0:
            self.__food[pos[1]][pos[0]] = 0

    def addPheromone(self, pos, level):
        x = pos[0]
        y = pos[1]
        self.__pheromone[y][x] += level
        if self.__pheromone[y][x] > MAX_PHEROMONE:
            self.__pheromone[y][x] = MAX_PHEROMONE

    def decayPheromone(self):
        for y in range(self.__height):
            for x in range(self.__width):
                self.__pheromone[y][x] -= DECAY_PHEROMONE
                if self.__pheromone[y][x] <= 0:
                    self.__pheromone[y][x] = 0

    # def decayPheromone2(self):
    #     for cell in numpy.nditer(self.__pheromone, op_flags=['readwrite']):
    #         cell -= DECAY_PHEROMONE
    #         if cell <= 0:
    #             cell = 0

    def getColonies(self):
        return self.__colonies

    def addColony(self, pos, nbants, color):
        print("=> add colony {} of {} ants at position ({},{})".format(
            color, nbants, pos[0], pos[1]))
        colony = ants.Colony(self, pos, color)
        colony.addAnts(nbants)
        self.__colonies.append(colony)
        return colony

    # update world at each clock tick
    def update(self, dt):
        self.decayPheromone()
        if self.__pause:
            return
        for colony in self.__colonies:
            colony.update(dt)
