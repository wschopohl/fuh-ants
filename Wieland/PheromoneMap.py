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
        self.radius = 90
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
                        self.sens_weight[x,y,0] = 1/((self.radius-x)**2+(y-self.radius)**2)**0.5
                        self.sens_weight[x,y,1] = np.arctan2(-(y-self.radius),(x-self.radius))/np.pi*180
            
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
            self.phero_map -= Config.PheromoneDecay/10
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

        #s1 = np.array(self.sens_weight[max(0,radius-x):min(self.world.width-x,radius)+radius+1,max(0,radius-y):min(self.world.height-y,radius)+radius+1,0])
        #s2 = np.array(self.sens_weight[max(0,radius-x):min(self.world.width-x,radius)+radius+1,max(0,radius-y):min(self.world.height-y,radius)+radius+1,1])
        s1 = np.array(self.sens_weight[mx2:px2,my2:py2,0])
        s2 = np.array(self.sens_weight[mx2:px2,my2:py2,1])
        s2[:,:] = (s2[:,:]-old_angle)%360
        s2 = np.where(s2<180,s2,s2-360)
        s2 = np.where(s2>-70,s2,-70)
        s2 = np.where(s2<70,s2,70)
        #s2 = s2.clip(-70,70)
        s2[:,:] = (70-abs(s2[:,:]))/70
        # s2[:,:] = [x if x<180 else x-360 for x in s2]

        # if old_angle<180:
        #     s2[:,:] = s2[:,:]-old_angle
        #     s2 = s2.clip(-70,70)
        # else:
        #     s2[:,:] = s2[:,:]-old_angle-360
        #     s2 = s2.clip(-70,70)
        #center of mass
        weights = vow[:,:]*s1[:,:]*s2[:,:]
        if len(np.where(weights!=0)[0])== 0:
            return None
        #weights = s2
        #mask_nonzero = weights[np.nonzero(weights[:,:])]
        total_weight = np.sum(weights[:,:])

        x = np.sum(np.array([(i-radius+mx2)*np.sum(weights[i,:]) for i in range(weights.shape[0])]))/total_weight
        y = np.sum(np.array([(i-radius+my2)*np.sum(weights[:,i]) for i in range(weights.shape[1])]))/total_weight

        #new_direction = np.average(mask_nonzero[:,:],axis=None, weights=np.sum(mask_nonzero[:,0]))
        #print(np.arctan2(new_direction[1]-radius+my2,new_direction[0]-radius+mx2)/np.pi*180)
        return np.arctan2(-y,x)/np.pi*180

