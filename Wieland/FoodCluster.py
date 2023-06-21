import Config

class FoodCluster:
    def __init__(self, position, amount):
        self.position = position
        self.amount = amount
        self.is_poisoned = False

    def setWorld(self, world):
        self.world = world

    def setSprite(self, sprite):
        self.sprite = sprite

    def size(self):
        return Config.AntFoodSize + self.amount * Config.FoodSize
    
    def take(self, units):
        if self.amount <= 0: return 0
        taken = units
        if self.amount - units < 0: taken = self.amount
        self.amount -= units

        if self.sprite != None:
            self.sprite.update()

        return taken

    def poison(self):
        self.is_poisoned = True
        if self.sprite != None:
            self.sprite.update()