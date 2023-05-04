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

    def setWorld(self, world):
        self.world = world

    def run(self):
        self.running = True
        self.loopthread = threading.Thread(target=self.loop)
        self.loopthread.start()

    def stop(self):
        self.running = False
        self.loopthread.join()

    def loop(self):
        while self.running:
            self.world.add(Ant(self))
            self.spawned += 1
            if self.spawned >= self.max_ants:
                self.running = False
            time.sleep(1/self.spawn_rate)