from random import randrange
import threading
import time

from Nest import Nest
from Ant import Ant
from Pheromone import Pheromone
import Config

Unlimited = -1
RandomPosition = -1

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nests = []
        self.ants = []
        self.pheromones = []

    def add(self, object):
        object.setWorld(self)
        if type(object) is Nest:
            self.nests.append(object)
        elif type(object) is Ant:
            self.ants.append(object)
        elif type(object) is Pheromone:
            self.pheromones.append(object)
        
    def run(self):
        for nest in self.nests:
            nest.run()
        
        self.startAntThread()

    def stop(self):
        for nest in self.nests:
            nest.stop()

        self.stopAntThread()

    def startAntThread(self):
        self.running = True
        self.ant_thread = threading.Thread(target=self.antLoop)
        self.ant_thread.start()


    def stopAntThread(self):
        self.running = False
        self.ant_thread.join()


    def antLoop(self):
        while self.running:
            for ant in self.ants:
                ant.move()
        
            time.sleep(Config.AntSleepTime)

    def randomPosition(self, margin=0):
        return (randrange(margin, self.width - margin), randrange(margin, self.height - margin))
