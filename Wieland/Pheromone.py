from enum import Enum

# class syntax
class Type(Enum):
    HOME = 1
    FOOD = 2

class Pheromone:
    def __init__(self, position, type, intensity):
        self.position = position
        self.type = type.value
        self.intensity = intensity
    
    def setWorld(self, world):
        self.world = world

    def setSprite(self, sprite):
        self.sprite = sprite

    def decay(self, amount):
        self.intensity -= amount
        if self.intensity <= 0:
            if self.sprite != None: self.sprite.remove()
            self.world.remove(self)
