import Config
import math
from Pheromone import Type
import numpy as np

class PheromoneMap:
    def __init__(self, world):
        self.world = world
        self.width = math.ceil(world.width / Config.PheromoneMapTileSize)
        self.height = math.ceil(world.height / Config.PheromoneMapTileSize)
        self.map = [[ [None for row in range(self.width)] for col in range(self.height)] for type in range(2)]
        if Config.UseNumpy:
            self.phero_map = np.zeros((world.width,world.height,2))



    def add(self, pheromone):
        
        #numpy
        if Config.UseNumpy:
            x,y = pheromone.position
            self.phero_map[math.floor(pheromone.position[0]),math.floor(pheromone.position[0]),pheromone.type] += pheromone.intensity
        #old
        x,y = self.getMapCoordinates(pheromone.position)
        if x >= self.width or y >= self.height: return False
        if x < 0 or y < 0: return False
        if self.map[pheromone.type][y][x] == None:
            self.map[pheromone.type][y][x] = pheromone
            return True
        self.adjustPheromone(self.map[pheromone.type][y][x], pheromone)
        return False
    
    def remove(self, pheromone):
        #numpy
        if Config.UseNumpy:
            x,y = pheromone.position
            self.phero_map[math.floor(pheromone.position[0]),math.floor(pheromone.position[0]),pheromone.type] = 0
        #old
        x,y = self.getMapCoordinates(pheromone.position)
        self.map[pheromone.type][y][x] = None
    def update(self):
        if Config.UseNumpy:
            self.phero_map -= Config.PheromoneDecay
            self.phero_map.clip(min=0)

    
    def adjustPheromone(self, existing_pheromone, new_pheromone):
        ifactor = (new_pheromone.intensity / (new_pheromone.intensity + existing_pheromone.intensity))
        dx = (new_pheromone.position[0] - existing_pheromone.position[0]) * ifactor
        dy = (new_pheromone.position[1] - existing_pheromone.position[1]) * ifactor
        
        nx = (existing_pheromone.position[0] + dx)
        ny = (existing_pheromone.position[1] + dy)
        
        existing_pheromone.intensity += new_pheromone.intensity
        existing_pheromone.represents += 1
        existing_pheromone.position = (nx, ny)


    def getMapCoordinates(self, position):
        return (math.floor(position[0] / Config.PheromoneMapTileSize), math.floor(position[1] / Config.PheromoneMapTileSize))
    
    def getNearby(self, position, radius, type):
        x,y = self.getMapCoordinates(position)
        tiles = math.ceil(radius / Config.PheromoneMapTileSize)
        pheromones = []
        for my in range(y-tiles,y+tiles):
            for mx in range(x-tiles,x+tiles):
                if(mx >= self.width or my >= self.height): continue
                if(mx < 0 or my < 0): continue
                if(self.map[type][my][mx] != None):
                    pheromones.append(self.map[type][my][mx])
        return pheromones
    
    def numpy_sensor(self,position,radius,old_angle):
        #numpy
        x,y = position
        vow = self.phero_map[int(x-radius):int(x+radius),int(y-radius):int(y+radius),type]