import pygame


class KeyboardController:

    def __init__(self, world):
        pygame.key.set_repeat(1, 200)  # repeat keydown events every 200ms
        self.__world = world

    def tick(self, dt):

        # process all keyboard & window events
        for event in pygame.event.get():
            cont = True
            if event.type == pygame.QUIT:
                cont = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                cont = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__world.pauseresume()
            # don't continue?
            if not cont:
                return False

        return True
