import numpy as np
import random

def mask_array(arr,rot):
    pass
    return arr

def get_neighborhood(map,pos,sensor_weite):
    return map[int(pos[0])-sensor_weite:int(pos[0])+sensor_weite,
                                   int(pos[1])-sensor_weite:int(pos[1])+sensor_weite]
        
    pass

def simple_sensor(map):
    pos = [(7,4),(7,7),(4,7),(1,7),(1,4),(1,1),(4,1),(7,1)]
    return [np.sum(get_neighborhood(map,x,4)) for x in pos]
            
def dis_pos(a,b):
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def f_logistic(x,G,k,f0):
    return G/(1+np.exp(-k*G*x)*((G/f0)-1))

class ant():
    def __init__(self, colony, pos=(120, 100), rot=45, name='', vis_obj=None, 
                 geschwindigkeit=1) -> None:
        self.pos = pos
        self.colony = colony
        self.umwelt = colony.umwelt
        self.rotation = rot
        self.geschwindigkeit = geschwindigkeit 
        self.name = name
        self.vis_obj = vis_obj
        self.sensor_weite = 10 #"sichtweise" in pixel
        self.trage_obj = None
        self.count_event=0
        

    def update(self):

        # sensor
        #Futter in der naehe?
        if not self.trage_obj:
            for food in self.umwelt.food_places:
                if dis_pos(food.pos,self.pos) <20:
                    self.trage_obj = True
                    food.amount -=1
                    #print('FUTTER')
                    self.rotation+=180
                    self.count_event=0
        #colonie in der naehe
        if self.trage_obj:
            for colony in self.umwelt.colonys:
                if dis_pos(colony.pos,self.pos) <20:
                    self.trage_obj = False
                    colony.food +=1
                    #print(colony.food)
                    self.rotation+=180
                    self.count_event=0
        #neue_Richtung?
        if not self.trage_obj:
            arr = simple_sensor(get_neighborhood(self.colony.phero[1],self.pos,self.sensor_weite))
        else:
            arr = simple_sensor(get_neighborhood(self.colony.phero[0],self.pos,self.sensor_weite))
        sector_i = int((self.rotation+22.5)/45)%8 #kaufmaennisch runden
        bias = 1
        links = arr[(sector_i-1)%8]+bias
        mitte = arr[(sector_i)%8]+bias
        rechts = arr[(sector_i+1)%8]+bias
        
        # weight = links+mitte+rechts
        # new_dir = np.random.random()
        # if new_dir < links/weight:
        #     self.rotation += -40*np.random.random() -30
        # elif new_dir < (links+mitte)/weight:
        #     self.rotation += +60*np.random.random() -30
        # else:
        #     self.rotation += +40*np.random.random() +30
        if max([links,rechts,mitte])<15:
            if np.random.random()<0.3:
                self.rotation += -45+90* np.random.random()
        else:
            if links>mitte and links >rechts:
                self.rotation -= 10
            elif rechts>mitte and rechts > links:
                self.rotation +=10
            
        
        # auswertung
        
        #bewegung


        if self.rotation<0:
            self.rotation += 360
        if self.rotation>0:
            self.rotation -= 360

        move_x = np.cos(self.rotation/180*np.pi)*self.geschwindigkeit
        move_y = np.sin(self.rotation/180*np.pi)*self.geschwindigkeit
        if self.pos[1] + move_y > self.umwelt.hoehe-20 or self.pos[1]+move_y < 0:
            move_y = move_y * -1

        if self.pos[0] + move_x > self.umwelt.breite-20 or self.pos[0]+move_x < 0:
            move_x = move_x * -1
        self.pos = (self.pos[0]+move_x, self.pos[1]+move_y)
        pos_i = (int(self.pos[0]+move_x),int( self.pos[1]+move_y))
        

        change_val = 255-255*f_logistic(self.count_event/100-3,1,1,0.5)
        if not self.trage_obj: # suche futter
            self.colony.change_phero(0,change_val,pos_i)
        else: #suche colony
            self.colony.change_phero(1,change_val,pos_i)

        if move_x != 0:
            self.rotation = np.arctan2(-move_y, move_x)/np.pi*(-180)
            
        elif move_y !=0:
            self.rotation = np.sign(move_y)*180
            
            pass

        self.count_event += 1