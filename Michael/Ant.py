import os
import math
import random
import pygame




class Ant(pygame.sprite.Sprite):

    # Ant-Image WIDTH and HEIGHT Setting
    ANT_IMAGE_WIDTH = 20
    ANT_IMAGE_HEIGHT = 30
    

    def __init__(self, sc, colony ,maxSpeed = 100):
        super(Ant, self).__init__()
        # Import Ant-Image and resize it
        self.image = (pygame.transform.scale(pygame.image.load(os.path.join('Assets','ant.png')), (self.ANT_IMAGE_WIDTH,self.ANT_IMAGE_HEIGHT))).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.x = sc.WIDTH/2
        self.rect.y = sc.HEIGHT/2

        self.maxSpeed = maxSpeed
        self.colony = colony
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0


    def antImage(self):
        ANT_IMAGE_RECT = self.rect
          
        ANT_IMAGE_RECT.center = (self.rect.x, self.rect.y)

        degrees = - (math.degrees(self.angle)-90)
        
        ROTATED_ANT_IMAGE = pygame.transform.rotate(self.image, degrees)
        
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
        self.rect.x += self.vel_x * elapsed
        self.rect.y += self.vel_y * elapsed

    def setMaxSpeed(newMaxSpeed):
        Ant.MAX_SPEED = newMaxSpeed

    