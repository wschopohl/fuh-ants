class TileMemory:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.tiles = []

    def remember(self, coordinates):
        for tile in self.tiles:
            if tile["coordinate"] == coordinates:
                tile["intensity"] *= 0.5
                return
        self.tiles.append({"coordinate":coordinates, "intensity":0.25})
        if(len(self.tiles) > self.maxsize):
            self.tiles.pop(0)

    def intensity(self, coordinates):
        tile = self.get(coordinates)
        if tile != None:
            return tile["intensity"]
        return 0

    def get(self, coordinates):
        for tile in self.tiles:
            if tile["coordinate"] == coordinates:
                return tile
        return None
    
    def reset(self):
        self.tiles = []