from enum import Enum
import math

# class syntax
class Type(Enum):
    HOME = 0
    FOOD = 1

class Pheromone:
    def __init__(self, position, type, intensity):
        self.position = position
        self.type = type.value
        self.intensity = 1
        self.sprite = None
        self.represents = 1
    
    def setWorld(self, world):
        self.world = world

    def setSprite(self, sprite):
        self.sprite = sprite

    def decay(self, amount):
        self.represents -= amount
        if self.represents <= 0: self.represents = 1
        self.intensity -= (amount * math.ceil(self.represents))
        if self.intensity <= 0:
            if self.sprite != None: self.sprite.remove()
            self.world.remove(self)

    def update(self):
        if self.sprite != None: self.sprite.update()
