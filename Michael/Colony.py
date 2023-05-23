from Ant import Ant
import pygame

class Colony:
    

    def __init__(self, screen ,ant_count = 1):
        self.ants = []
        self.screen = screen
        self.all_sprites_list = pygame.sprite.Group()

        for ant in range (ant_count):
            self.ants.append(Ant(screen,self))
        
        for i in self.ants:
            self.all_sprites_list.add(i)

    def update(self, elapsed):
        self.all_sprites_list.update(elapsed)

        for ant in self.ants:
            ant.update(elapsed)

            # Make sure the ant is not moving out of the window
            # collide = ant.colliderect(self.screen.window.get_rect)
            # if collide:
            #     print("true")



    # Hier könnten Anweisungen an alle ants der colony erfolgen
    
    # Alle Ameisen schwärmen aus und sammeln Essen
    def collect_food():
        pass

    # Alle Ameisen attackieren Angreifer
    def attack():
        pass
    
    # Alle Ameisen verstecken sich im Nest
    def hide():
        pass

    # Neue Ameise erzeugen
    def birth():
        pass

   