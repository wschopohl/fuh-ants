import pygame
import os
import random
import math
import time

# Define Colors in RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
   
# Create Window
pygame.init()

# Set Window Size
WIDTH = 800
HEIGHT = 600

# Set Refresh-rate for the Window
FPS = 60

# Set Caption for the Window
pygame.display.set_caption("Ant Simulation")

# Ant-Image WIDTH and HEIGHT Setting
ANT_IMAGE_WIDTH = 10
ANT_IMAGE_HEIGHT = 15

window = pygame.display.set_mode((WIDTH, HEIGHT))

# Import Ant-Image and resize it
ANT_IMAGE = (pygame.transform.scale(pygame.image.load(os.path.join('Assets','ant.png')), (ANT_IMAGE_WIDTH,ANT_IMAGE_HEIGHT))).convert_alpha()


# MAX Speed
MAX_SPEED = 100

PHEROMONE_TICK = 5



clock = pygame.time.Clock()


class Ant:
    def __init__():
        print("test")

    def update(self):
        last_update_time = time.time()

        # Calculate how long its been since the last update
        current_time = time.time()
        elapsed = current_time - last_update_time
        last_update_time = current_time

        # Trigonometry
        # Calculate random angles for movement
        angle += random.uniform(-0.25, 0.25)
        vel_y = -math.sin(angle) * MAX_SPEED
        vel_x = -math.cos(angle) * MAX_SPEED

        # Update ant position
        ant_pos[0] += vel_x * elapsed
        ant_pos[1] += vel_y * elapsed


class Pheromone:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (BLACK)
        self.thickness = 1

    def display(self):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.size, self.thickness)


def main():

    ant_pos = [WIDTH/2, HEIGHT/2]
    
    pheromone_time = time.time()
    
    angle = 0

    pheromone_positions = []

    ants = []
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # Drawing

        '''START: ADD COLLISION DETECTION USING PYGAME COLLISION FUNCTIONS HERE'''

        # Make sure the ant is not moving out of the window
        if ant_pos[0] <= 0 or ant_pos[0] >= WIDTH:
            ant_pos[0] *= -1

        if ant_pos[1] <= 0 or ant_pos[1] >= HEIGHT:
            ant_pos[1] *= -1

        '''END'''

        # Generate Pheromone-Trails

        position = ant_pos[0], ant_pos[1]
        pheromone_positions.append(position)
       
        window.fill(WHITE)

        ANT_IMAGE_RECT = ANT_IMAGE.get_rect()
          
        ANT_IMAGE_RECT.center = (ant_pos[0], ant_pos[1])

        degrees = - (math.degrees(angle)-90)
        
        ROTATED_ANT_IMAGE = pygame.transform.rotate(ANT_IMAGE, degrees)
        
        window.blit(ROTATED_ANT_IMAGE, ANT_IMAGE_RECT)

        for ant in ants:
            print("test")

        # Draw Pheromone-Trails

        for position in pheromone_positions:
            pygame.draw.circle(window, BLACK, position, 1)

        
    
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
