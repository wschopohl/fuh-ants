import os
import math
import random
import pygame




class Ant:
    # Ant-Image WIDTH and HEIGHT Setting
    ANT_IMAGE_WIDTH = 20
    ANT_IMAGE_HEIGHT = 30
    # Import Ant-Image and resize it
    ANT_IMAGE = (pygame.transform.scale(pygame.image.load(os.path.join('Assets','ant.png')), (ANT_IMAGE_WIDTH,ANT_IMAGE_HEIGHT))).convert_alpha()
    
    def __init__(self, sc ,maxSpeed = 100):
        self.ant_pos = [sc.WIDTH/2, sc.HEIGHT/2]
        self.maxSpeed = maxSpeed
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0

    def antImage(self):
        ANT_IMAGE_RECT = self.ANT_IMAGE.get_rect()
          
        ANT_IMAGE_RECT.center = (self.ant_pos[0], self.ant_pos[1])

        degrees = - (math.degrees(self.angle)-90)
        
        ROTATED_ANT_IMAGE = pygame.transform.rotate(self.ANT_IMAGE, degrees)
        
        ant_img = [ROTATED_ANT_IMAGE, ANT_IMAGE_RECT]
        return ant_img
    
    # Trigonometry
    def calc(self):
        # Calculate random angles for movement
        self.angle += random.uniform(-0.25, 0.25)
        self.vel_y = -math.sin(self.angle) * self.maxSpeed
        self.vel_x = -math.cos(self.angle) * self.maxSpeed

    def update(self, elapsed):
        # Update ant position
        self.calc()
        self.ant_pos[0] += self.vel_x * elapsed
        self.ant_pos[1] += self.vel_y * elapsed

    def setMaxSpeed(newMaxSpeed):
        Ant.MAX_SPEED = newMaxSpeed

    