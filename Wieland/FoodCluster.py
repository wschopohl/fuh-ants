import Config

class FoodCluster:
    def __init__(self, position, amount):
        self.position = position
        self.amount = amount

    def setWorld(self, world):
        self.world = world

    def setSprite(self, sprite):
        self.sprite = sprite

    def size(self):
        return Config.AntFoodSize + self.amount * Config.FoodSize
    
    def take(self, units):
        taken = units
        if self.amount - units < 0:
            taken = self.amount
        else:
            taken = units
        self.amount -= units

        if self.sprite != None:
            self.sprite.update()

        return taken