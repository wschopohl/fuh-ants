import math
import Screen
import random
import ant_roaming

class Ant:
    def __init__(self, maxSpeed = 100):
        self.ant_pos = [Screen.WIDTH/2, Screen.HEIGHT/2]
        self.maxSpeed = maxSpeed
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0

    # Trigonometry
    def calc(self):
        # Calculate random angles for movement
        self.angle += random.uniform(-0.25, 0.25)
        vel_y = -math.sin(self.angle) * self.maxSpeed
        vel_x = -math.cos(self.angle) * self.maxSpeed

    def update(self):
        # Update ant position
        self.calc()
        Ant.ant_pos[0] += self.vel_x * ant_roaming.elapsed
        Ant.ant_pos[1] += self.vel_y * ant_roaming.elapsed

    def setMaxSpeed(newMaxSpeed):
        Ant.MAX_SPEED = newMaxSpeed