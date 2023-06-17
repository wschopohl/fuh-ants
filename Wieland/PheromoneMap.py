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
            self.sens_weight = np.zeros((2*Config.AntSenseRadius+1,2*Config.AntSenseRadius+1,2))
            #self.sens
            for x in range(self.sens_weight.shape[0]):
                for y in range(self.sens_weight.shape[1]):
                    self.sens_weight[x,y,0] = ((x-Config.AntSenseRadius)**2+(y-Config.AntSenseRadius)**2)**0.5/Config.AntSenseRadius
                    self.sens_weight[x,y,1] = np.arctan2((y-Config.AntSenseRadius),(x-Config.AntSenseRadius))/np.pi*180
            
            # sensor_res = 36
            # self.sens_mask = np.zeros((2*Config.AntSenseRadius+1,2*Config.AntSenseRadius+1,sensor_res))
            # for i in sensor_res:
            #     for x in range(self.sens_mask.size[0]):
            #         for y in range(self.sens_mask.size[1]):
            #             self.sens_mask[x,y,i]
                



    def add(self, pheromone):
        
        #numpy
        if Config.UseNumpy:
            x,y = pheromone.position
            self.phero_map[math.floor(pheromone.position[0]),math.floor(pheromone.position[1]),pheromone.type] += pheromone.intensity
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
            self.phero_map[math.floor(pheromone.position[0]),math.floor(pheromone.position[1]),pheromone.type] = 0
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
    
    def numpy_sensor(self,position,old_angle,type):
        #numpy
        radius = Config.AntSenseRadius
        x,y = position
        
        vow = self.phero_map[math.floor(x-radius):math.floor(x+radius),math.floor(y-radius):math.floor(y+radius),type]
        self.sens_weight[0]*self.sens_weight[1]
