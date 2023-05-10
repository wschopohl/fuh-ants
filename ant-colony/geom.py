from constants import *
import world
import ants

import numpy
import random
import sys
import math
import bresenham

### Constants ###

PROBA = [1/2, 1/4, 1/8, 1/8, 0]
PROBASUM = [0.5, 0.75, 0.875, 1.0, 1.0]
NBTRIES = 5


def distance(pos0, pos1):
    dx = pos1[0] - pos0[0]
    dy = pos1[1] - pos0[1]
    return math.sqrt(dx*dx + dy*dy)


def isValidDir(world, antpos, antdir):
    newpos = world.getNeighbor(antpos, antdir)
    if world.isValidPos(newpos):
        return True
    return False


def targetDir(world, antpos, targetpos):
    if antpos == targetpos:
        return -1
    b = bresenham.bresenham(antpos[0], antpos[1], targetpos[0], targetpos[1])
    nextpos = next(b)
    if(nextpos == antpos):
        nextpos = next(b)
    # find direction
    bestdir = -1
    for direction in world.getNeighbors(antpos, onlyvalid=True, allowblock=False, allowfood=False, returndir=True):
        pos = world.getNeighbor(antpos, direction)
        if nextpos == pos:
            bestdir = direction
            break
    return bestdir


def rotateDir(world, antpos, antdir):
    if antdir == -1:
        return -1
    clockwise = 2 * random.randint(0, 1) - 1
    # r = random.randint(0, 4) # uniform distribution
    p = random.random()
    for r in range(5):
        if(p <= PROBASUM[r]):
            break
    newdir = (antdir + clockwise * r) % NBDIRS
    if isValidDir(world, antpos, newdir):
        return newdir
    return antdir


def randomDir(world, antpos):
    direction = -1
    for _ in range(NBTRIES):
        direction = random.randint(0, NBDIRS-1)
        newpos = world.getNeighbor(antpos, direction)
        if(world.isValidPos(newpos)):
            break
    return direction


def pheromoneDir(world, antpos, homepos, optdist):
    antdist = distance(homepos, antpos)
    maxpheromone = 0
    bestdir = -1
    for direction in world.getNeighbors(antpos, onlyvalid=True, returndir=True):
        neighborpos = world.getNeighbor(antpos, direction)
        pheromone = world.getPheromone(neighborpos)
        neighbordist = distance(homepos, neighborpos)
        if((not optdist) and (pheromone > maxpheromone)):
            maxpheromone = pheromone
            bestdir = direction
        if(optdist and (pheromone > maxpheromone) and (neighbordist > antdist)):
            maxpheromone = pheromone
            bestdir = direction
    return bestdir


def foodDir(world, antpos):
    maxfood = 0
    bestdir = -1
    for direction in world.getNeighbors(antpos, onlyvalid=True, allowfood=True, returndir=True):
        neighborpos = world.getNeighbor(antpos, direction)
        food = world.getFood(neighborpos)
        if(food > maxfood):
            maxfood = food
            bestdir = direction
    return bestdir


def randomTargetPos(world, antpos, mindist=0, maxdist=0):
    if maxdist == 0:
        maxdist = max(world.width(), world.height())
    assert(mindist <= maxdist)
    for _ in range(NBTRIES):
        sx = 2 * random.randint(0, 1) - 1
        sy = 2 * random.randint(0, 1) - 1
        dx = random.randint(mindist, maxdist)
        dy = random.randint(mindist, maxdist)
        if dx != 0 and dy != 0:
            break
    return (antpos[0] + sx*dx, antpos[1] + sy*dy)


def randomPos(world):
    while True:
        x = random.randint(0, world.width()-1)
        y = random.randint(0, world.height()-1)
        if world.isValidPos((x, y)):
            return (x, y)
