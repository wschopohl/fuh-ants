import Config

class FoodCluster:
    def __init__(self, position, amount):
        self.position = position
        self.amount = amount

    def setWorld(self, world):
        self.world = world

    def size(self):
        return self.amount * Config.FoodSize