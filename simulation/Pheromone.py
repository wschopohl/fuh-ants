from enum import Enum
import math

# class syntax
class Type(Enum):
    HOME = 0
    FOOD = 1
    POISON = 2

class Pheromone:
    maxIntensity = 1

    def __init__(self, position, type, intensity):
        self.position = position
        self.type = type.value
        self.intensity = intensity
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
            self.remove()

    def remove(self):
        self.world.remove(self)


    def update(self):
        if self.sprite != None: self.sprite.update()
