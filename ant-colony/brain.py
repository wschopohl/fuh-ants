from geom import *
from misc import *

import world
import ants

import random
import numpy
import math

### Constants ###

# MAX_ESCAPE_STEPS = 20
SEARCH_MAX_STEPS = 50
SEARCH_DIST_INC = 1

# ant brain mode
SEARCH = 0
BACK = 1


class Brain:

    def __init__(self, world, colony, ant):
        self.__world = world
        self.__colony = colony
        self.__ant = ant
        self.__mode = SEARCH        # current mode in [SEARCH, BACK, ESCAPE]
        self.__steps = 0            # nb steps done in current mode
        self.__targetpos = None     # set target position
        self.__escape = False       # escape

    def mode(self):
        return self.__mode

    def setMode(self, mode):
        self.__mode = mode
        self.__steps = 0
        self.__targetpos = None

    ### search food ###
    def searchFood(self):
        self.__mode = SEARCH
        direction = -1

        while direction == -1:

            # check neighborhood
            if self.__ant.nearFood():
                self.__targetpos = None
                direction = foodDir(self.__world, self.__ant.getPos())
                debug("I am near food (direction {})".format(strdir(direction)))
            elif self.__ant.onPheromone():
                self.__targetpos = None
                direction = pheromoneDir(self.__world, self.__ant.getPos(),
                                         self.__ant.getHomePos(), True)
                debug("I follow pheromone (direction {})".format(strdir(direction)))
            elif self.__ant.nearPheromone():
                self.__targetpos = None
                direction = pheromoneDir(self.__world, self.__ant.getPos(),
                                         self.__ant.getHomePos(), False)
                debug("I'am near pheromone (direction {})".format(strdir(direction)))

            # try to continue random walk
            if direction == -1 and self.__targetpos:
                direction = targetDir(self.__world, self.__ant.getPos(), self.__targetpos)
                debug("I try to follow my target (direction {})".format(strdir(direction)))

            # setup a new random walk (target reached, blocked, ...)
            if direction == -1:
                self.__targetpos = randomTargetPos(
                    self.__world, self.__ant.getPos(), mindist=0, maxdist=50)
                direction = targetDir(self.__world, self.__ant.getPos(), self.__targetpos)
                debug("I setup a new random target (direction {})".format(strdir(direction)))

        return direction

    ### back home ###
    def backHome(self):
        self.__mode = BACK
        direction = -1

        while direction == -1:

            # set an escape target
            if self.__escape and self.__targetpos == None:
                self.__targetpos = randomTargetPos(
                    self.__world, self.__ant.getPos(), mindist=20, maxdist=50)
                direction = targetDir(self.__world, self.__ant.getPos(), self.__targetpos)
                debug("I setup an escape target (direction {})".format(strdir(direction)))
            # continue escape
            elif self.__escape:
                direction = targetDir(self.__world, self.__ant.getPos(), self.__targetpos)
                debug("I try to follow my escape target (direction {})".format(strdir(direction)))
            # go straightforward to home
            else:
                self.__targetpos = None
                direction = targetDir(self.__world, self.__ant.getPos(), self.__ant.getHomePos())
                debug("I try to go back straightforward to home (direction {})".format(strdir(direction)))

            # check if I need an escape
            if direction == -1 and self.__escape == True:
                self.__targetpos = None
                self.__escape = False
            elif direction == -1 and self.__escape == False:
                self.__targetpos = None
                self.__escape = True

        return direction

    def act(self):

        # seach mode
        if self.__mode == SEARCH:
            direction = self.searchFood()
            if self.__ant.move(direction):
                self.__steps += 1
                if self.__ant.onFood():
                    self.__ant.takeFood()
                    self.setMode(BACK)

        # back mode
        elif self.__mode == BACK:
            direction = self.backHome()
            if self.__ant.move(direction):
                self.__steps += 1
                self.__ant.dropPheromone()
                if self.__ant.atHome():
                    self.__ant.releaseFood()
                    self.setMode(SEARCH)
