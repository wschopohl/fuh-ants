import Config
import math

class PheromoneMap:
    def __init__(self, world):
        self.world = world
        self.width = math.ceil(world.width / Config.PheromoneMapTileSize)
        self.height = math.ceil(world.height / Config.PheromoneMapTileSize)
        self.map = 