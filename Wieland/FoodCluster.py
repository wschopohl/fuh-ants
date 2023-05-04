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
        return self.amount * Config.FoodSize
    
    def take(self, units):
        taken = units
        if self.amount - units < 0:
            taken = self.amount
            self.amount = 0
        else:
            self.amount -= units
        
        if self.sprite != None:
            self.sprite.update()

        return taken