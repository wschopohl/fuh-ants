from random import randint
import math

from Pheromone import Pheromone, Type

import Config

class Ant:
    killCounter = 0

    def __init__(self, nest):
        self.nest = nest
        self.position = nest.position
        self.direction = randint(0,360)
        self.carry_food = 0
        self.max_carry = 1
        self.step = 0
        self.pheromone_intensity = 1
        self.sprite = None
        self.wallSearchStart = randint(0,1)
        self.calculateMoveVectors()

        self.nextRandomSteeringUpdate = 0

        self.is_poisoned = False
        self.poisoning_time = 0

    def setSprite(self, sprite):
        self.sprite = sprite

    def move(self):
        self.pheromone_intensity -= (Config.PheromoneDecay * Config.PheromoneDistanceReduce)
        self.step += 1
        self.position = (self.position[0] + self.dx, self.position[1] + self.dy)
        if self.is_poisoned and self.step > self.poisoning_time + Config.AntPoisonedLifespan:
            self.suicide()
        else:
            # self.randomChangeDirection_unmodified()
            self.randomChangeDirection()
            self.dropPheromone()

    def turnaround(self):
        self.direction = (self.direction + 180) % 360
        self.calculateMoveVectors()

    def take(self, foodcluster):
        if self.carry_food >= self.max_carry: return
        self.pheromone_intensity = 1
        self.carry_food += foodcluster.take(self.max_carry)
        if foodcluster.is_poisoned:
            self.is_poisoned = True
            self.poisoning_time = self.step
        self.turnaround()
        self.sprite.updateImage()

    def deliver(self, nest):
        if self.nest != nest: return # don't deliver to unknown nests
        self.pheromone_intensity = 1
        if self.carry_food == 0: return
        nest.deliver(self.carry_food)
        self.carry_food = 0
        # self.turnaround()
        self.position = self.nest.position
        self.direction = randint(0,360)
        self.calculateMoveVectors()

    def dropPheromone(self):
        if self.step % Config.AntPheromoneDrop != 0: return
        if self.pheromone_intensity <= 0: return
        if self.carry_food > 0:
            if not self.is_poisoned:
                pheromone_type = Type.FOOD
            else:
                pheromone_type = Type.POISON
        else:
            pheromone_type = Type.HOME
        self.nest.world.add(Pheromone(self.position, pheromone_type, self.pheromone_intensity))

    # old version left for reference
    def randomChangeDirection_wieland_original(self):
        # ants are allowed to walk outside the window a little bit, but are steered back soon after
        if self.position[0] < -50 or self.position[0] > self.nest.world.width + 50 or self.position[1] < -50 or self.position[1] > self.nest.world.height + 50:
            self.direction = (fast_angle(self.position[0] - self.nest.world.width / 2, self.position[1] - self.nest.world.height / 2)) % 360
        if self.step % Config.AntAngleStep != 0: return

        sense_angle = self.sense()
        
        da = randint(-Config.AntAngleVariation, Config.AntAngleVariation)
        if sense_angle != None:
            self.direction = (sense_angle + da * 0.2) % 360
        else:   
            self.direction = (self.direction + da) % 360

        self.calculateMoveVectors()
        if self.sprite != None: self.sprite.updateImage()
    
    # updated version by lennart, that introduces more randomness
    def randomChangeDirection(self):
        # ants are allowed to walk outside the window a little bit, but are steered back soon after
        if self.position[0] < -50 or self.position[0] > self.nest.world.width + 50 or self.position[1] < -50 or self.position[1] > self.nest.world.height + 50:
            self.direction = (fast_angle(self.position[0] - self.nest.world.width / 2, self.position[1] - self.nest.world.height / 2)) % 360
        if self.step % Config.AntAngleStep != 0: return

        if not self.is_poisoned:
            sense_angle = self.sense()
        else:
            sense_angle = None

        if  self.step >= self.nextRandomSteeringUpdate:
            self.randomSteering = randint(-Config.AntAngleVariation, Config.AntAngleVariation)
            self.nextRandomSteeringUpdate += Config.AntAngleStep * randint(Config.RandomSteeringUpdateIntervalMin, Config.RandomSteeringUpdateIntervalMax)
        if sense_angle != None:
            self.direction = (sense_angle + self.randomSteering * Config.RandomSteeringWeight) % 360
        else:   
            self.direction = (self.direction + self.randomSteering) % 360

        self.calculateMoveVectors()
        if self.sprite != None: self.sprite.updateImage()

    def calculateMoveVectors(self):
        olddirection = self.direction
        search_angle = 0
        search_invert = (1 if self.wallSearchStart == 0 else -1)
        iteration = 0
        while True:
            if self.sprite == None: break
            if self.nest.world.map == None: break
            future_x = self.position[0] + Config.AntMoveDistance * Config.AntAngleStep * math.cos(math.radians(self.direction))
            future_y = self.position[1] -Config.AntMoveDistance * Config.AntAngleStep * math.sin(math.radians(self.direction))
            if self.nest.world.collision.checkPointMask((future_x, future_y), self.nest.world.map.sprite) == False: break
            if iteration % 2 == 0: 
                search_angle += Config.AntWallSearchAngle
                self.direction = (olddirection + (search_angle * search_invert)) % 360
            else:
                self.direction = (olddirection + (search_angle * search_invert * -1)) % 360
            iteration += 1
            if iteration > 24: 
                self.suicide()
                return
        self.dx = Config.AntMoveDistance * math.cos(math.radians(self.direction))
        self.dy = -Config.AntMoveDistance * math.sin(math.radians(self.direction))

    def suicide(self):
        Ant.killCounter += 1
        print("Ants killed:", Ant.killCounter)
        self.nest.kill(self)

    def sense(self):
        pheromone_type = Type.FOOD if self.carry_food == 0 else Type.HOME

        # if near to nest ignore pheromones and go directly in direction of nest
        if pheromone_type == Type.HOME:
            dnest = calculate_distance(self.position, self.nest.position)
            # print(self.nest.radius)
            if dnest <= Config.AntSenseRadius + Config.NestSize:
                return fast_angle(self.position[0] - self.nest.position[0], self.position[1] - self.nest.position[1])
            
        # if near to food ignore pheromones and go directly in direction of food
        if pheromone_type == Type.FOOD:
            for foodcluster in self.nest.world.foodclusters:
                if foodcluster.amount <= 0: continue
                dfood = calculate_distance(self.position, foodcluster.position)
                if dfood <= Config.AntSenseRadius + Config.NestSize:
                    return fast_angle(self.position[0] - foodcluster.position[0], self.position[1] - foodcluster.position[1])
        if Config.UseNumpy:
            return self.nest.world.pheromoneMap.numpy_sensor(self.position,self.direction,pheromone_type.value)

        poison_angle = self.calculate_pheromone_vector(Config.AntSenseRadiusPoisonPheromones, Type.POISON.value)
        if poison_angle is None:
            # no poison pheromones => follow food/home pheromones
            angle = self.calculate_pheromone_vector(Config.AntSenseRadius, pheromone_type.value)
        elif (poison_angle - self.direction) % 360 <= Config.AntFieldOfView:
            # poison pheromones on right side => turn as far left as possible
            angle = (self.direction - Config.AntFieldOfView) % 360
        else:
            # poison pheromones on left side => turn as far right as possible
            angle = (self.direction + Config.AntFieldOfView) % 360

        return angle

    def calculate_pheromone_vector(self, radius, type):
        pheromones = self.nest.world.pheromoneMap.getNearby(self.position, radius, type)
        if len(pheromones) == 0: return None

        vector = {'x': 0, 'y': 0}
        for p in pheromones:
            dx = self.position[0] - p.position[0]
            dy = self.position[1] - p.position[1]
            length = math.sqrt(dx*dx + dy*dy)
            if length <= radius:
                angle = fast_angle(dx, dy)
                if angle == None: continue
                angle_delta = 180 - abs(abs(angle - self.direction) - 180)
                if angle_delta <= Config.AntFieldOfView:
                    angle_factor = (1 - angle_delta / (Config.AntFieldOfView))
                    length_factor = 1 #(1 - length / radius) # distance factor not so important
                    vector['x'] += (dx * p.intensity * length_factor * angle_factor)
                    vector['y'] += (dy * p.intensity * length_factor * angle_factor)

        if vector['x'] == 0 == vector['y']: return None
        return fast_angle(vector['x'], vector['y'])
    
    # slices the total field of view into three equal circle sectors and returns an angle pointing towards the 
    # center of the sector containing the highest total pheromone intensity
    # code that lennart brought in, currently not used but kept for reference
    def calculate_pheromone_vector_in_sectors(self, pheromones):
        if len(pheromones) == 0: return None

        # vector = {'x': 0, 'y': 0}
        score_middle, score_left, score_right = 0, 0, 0
        for p in pheromones:
            dx = self.position[0] - p.position[0]
            dy = self.position[1] - p.position[1]
            length = math.sqrt(dx*dx + dy*dy)
            if length <= Config.AntSenseRadius:
                angle = fast_angle(dx, dy)
                if angle is None:
                    continue
                angle_delta = (angle - self.direction) % 360
                # middle sensor
                if angle_delta <= 1/3 * Config.AntFieldOfView or angle_delta >= 360 - 1/3 * Config.AntFieldOfView:
                    score_middle += p.intensity
                # left sensor
                elif angle_delta < 360 - 1/3 * Config.AntFieldOfView and angle_delta >= 360 - Config.AntFieldOfView:
                    score_left += p.intensity
                # right sensor
                elif angle_delta > 1/3 * Config.AntFieldOfView and angle_delta <= Config.AntFieldOfView:
                    score_right += p.intensity
        
        if score_middle + score_left + score_right <= 0:
            return None
        elif score_middle >= score_left and score_middle >= score_right:
            return self.direction
        elif score_left >= score_right:
            return (self.direction - 2/3 * Config.AntFieldOfView) % 360
        else:
            return (self.direction + 2/3 * Config.AntFieldOfView) % 360

def calculate_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx*dx + dy*dy)

def fast_angle(dx, dy):
    if dx == 0 == dy: return None
    if dx == 0:
        if dy > 0: return 90
        else: return 270
    a = math.degrees(math.atan(dy/-dx))
    if dx > 0: return (180 + a) % 360
    return a % 360
