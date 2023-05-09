import math
import Screen
import random
import ant_roaming

class Ant:
    def __init__(self, maxSpeed = 100):
        self.ant_pos = [Screen.WIDTH/2, Screen.HEIGHT/2]
        self.maxSpeed = maxSpeed
        self.angle = 0

    # Trigonometry
    # Calculate random angles for movement
    angle += random.uniform(-0.25, 0.25)
    vel_y = -math.sin(self.angle) * maxSpeed
    vel_x = -math.cos(self.angle) * self.maxSpeed

    def update():
        # Update ant position
        Ant.ant_pos[0] += vel_x * ant_roaming.elapsed
        Ant.ant_pos[1] += vel_y * ant_roaming.elapsed

    def setMaxSpeed(newMaxSpeed):
        Ant.MAX_SPEED = newMaxSpeed