import pygame
import os
import random
import math
import time

import Ant
import Pheromone
import Colors
import Screen

s = Screen()

# Ant-Image WIDTH and HEIGHT Setting
ANT_IMAGE_WIDTH = 20
ANT_IMAGE_HEIGHT = 30

elapsed = 0.0

# Import Ant-Image and resize it
ANT_IMAGE = (pygame.transform.scale(pygame.image.load(os.path.join('Assets','ant.png')), (ANT_IMAGE_WIDTH,ANT_IMAGE_HEIGHT))).convert_alpha()


clock = pygame.time.Clock()

def main():
    
    
    last_update_time = time.time()
    pheromone_time = time.time()

    pheromone_positions = []
    
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

        

        Ant.update()

        # Drawing

        '''START: ADD COLLISION DETECTION USING PYGAME COLLISION FUNCTIONS HERE'''

        # Make sure the ant is not moving out of the window
        if Ant.ant_pos[0] <= 0 or Ant.ant_pos[0] >= Screen.WIDTH:
            Ant.ant_pos[0] *= -1

        if Ant.ant_pos[1] <= 0 or Ant.ant_pos[1] >= Screen.HEIGHT:
            Ant.ant_pos[1] *= -1

        '''END'''

        # Generate Pheromone-Trails

        position = Ant.ant_pos[0], Ant.ant_pos[1]
        pheromone_positions.append(position)
       
        Screen.window.fill(Colors.WHITE)

        ANT_IMAGE_RECT = ANT_IMAGE.get_rect()
          
        ANT_IMAGE_RECT.center = (Ant.ant_pos[0], Ant.ant_pos[1])

        degrees = - (math.degrees(Ant.angle)-90)
        
        ROTATED_ANT_IMAGE = pygame.transform.rotate(ANT_IMAGE, degrees)
        
        Screen.window.blit(ROTATED_ANT_IMAGE, ANT_IMAGE_RECT)

        # Draw Pheromone-Trails

        for position in pheromone_positions:
            pygame.draw.circle(Screen.window, Colors.BLACK, position, 1)

        
    
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
