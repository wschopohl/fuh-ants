import pygame
from Ant import Ant
from Nest import Nest
from FoodCluster import FoodCluster
import Colors
import Config

import math

class EnginePygame:
    def __init__(self):
        pygame.init()

    def setup(self, world):
        self.screen = pygame.display.set_mode([world.width, world.height])
        pygame.display.set_caption("MAS - Multi Agent System")
        self.world = world
        self.pgants = pygame.sprite.Group()
        self.pgnests = pygame.sprite.Group()
        self.pgfoodclusters = pygame.sprite.Group()

    def add(self, object):
        if type(object) is Ant:
            pgant = PGAnt(object)
            self.pgants.add(pgant)
        if type(object) is Nest:
            pgnest = PGNest(object)
            self.pgnests.add(pgnest)
        if type(object) is FoodCluster:
            pgfoodcluster = PGFoodCluster(object)
            self.pgfoodclusters.add(pgfoodcluster)
        
    def startRenderLoop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.pgants.update()
            
            self.screen.fill(Colors.Background)
            
            self.pgnests.draw(self.screen)
            self.pgfoodclusters.draw(self.screen)
            self.pgants.draw(self.screen)
            

            pygame.display.flip()

        self.world.stop()
        pygame.quit()



class PGAnt(pygame.sprite.Sprite):
    original_image = None
    
    def __init__(self, ant):
        pygame.sprite.Sprite.__init__(self)
        self.ant = ant
        ant.setSprite(self)
        if PGAnt.original_image == None:
            PGAnt.original_image = pygame.image.load(Config.AntImageFile).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.updateRotation()
    
    def update(self):
        self.rect.x = self.ant.position[0] - self.rect.width / 2
        self.rect.y = self.ant.position[1] - self.rect.height / 2

    def updateRotation(self):
        deg = (self.ant.direction) -90
        self.image = pygame.transform.rotate(PGAnt.original_image, deg)


class PGNest(pygame.sprite.Sprite):
    def __init__(self, nest):
        pygame.sprite.Sprite.__init__(self)
        self.nest = nest
        self.image = pygame.Surface((Config.NestSize*2, Config.NestSize*2), pygame.SRCALPHA)   # per-pixel alpha
        pygame.draw.circle(self.image, Colors.Nest, (Config.NestSize, Config.NestSize), Config.NestSize)
        self.rect = self.image.get_rect()
        self.update()
    
    def update(self):
        self.rect.x = self.nest.position[0] - self.rect.width / 2
        self.rect.y = self.nest.position[1] - self.rect.height / 2


class PGFoodCluster(pygame.sprite.Sprite):
    def __init__(self, foodcluster):
        pygame.sprite.Sprite.__init__(self)
        self.foodcluster = foodcluster
        self.image = pygame.Surface((foodcluster.size()*2, foodcluster.size()*2), pygame.SRCALPHA)   # per-pixel alpha
        pygame.draw.circle(self.image, Colors.FoodCluster, (foodcluster.size(), foodcluster.size()), foodcluster.size())
        self.rect = self.image.get_rect()
        self.update()
    
    def update(self):
        self.rect.x = self.foodcluster.position[0] - self.rect.width / 2
        self.rect.y = self.foodcluster.position[1] - self.rect.height / 2