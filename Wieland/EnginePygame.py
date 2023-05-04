import pygame
from Ant import Ant
from Nest import Nest
from FoodCluster import FoodCluster
import Colors
import Config

import math
import threading
import time

renderMutex = threading.Lock()

class EnginePygame:
    def __init__(self):
        pygame.init()

    def setup(self, world):
        self.screen = pygame.display.set_mode([world.width, world.height])
        pygame.display.set_caption("MAS - Multi Agent System")
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
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
            
            renderMutex.acquire()
            self.pgnests.draw(self.screen)
            self.pgfoodclusters.draw(self.screen)
            self.pgants.draw(self.screen)
            self.printNestStats()
            renderMutex.release()
            
            pygame.display.flip()
            time.sleep(Config.AntSleepTime)

        self.world.stop()
        pygame.quit()

    def printNestStats(self):
        text = "Nest Food: "
        for idx, nest in enumerate(self.world.nests):
            text += "["+ str(idx) + "]: " + str(nest.food_amount) + " "
        text_surface = self.font.render(text, True, Colors.InfoText)
        self.screen.blit(text_surface, (20, 20))


class PGAnt(pygame.sprite.Sprite):
    original_image = None
    original_image_food = None

    @classmethod
    def loadImages(cls):
        if PGAnt.original_image != None: return
        PGAnt.original_image = pygame.image.load(Config.AntImageFile).convert_alpha()
        PGAnt.original_image_food = PGAnt.original_image.copy()
        pygame.draw.circle(PGAnt.original_image_food, Colors.FoodCluster, Config.AntFoodPosition, Config.AntFoodSize)
    
    def __init__(self, ant):
        pygame.sprite.Sprite.__init__(self)
        self.ant = ant
        self.object = ant
        ant.setSprite(self)
        PGAnt.loadImages()
        self.updateImage()
    
    def update(self):
        self.rect.x = self.ant.position[0] - self.rect.width / 2
        self.rect.y = self.ant.position[1] - self.rect.height / 2

    def updateImage(self):
        deg = (self.ant.direction) -90
        self.image = PGAnt.original_image
        renderMutex.acquire()
        if self.ant.carry_food > 0:
            self.image = pygame.transform.rotate(PGAnt.original_image_food, deg)
        else:    
            self.image = pygame.transform.rotate(PGAnt.original_image, deg)
        renderMutex.release()
        self.rect = self.image.get_rect()


class PGNest(pygame.sprite.Sprite):
    def __init__(self, nest):
        pygame.sprite.Sprite.__init__(self)
        self.nest = nest
        nest.setSprite(self)
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
        foodcluster.setSprite(self)
        self.update()
    
    def update(self):
        self.image = pygame.Surface((self.foodcluster.size()*2, self.foodcluster.size()*2), pygame.SRCALPHA)   # per-pixel alpha
        pygame.draw.circle(self.image, Colors.FoodCluster, (self.foodcluster.size(), self.foodcluster.size()), self.foodcluster.size())
        self.rect = self.image.get_rect()
        self.rect.x = self.foodcluster.position[0] - self.rect.width / 2
        self.rect.y = self.foodcluster.position[1] - self.rect.height / 2