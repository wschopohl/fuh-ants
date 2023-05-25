import pygame
import Colors
HEROMONE_TICK = 5

class Pheromone:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (Colors.BLACK)
        self.thickness = 1

    #def display(window):
    #    pygame.draw.circle(window, self.colour, (self.x, self.y), self.size, self.thickness)