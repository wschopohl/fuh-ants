import Config
import math
from Pheromone import Type

class PheromoneMap:
    def __init__(self, world):
        self.world = world
        self.width = math.ceil(world.width / Config.PheromoneMapTileSize)
        self.height = math.ceil(world.height / Config.PheromoneMapTileSize)
        self.map = [[ [None for row in range(self.width)] for col in range(self.height)] for type in range(2)]

    def add(self, pheromone):
        x,y = self.getMapCoordinates(pheromone.position)
        if x >= self.width or y >= self.height: return False
        if x < 0 or y < 0: return False
        if self.map[pheromone.type][y][x] == None:
            self.map[pheromone.type][y][x] = pheromone
            return True
        self.adjustPheromone(self.map[pheromone.type][y][x], pheromone)
        return False
    
    def remove(self, pheromone):
        x,y = self.getMapCoordinates(pheromone.position)
        self.map[pheromone.type][y][x] = None

    def adjustPheromone(self, existing_pheromone, new_pheromone):
        nx = (existing_pheromone.position[0] + new_pheromone.position[0]) / 2
        ny = (existing_pheromone.position[1] + new_pheromone.position[1]) / 2
        existing_pheromone.intensity += new_pheromone.intensity
        existing_pheromone.represents += 1
        existing_pheromone.position = (nx, ny)


    def getMapCoordinates(self, position):
        return (math.floor(position[0] / Config.PheromoneMapTileSize), math.floor(position[1] / Config.PheromoneMapTileSize))