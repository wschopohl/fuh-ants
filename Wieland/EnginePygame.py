import pygame
from Ant import Ant
from Nest import Nest
from FoodCluster import FoodCluster
from Pheromone import Pheromone
from Map import Map
from CollisionPygame import CollisionPygame
import Colors
import Config

import threading
import time
import math

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
        self.pgpheromones = []
        self.pheromone_surface = pygame.Surface((world.width, world.height), pygame.SRCALPHA)
        self.pheromone_update_step = 0
        self.pgmap = None
        self.debug_surface = pygame.Surface((world.width, world.height), pygame.SRCALPHA)
        self.draw_surface = pygame.Surface((world.width, world.height), pygame.SRCALPHA)
        self.collision = CollisionPygame()
        self.running = True
        # used for Michaels User Code
        class UserInteraction:
            pass
        self.user_interaction = UserInteraction()
        self.user_interaction.active_foodcluster = None

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
        if type(object) is Pheromone:
            pgpheromone = PGPheromone(object)
            self.pgpheromones.append(pgpheromone)
        if type(object) is Map:
            self.pgmap = PGMap(object)
    
    def remove(self, object):
        if type(object) is Pheromone:
            self.pgpheromones.remove(object.sprite)

    def handleUserInteraction(self):
        LEFT = 1
        RIGHT = 2
        
        if self.user_interaction.active_foodcluster != None:
            amount = int((time.time() - self.user_interaction.click_time_start) * 500)
            self.user_interaction.active_foodcluster.amount = amount
            self.user_interaction.active_foodcluster.sprite.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # left mousebutton = food placement
                if event.button == LEFT and not self.pgmap.mask.get_at(pygame.mouse.get_pos()) :
                    self.user_interaction.active_foodcluster = FoodCluster(position = pygame.mouse.get_pos(), amount=1)
                    self.user_interaction.click_time_start = time.time()
                    self.world.add(self.user_interaction.active_foodcluster)

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[RIGHT]:
                    if pygame.key.get_pressed()[pygame.K_d]:
                        self.pgmap.draw_circle(pygame.mouse.get_pos(), (0,0,0,0), 20)
                    else:
                        self.pgmap.draw_circle(pygame.mouse.get_pos(), Colors.UserWalls, 10)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == LEFT:
                    self.user_interaction.active_foodcluster = None
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    mouse_pos = pygame.mouse.get_pos()
                    for foodcluster in self.world.foodclusters:
                        # print(math.sqrt((foodcluster.position[0] - mouse_pos[0]) ** 2
                        #              + (foodcluster.position[1] - mouse_pos[1]) ** 2))
                        if math.sqrt((foodcluster.position[0] - mouse_pos[0]) ** 2
                                     + (foodcluster.position[1] - mouse_pos[1]) ** 2) <= foodcluster.size():
                            foodcluster.poison()

    def drawPheromones(self):
        self.pheromone_update_step += 1
        if self.pheromone_update_step % 1 == 0:
            maxIntensity = 1
            self.pheromone_surface.fill((0,0,0,0))
            for pgpheromone in self.pgpheromones:
                if pgpheromone.pheromone.intensity > maxIntensity:
                    maxIntensity = pgpheromone.pheromone.intensity
                pgpheromone.draw(self.pheromone_surface)

            Pheromone.maxIntensity = maxIntensity

        self.screen.blit(self.pheromone_surface, (0,0))


    def startRenderLoop(self):
        clock = pygame.time.Clock()
        while self.running:
                
            self.handleUserInteraction()

            if not Config.UseThreading: self.world.update()
            
            self.pgants.update()
            
            self.screen.fill(Colors.Background)
            
            renderMutex.acquire()
            self.drawPheromones()
            if self.pgmap != None: self.pgmap.draw(self.screen)
            # self.screen.blit(self.debug_surface, (0,0))
            self.pgnests.draw(self.screen)
            self.pgfoodclusters.draw(self.screen)
            self.pgants.draw(self.screen)
            self.printNestStats()
            self.printDescription()
           
            renderMutex.release()            
            
            pygame.display.flip()
            # self.debug_surface.fill((255,255,255,0))
            if Config.UseThreading: time.sleep(Config.AntSleepTime)
            else: clock.tick(120)

        if Config.UseThreading: self.world.stop()
        pygame.quit()

    def printNestStats(self):
        text = "Nest Food: "
        for idx, nest in enumerate(self.world.nests):
            text += "["+ str(idx) + "]: " + str(nest.food_amount) + " "
        text += " Pheromones: " + str(len(self.pgpheromones))
        text_surface = self.font.render(text, True, Colors.InfoText)
        self.screen.blit(text_surface, (20, 20))

    def printDescription(self):
        text = " Press + hold left mousebutton for food placement."
        text2 = " Press + hold right mousebutton for wall placement."
        text3 = " Point with mouse + press \"d\" for deleting walls."

        text_surface = self.font.render(text, True, Colors.Description)
        text_surface2 = self.font.render(text2, True, Colors.Description)
        text_surface3 = self.font.render(text3, True, Colors.Description)

        self.screen.blit(text_surface, (20, self.world.height-20))
        self.screen.blit(text_surface2, (20, self.world.height-40))
        self.screen.blit(text_surface3, (20, self.world.height-60))

        

    def drawVector(self, start, end):
        pygame.draw.line(self.draw_surface, (255,0,0,255), start, end)
        pygame.draw.circle(self.draw_surface, (0,255,0,255), start, 2)
        self.draw_surface.set_alpha(200)
        self.debug_surface.blit(self.draw_surface, (0,0))
        self.draw_surface.blit(self.debug_surface, (0,0))


