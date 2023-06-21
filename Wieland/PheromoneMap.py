import Config
import math
from Pheromone import Type
import numpy as np


class PheromoneMap:
    def __init__(self, world):
        self.world = world
        if Config.UseNumpy:
            Config.PheromoneMapTileSize = 3
        self.width = math.ceil(world.width / Config.PheromoneMapTileSize)
        self.height = math.ceil(world.height / Config.PheromoneMapTileSize)
        self.map = [[ [None for row in range(self.width)] for col in range(self.height)] for type in range(3)]
          
        self.radius = 90 # distance of view
        self.aov = 70 # angle of view
        if Config.UseNumpy:
            self.phero_map = np.zeros((world.width,world.height,2))
            self.sens_weight = np.zeros((2*self.radius+1,2*self.radius+1,2))
            #self.sens
            for x in range(self.sens_weight.shape[0]):
                for y in range(self.sens_weight.shape[1]):
                    if x==y==self.radius:
                        self.sens_weight[x,y,0] = 1
                        self.sens_weight[x,y,1] = 0
                    else:
                        self.sens_weight[x,y,0] = 1#1/((self.radius-x)**2+(y-self.radius)**2)**0.5
                        self.sens_weight[x,y,1] = np.arctan2(-(y-self.radius),(x-self.radius))/np.pi*180
            #Sensor 2
            # self.sensor_res = 36
            # self.sens_mask = np.zeros((2*Config.AntSenseRadius+1,2*Config.AntSenseRadius+1,self.sensor_res))
            # for i in range(self.sensor_res):
            #     for x in range(self.sens_mask.shape[0]):
            #         for y in range(self.sens_mask.shape[1]):
            #             angle = abs(np.arctan2(-(y-self.radius),(x-self.radius))/np.pi*180-(360/self.sensor_res*i))
            #             #self.sens_mask[x,y,i] = angle/self.aov if angle < self.aov else 0
            #             self.sens_mask[x,y,i] = 1 if angle < self.aov else 0
                



    def add(self, pheromone):
        
        #numpy
        if Config.UseNumpy:
            x,y = pheromone.position
            self.phero_map[math.floor(pheromone.position[0]),math.floor(pheromone.position[1]),pheromone.type] = max(self.phero_map[math.floor(pheromone.position[0]),math.floor(pheromone.position[1]),pheromone.type],pheromone.intensity)
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
            self.phero_map = self.phero_map.clip(min=0)

    
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
        radius = self.radius#Config.AntSenseRadius
        x,y = position
        x = math.floor(x)
        y = math.floor(y)
        mx = max(math.floor(x-radius),0)
        px = min(self.world.width,x+radius+1)
        my = max(math.floor(y-radius),0)
        py = min(self.world.height,y+radius+1)
        vow = self.phero_map[mx:px,my:py,type]
        if len(np.where(vow!=0)[0]) == 0:
            return None

        mx2 = radius+mx-x
        px2 = radius+px-x
        my2 = radius+my-y
        py2 = radius+py-y

        s1 = np.array(self.sens_weight[mx2:px2,my2:py2,0])
        #sensor 1
        s2 = np.array(self.sens_weight[mx2:px2,my2:py2,1])
        s2[:,:] = (s2[:,:]-old_angle)%360
        s2 = np.where(s2<180,s2,s2-360)
        s2 = np.where(s2>-self.aov,s2,-self.aov)
        s2 = np.where(s2<self.aov,s2,self.aov)
        
        s2[:,:] = (self.aov-abs(s2[:,:]))/self.aov
        
        #sensor 2
        #s2 = self.sens_mask[mx2:px2,my2:py2,int(old_angle//(360//self.sensor_res)%self.sensor_res)]
        
        
        #center of mass
        weights = vow[:,:]*s1[:,:]*s2[:,:]
        if len(np.where(weights!=0)[0])== 0:
            return None
        total_weight = np.sum(weights[:,:])
        if total_weight <1:
            return None
        x = np.sum(np.array([(i-radius+mx2)*np.sum(weights[i,:]) for i in range(weights.shape[0])]))/total_weight
        y = np.sum(np.array([(i-radius+my2)*np.sum(weights[:,i]) for i in range(weights.shape[1])]))/total_weight

        return np.arctan2(-y,x)/np.pi*180

