import pygame
class Screen:

    window = None

    def __init__(self, FPS=60, WIDTH = 800, HEIGHT = 600, caption = "Ant Simulation"):
        # Create Window
        pygame.init()

        # Set Window Size
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        # Set Refresh-rate for the Window
        self.FPS = FPS

        # Set Caption for the Window
        pygame.display.set_caption("Ant Simulation")

        window = pygame.display.set_mode((WIDTH, HEIGHT))