class PGAnt(pygame.sprite.Sprite):
    original_image = None
    original_image_food = None
    original_image_poisoned_food = None
    original_mask_image = None
    middle_offset = None

    @classmethod
    def loadImages(cls):
        if PGAnt.original_image != None: return
        PGAnt.original_image = pygame.image.load(Config.AntImageFile).convert_alpha()
        PGAnt.original_mask_image = pygame.image.load(Config.AntViewMaskFile).convert_alpha()
        PGAnt.original_image_food = PGAnt.original_image.copy()
        pygame.draw.circle(PGAnt.original_image_food, Colors.FoodCluster, Config.AntFoodPosition, Config.AntFoodSize)
        PGAnt.original_image_poisoned_food = PGAnt.original_image.copy()
        pygame.draw.circle(PGAnt.original_image_poisoned_food, Colors.FoodClusterPoisoned, Config.AntFoodPosition, Config.AntFoodSize)
        image_rect = PGAnt.original_image.get_rect()
        PGAnt.middle_offset = pygame.Vector2(image_rect.width / 2 - Config.AntMiddlePosition[0], image_rect.height / 2 - Config.AntMiddlePosition[1])
    
    def __init__(self, ant):
        pygame.sprite.Sprite.__init__(self)
        self.ant = ant
        self.object = ant
        self.radius = 2
        ant.setSprite(self)
        PGAnt.loadImages()
        self.updateImage()
    
    def update(self):
        renderMutex.acquire()
        try:
            self.rect.x = self.ant.position[0] - self.rect.width / 2 + self.middle.x
            self.rect.y = self.ant.position[1] - self.rect.height / 2 - self.middle.y
        except AttributeError:
            pass
        renderMutex.release()

    def updateImage(self):
        renderMutex.acquire()
        deg = (self.ant.direction)
        self.image = PGAnt.original_image
        if self.ant.carry_food > 0:
            if not self.ant.is_poisoned:
                self.image = pygame.transform.rotate(PGAnt.original_image_food, deg)
            else:
                self.image = pygame.transform.rotate(PGAnt.original_image_poisoned_food, deg)
        else:    
            self.image = pygame.transform.rotate(PGAnt.original_image, deg)
        self.mask = pygame.mask.from_surface(pygame.transform.rotate(PGAnt.original_mask_image, deg))
        self.rect = self.image.get_rect()
        self.middle = PGAnt.middle_offset.rotate(self.ant.direction)
        renderMutex.release()


class PGNest(pygame.sprite.Sprite):
    def __init__(self, nest):
        pygame.sprite.Sprite.__init__(self)
        self.nest = nest
        self.radius = Config.NestSize
        nest.setSprite(self)
        self.image = pygame.image.load(Config.NestImageFile).convert_alpha()
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
        if self.foodcluster.amount <= 0: self.kill()
        self.image = pygame.Surface((self.foodcluster.size()*2, self.foodcluster.size()*2), pygame.SRCALPHA)   # per-pixel alpha
        if not self.foodcluster.is_poisoned:
            color = Colors.FoodCluster
        else:
            color = Colors.FoodClusterPoisoned
        pygame.draw.circle(self.image, color, (self.foodcluster.size(), self.foodcluster.size()), self.foodcluster.size())    
        self.radius = self.foodcluster.size() # little hack because of oversized ant masks for view
        self.rect = self.image.get_rect()
        self.rect.x = self.foodcluster.position[0] - self.rect.width / 2
        self.rect.y = self.foodcluster.position[1] - self.rect.height / 2

class PGPheromone():
    def __init__(self, pheromone):
        self.pheromone = pheromone
        pheromone.setSprite(self)

    def draw(self, surface):
        color = self.pheromone.type
        size = Config.PheromoneSize + Config.PheromoneMapTileSize * self.pheromone.intensity / Pheromone.maxIntensity
        pygame.draw.circle(surface, Colors.PheromoneColors[color], self.pheromone.position, size)


class PGMap(pygame.sprite.Sprite):
    def __init__(self, map_obj):
        self.original_image = pygame.image.load(map_obj.image).convert_alpha()
        self.image = pygame.Surface((self.original_image.get_width(), self.original_image.get_height()), pygame.SRCALPHA)
        self.draw_surface = pygame.Surface((self.original_image.get_width(), self.original_image.get_height()), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.compose()
        map_obj.setSprite(self)

    def update(self):
        pass

    def compose(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.original_image, (0,0))
        self.image.blit(self.draw_surface, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_circle(self, position, color, radius):
        pygame.draw.circle(self.draw_surface, color, position, radius)
        self.compose()

   


        
