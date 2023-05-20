import pygame
import random
import math
import time


from Screen import Screen
screen = Screen(60, 800, 600)

from Ant import Ant


from Pheromone import Pheromone
from Colors import COLORS





elapsed = 0.0

clock = pygame.time.Clock()




def main():
    last_update_time = time.time()
    pheromone_time = time.time()

    pheromone_positions = []
    ants = []
    
    run = True

    # Anzahl der Ameisen
    for i in range(10):
        ants.append(Ant(screen))

    while run:
        clock.tick(screen.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Calculate how long its been since the last update
        current_time = time.time()
        elapsed = current_time - last_update_time
        last_update_time = current_time

        
        for ant in ants:
            ant.update(elapsed)


            # Make sure the ant is not moving out of the window
            if ant.ant_pos[0] <= 0 or ant.ant_pos[0] >= screen.WIDTH:
                ant.ant_pos[0] *= -1

            if ant.ant_pos[1] <= 0 or ant.ant_pos[1] >= screen.HEIGHT:
             ant.ant_pos[1] *= -1


        # Generate Pheromone-Trails

        '''position = ant.ant_pos[0], ant.ant_pos[1]
        pheromone_positions.append(position)
       '''
        
        screen.fill(COLORS.white())

        

        # Draw Pheromone-Trails

        for position in pheromone_positions:
            pygame.draw.circle(screen.window, COLORS.black(), position, 1)
        
        # Draw Ants
        for ant in ants:
            ant_image = ant.antImage()

            screen.blit(ant_image)
    
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
