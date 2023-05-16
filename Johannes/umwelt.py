import ant
import numpy as np

class umwelt():
    def __init__(self,breite=800,hoehe=600) -> None:
        self.breite = breite
        self.hoehe = hoehe
        self.colonys=[]
        self.food_places=[food()]
        

        self.map = np.ones((self.breite,self.hoehe))
        self.map[1:-1,1:-1] = np.zeros((self.breite-2,self.hoehe-2))
        

    def add_colony(self):
        self.colonys.append(colony(self))

    def update(self):
        for colony in self.colonys:
            colony.update()

class colony():
    def __init__(self,env,pos=(100,100),food=0) -> None:
        self.umwelt = env
        self.pos = pos
        self.ants =[]
        self.food = food
        self.phero = [None,None]
        self.phero[0] = np.zeros((env.breite,env.hoehe),dtype=np.uint8)
        self.phero[1] = np.zeros((env.breite,env.hoehe),dtype=np.uint8)
    def add_ant(self):
        self.ants.append(ant.ant(self))

    def update(self):
        for ant in self.ants:
            ant.update()
        for i,phero in enumerate(self.phero):
            self.phero[i] = phero*0.99
    
    def change_phero(self,ind,val,pos):
        #self.phero[ind][pos[0]-4:pos[0]+4,pos[1]-4:pos[1]+4] =min(max(0, self.phero[ind][pos[0],pos[1]]+val),255)
        self.phero[ind][pos[0]-1:pos[0]+1,pos[1]-1:pos[1]+1] =min(max(0, self.phero[ind][pos[0],pos[1]]+val),255)        

class food:
    def __init__(self,pos=(250,260),amount = 100) -> None:
        self.pos = pos
        self.amount = amount
        
        
if __name__ == "__main__":
    Sim = umwelt()
    Sim.add_colony()


    for i in range(4000):
        for colony in Sim.colonys:
            if len(colony.ants)<100:
                    colony.add_ant()
        Sim.update()
    print(Sim.colonys[0].food)