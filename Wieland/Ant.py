from random import randint
import math

import Config

class Ant:
    def __init__(self, nest):
        self.nest = nest
        self.direction = math.radians(randint(0,360))
        self.position = nest.position
        self.step = 0

    def move(self):
        dx = Config.AntMoveDistance * math.cos(self.direction)
        dy = Config.AntMoveDistance * math.sin(self.direction)
        self.position = (self.position[0] + dx, self.position[1] + dy)
        self.randomChangeDirection()

    def randomChangeDirection(self):
        self.step += 1
        if self.step < Config.AntAngleStep:
            return
        self.step = 0
        da = math.radians(randint(-Config.AntAngleVariation, Config.AntAngleVariation))
        self.direction += da