import pygame
import Colors
import Config

class EnginePygame:
    def __init__(self):
        pygame.init()

    def setup(self, world):
        self.screen = pygame.display.set_mode([world.width, world.height])
        self.world = world

    def startRenderLoop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the background with white
            self.screen.fill(Colors.Background)
            self.__drawNests()
            self.__drawAnts()


            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

    def __drawNests(self):
        for nest in self.world.nests:
            pygame.draw.circle(self.screen, Colors.Nest, nest.position, Config.NestSize)

    def __drawAnts(self):
        for ant in self.world.ants:
            pygame.draw.circle(self.screen, Colors.Ant, ant.position, Config.AntSize)