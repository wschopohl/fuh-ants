import pygame

window = None

def init():
    # Create Window
    pygame.init()

    # Set Window Size
    WIDTH = 800
    HEIGHT = 600

    # Set Refresh-rate for the Window
    FPS = 60

    # Set Caption for the Window
    pygame.display.set_caption("Ant Simulation")

    window = pygame.display.set_mode((WIDTH, HEIGHT))
