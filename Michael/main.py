import pygame
import random
import math
import time


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
    ants = []
    
    run = True

    colony = Colony (screen, 10)
   

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

        '''position = ant.ant_pos[0], ant.ant_pos[1]
        pheromone_positions.append(position)
       '''
        
        screen.fill(COLORS.white())

        

        # Draw Pheromone-Trails
        '''
        for position in pheromone_positions:
            pygame.draw.circle(screen.window, COLORS.black(), position, 1)
        '''
        # Draw Ants
        
        screen.draw(colony)
    
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
