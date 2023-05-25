import pygame
import random
import math
import time

from Environment import Environment
from Screen import Screen
screen = Screen(60, 800, 600)

from Ant import Ant
from Pheromone import Pheromone
from Colors import COLORS
from Colony import Colony

elapsed = 0.0

clock = pygame.time.Clock()

def main():
    last_update_time = time.time()
    pheromone_time = time.time()

    pheromone_positions = []
    
    

    environment = Environment()
    colony = Colony (screen, 10)
    
    
    

    run = True
    while run:
        clock.tick(screen.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Calculate how long its been since the last update
        current_time = time.time()
        elapsed = current_time - last_update_time
        last_update_time = current_time

        colony.update(elapsed)


        # Generate Pheromone-Trails
        screen.fill(COLORS.white())

        # Draw Pheromone-Trails

        # Draw Ants
        colony.all_sprites_list.draw(screen.window)
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
