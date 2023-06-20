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
        self.pgpheromones = pygame.sprite.Group()
        self.pgmap = None
        self.debug_surface = pygame.Surface((world.width, world.height), pygame.SRCALPHA)
        self.draw_surface = pygame.Surface((world.width, world.height), pygame.SRCALPHA)
        self.collision = CollisionPygame()
        self.running = True
        # used for Michaels User Code
        class UserInteraction:
            pass
        self.user_interaction = UserInteraction() 

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
            self.pgpheromones.add(pgpheromone)
        if type(object) is Map:
            self.pgmap = PGMap(object)

    def handleUserInteraction(self):
        LEFT = 1
        RIGHT = 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # left mousebutton = food placement
                if event.button == LEFT:
                    # activate timer and get mouse position
                    self.user_interaction.x, self.user_interaction.y = pygame.mouse.get_pos()
                    self.user_interaction.click_time_start = time.time()

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[RIGHT]:
                    if pygame.key.get_pressed()[pygame.K_d]:
                        self.pgmap.draw_circle(pygame.mouse.get_pos(), (0,0,0,0), 20)
                    else:
                        self.pgmap.draw_circle(pygame.mouse.get_pos(), Colors.UserWalls, 10)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == LEFT:
                    # Get mousebutton release time and calculate clickduration
                    click_time_stop = time.time()
                    click_duration = click_time_stop - self.user_interaction.click_time_start
                    x,y = self.user_interaction.x, self.user_interaction.y
                    # add food according click duration
                    # add only when mouseposition is in the mask of the map


                    pos_in_mask = x - self.pgmap.rect.x, y - self.pgmap.rect.x
                    touching = self.pgmap.rect.collidepoint(x,y) and self.pgmap.mask.get_at(pos_in_mask) 

                    if touching: break
                    
                    if (int(click_duration*300)) > Config.MaxUserFoodSize:
                        self.world.add(FoodCluster(position = (x,y), amount=(int(Config.MaxUserFoodSize))))

                    else:
                        self.world.add(FoodCluster(position=(x, y), amount=int(click_duration * 300)))
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    mouse_pos = pygame.mouse.get_pos()
                    for foodcluster in self.world.foodclusters:
                        # print(math.sqrt((foodcluster.position[0] - mouse_pos[0]) ** 2
                        #              + (foodcluster.position[1] - mouse_pos[1]) ** 2))
                        if math.sqrt((foodcluster.position[0] - mouse_pos[0]) ** 2
                                     + (foodcluster.position[1] - mouse_pos[1]) ** 2) <= foodcluster.size():
                            foodcluster.poison()


    def startRenderLoop(self):
        render_step = 0

        clock = pygame.time.Clock()
        while self.running:
            render_step += 1
                
            self.handleUserInteraction()

            if not Config.UseThreading: self.world.update()
            
            self.pgants.update()
            if render_step % 5 == 0: self.pgpheromones.update()
            
            self.screen.fill(Colors.Background)
            
            renderMutex.acquire()
            # TODO: Maybe optimize to not draw the lines every time
            if self.pgmap != None: self.pgmap.draw(self.screen)
            # self.screen.blit(self.debug_surface, (0,0))
            self.pgnests.draw(self.screen)
            self.pgfoodclusters.draw(self.screen)
            self.pgpheromones.draw(self.screen)
            self.pgants.draw(self.screen)
            # for ant in self.pgants:
            #     pygame.draw.circle(self.screen, (0,0,0,40), ant.ant.position, Config.AntSenseRadius, 1)
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

class PGPheromone(pygame.sprite.Sprite):
    pheromone_images = {}
    
    @classmethod
    def loadImages(cls):
        if PGPheromone.pheromone_images:
            return
        for color in Colors.PheromoneColors:
            tmp_image = pygame.Surface((Config.PheromoneSize*2, Config.PheromoneSize*2), pygame.SRCALPHA)   # per-pixel alpha
            pygame.draw.circle(tmp_image, Colors.PheromoneColors[color], (Config.PheromoneSize, Config.PheromoneSize), Config.PheromoneSize)
            PGPheromone.pheromone_images[color] = tmp_image
    
    def __init__(self, pheromone):
        pygame.sprite.Sprite.__init__(self)
        PGPheromone.loadImages()
        self.pheromone = pheromone
        pheromone.setSprite(self)
        self.image = PGPheromone.pheromone_images[pheromone.type].copy()
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        intensity = (self.pheromone.intensity / 10 * 225) + 20
        # size = (5 / 10) * self.pheromone.intensity
        # self.image = pygame.transform.scale(PGPheromone.pheromone_images[self.pheromone.type], (size, size))
        self.rect.x = self.pheromone.position[0] - self.rect.width / 2
        self.rect.y = self.pheromone.position[1] - self.rect.height / 2
        self.image.set_alpha(intensity)

    def remove(self):
        self.kill()

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

   


        
