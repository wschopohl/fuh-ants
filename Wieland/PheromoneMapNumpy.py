import Config
import math
from Pheromone import Type
import numpy as np


class PheromoneMapNumpy:
    def __init__(self, world):
        self.world = world
        
        self.width = math.ceil(world.width / Config.PheromoneMapTileSizeNumpy)
        self.height = math.ceil(world.height / Config.PheromoneMapTileSizeNumpy)       
        
        self.phero_map = np.zeros((self.width, self.height,len(Type)))
        self.sense_radius = math.floor(Config.AntSenseRadiusNumpy / Config.PheromoneMapTileSizeNumpy)
        self.sens_weight = np.zeros((2*self.sense_radius+1,2*self.sense_radius+1,2))

        self.maxIntensity = [1 for i in range(len(Type))]

        for x in range(self.sens_weight.shape[0]):
            for y in range(self.sens_weight.shape[1]):
                if x==y==self.sense_radius:
                    self.sens_weight[x,y,0] = 1
                    self.sens_weight[x,y,1] = 0
                else:
                    self.sens_weight[x,y,0] = 1#1/((Config.AntSenseRadiusNumpy-x)**2+(y-Config.AntSenseRadiusNumpy)**2)**0.5
                    self.sens_weight[x,y,1] = np.arctan2(-(y-self.sense_radius),(x-self.sense_radius))/np.pi*180
                

    def add(self, pheromone):
        x,y = self.getMapCoordinates(pheromone.position)
        self.phero_map[x,y,pheromone.type] += pheromone.intensity

    def remove(self, pheromone):
        x,y = self.getMapCoordinates(pheromone.position)
        self.phero_map[x,y,pheromone.type] = 0
        
    def decay(self):
        self.phero_map -= Config.PheromoneDecay
        self.phero_map = self.phero_map.clip(min=0)

    def removeAllAt(self, position):
        mx,my = self.getMapCoordinates(position)
        size = int(Config.PheromoneEraserSize / Config.PheromoneMapTileSize)
        xl = max(mx - size, 0)
        xh = min(mx + size, self.width-1)
        yl = max(my - size, 0)
        yh = min(my + size, self.height-1)
        self.phero_map[xl:xh,yl:yh,:] = 0

    def getMapCoordinates(self, position):
        return (math.floor(position[0] / Config.PheromoneMapTileSizeNumpy), math.floor(position[1] / Config.PheromoneMapTileSizeNumpy))
    
    def sensor(self,position,old_angle,type):
        x,y = self.getMapCoordinates(position)
        mx = max(x-self.sense_radius,0)
        px = min(self.width,x+self.sense_radius+1)
        my = max(y-self.sense_radius,0)
        py = min(self.height,y+self.sense_radius+1)
        nearby = self.phero_map[mx:px,my:py,type]
        if len(np.where(nearby!=0)[0]) == 0:
            return None

        mx2 = self.sense_radius+mx-x
        px2 = self.sense_radius+px-x
        my2 = self.sense_radius+my-y
        py2 = self.sense_radius+py-y

        # s1 = np.array(self.sens_weight[mx2:px2,my2:py2,0])
        # sensor 1
        s2 = np.array(self.sens_weight[mx2:px2,my2:py2,1])
        s2[:,:] = (s2[:,:]-old_angle)%360
        s2 = np.where(s2<180,s2,s2-360)
        s2 = np.where(s2>-Config.AntFieldOfViewNumpy,s2,-Config.AntFieldOfViewNumpy)
        s2 = np.where(s2<Config.AntFieldOfViewNumpy,s2,Config.AntFieldOfViewNumpy)
        
        s2[:,:] = (Config.AntFieldOfViewNumpy-abs(s2[:,:]))/Config.AntFieldOfViewNumpy
        
        #center of mass
        weights = nearby[:,:]*s2[:,:]
        if len(np.where(weights!=0)[0])== 0:
            return None
        total_weight = np.sum(weights[:,:])
        if total_weight <1:
            return None
        x = np.sum(np.array([(i-self.sense_radius+mx2)*np.sum(weights[i,:]) for i in range(weights.shape[0])]))/total_weight
        y = np.sum(np.array([(i-self.sense_radius+my2)*np.sum(weights[:,i]) for i in range(weights.shape[1])]))/total_weight

        return np.arctan2(-y,x)/np.pi*180


    def updatePixelArray(self, pixel_array):
        return
        for y in range(self.height):
            for x in range(self.width):
                for type in range(len(Type)):
                    if self.maxIntensity[type] < self.phero_map[x,y,type]: self.maxIntensity[type] = self.phero_map[x,y,type]
                    pixel_array[x,y] = 1024
