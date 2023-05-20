import pygame
import Colors

import numpy as np

class Screen:

#window = None
   # FPS = 60
   # WIDTH = 800
   # HEIGHT = 600

    def __init__(self, FPS=60, WIDTH = 640, HEIGHT = 480, caption = "Ant Simulation"):
        # Create Window
        pygame.init()

        # Set Window Size
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        # Set Refresh-rate for the Window
        self.FPS = FPS

        # Set Caption for the Window
        pygame.display.set_caption("Ant Simulation")

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
       # backgroundImg = pygame.image.load("wallBackground.jpg")


    def fill(self, col):
        self.window.fill(col)
