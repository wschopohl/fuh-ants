import threading
import time

from Ant import Ant
import Const

class Nest:    
    def __init__(self, position=(100,100), spawn_rate=1, max_ants=Const.Unlimited):
        self.position = position
        self.spawn_rate = spawn_rate
        self.max_ants = max_ants
        self.spawned = 0
        self.food_amount = 0

    def setWorld(self, world):
        self.world = world

    def setSprite(self, sprite):
        self.sprite = sprite

    def deliver(self, amount):
        self.food_amount += amount

    def run(self):
        self.running = True
        self.loopthread = threading.Thread(target=self.loop)
        self.loopthread.start()

    def stop(self):
        self.running = False
        self.loopthread.join()

    def loop(self):
        while self.running:
            if self.spawned < self.max_ants: self.world.add(Ant(self))
            self.spawned += 1
            time.sleep(1/self.spawn_rate)

    def kill(self, ant):
        self.world.remove(ant)
        self.spawned -= 1