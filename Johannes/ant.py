import numpy as np
import random

def mask_array(arr,rot):
    pass
    return arr

def get_neighborhood(map,pos,sensor_weite):
    return map[int(pos[0])-sensor_weite:int(pos[0])+sensor_weite+1,
                                   int(pos[1])-sensor_weite:int(pos[1])+sensor_weite+1]
        
    pass
def sum_neighborhood(map,pos,sensor_weite):
    return sum(map[int(pos[0])-sensor_weite:int(pos[0])+sensor_weite+1,
                                   int(pos[1])-sensor_weite:int(pos[1])+sensor_weite+1])
def simple_sensor(map):
    pos = [(7,4),(7,7),(4,7),(1,7),(1,4),(1,1),(4,1),(7,1)]
    return [np.sum(get_neighborhood(map,x,1)) for x in pos]
            
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
        self.rotation = 360*np.random.random()
        self.geschwindigkeit = geschwindigkeit 
        self.name = name
        self.vis_obj = vis_obj
        self.sensor_weite = 4 #"sichtweise" in pixel
        self.trage_obj = None
        self.count_event=0
        
    def sensor(self,phero):
        sensor_fov={-60:3,-30:7,0:10,30:7,60:3}
        sensor_depth = {15:4,10:6,5:10}
        sensor_list  = []
        # for y in sensor_fov.keys():
        #     deep_list = []
        #     for x in sensor_depth.keys():
        #         deep_list.append(sum(sum_neighborhood(phero,(int(self.pos[0]+np.cos((self.rotation+y)/180*np.pi)),
        #                                               int(self.pos[1]+np.sin((self.rotation+y)/180*np.pi))),2)
        #                 )*sensor_depth[x])
        #     sensor_list.append(sum(deep_list))
        # sum(sensor_list)

        weighted_dir=np.array([sum(
                        [sum(sum_neighborhood(phero,(int(self.pos[0]+np.cos((self.rotation+y)/180*np.pi)*x),
                                                      int(self.pos[1]+np.sin((self.rotation+y)/180*np.pi)*x)),2)
                        )*sensor_depth[x] for x in sensor_depth.keys()]) for y in sensor_fov.keys()])
        weight= sum(weighted_dir)
        if weight!=0:
            weighted_dir =weighted_dir/weight
            new_dir =sum([weighted_dir[i]*y for i,y in enumerate(sensor_fov.keys())])
        else:
            new_dir=0
        return new_dir
    def update(self):

        # sensor
        #Futter in der naehe?
        if not self.trage_obj:
            for food in self.umwelt.food_places:
                if dis_pos(food.pos,self.pos) <20:
                    self.trage_obj = True
                    food.amount -=1
                    print('FUTTER')
                    self.rotation+=180
                    self.count_event=0
        #colonie in der naehe
        if self.trage_obj:
            for colony in self.umwelt.colonys:
                if dis_pos(colony.pos,self.pos) <20:
                    self.trage_obj = False
                    colony.food +=1
                    print(colony.food)
                    self.rotation+=180
                    self.count_event=0
        #neue_Richtung?
        # if not self.trage_obj:
        #     arr = simple_sensor(get_neighborhood(self.colony.phero[1],self.pos,self.sensor_weite))
        # else:
        #     arr = simple_sensor(get_neighborhood(self.colony.phero[0],self.pos,self.sensor_weite))
        # sector_i = int((self.rotation+22.5)/45)%8 #kaufmaennisch runden
        # bias = 1
        # links = arr[(sector_i-1)%8]+bias
        # mitte = arr[(sector_i)%8]+bias
        # rechts = arr[(sector_i+1)%8]+bias

        # sensor_fov={-120:2,-90:4,-60:6,-30:8,0:10,30:8,60:6,90:4,120:2}
        # sensor_depth = {25:2,20:4,15:6,10:8,5:10}

        # sensor_fov={-60:6,-30:8,0:10,30:8,60:6}
        # sensor_depth = {15:6,10:8,5:10}
        if self.count_event%6 ==0:
            # new_dir=sum([sum([sum(get_neighborhood(self.colony.phero[1],(self.pos[0]+np.cos((self.rotation+y)/180*np.pi),
            #                                                     self.pos[1]+np.sin((self.rotation+y)/180*np.pi)),2)
            #             )*sensor_depth[x] for x in sensor_depth.keys()])/30*sensor_fov[y] for y in sensor_fov.keys()])/50
            
            if not self.trage_obj:
                new_dir=self.sensor(self.colony.phero[1])
            else:
                new_dir=self.sensor(self.colony.phero[0])

            if new_dir==0:
                if np.random.random()<0.3:
                    self.rotation = self.rotation-30+np.random.random()*60
            else:
                self.rotation += new_dir
        # weight = links+mitte+rechts
        # new_dir = np.random.random()
        # if new_dir < links/weight:
        #     self.rotation += -40*np.random.random() -30
        # elif new_dir < (links+mitte)/weight:
        #     self.rotation += +60*np.random.random() -30
        # else:
        #     self.rotation += +40*np.random.random() +30
        # if self.count_event%6 ==0:
        #     if max([links,rechts,mitte])<20:
        #         if np.random.random()<0.1:
        #             self.rotation += -45+90* np.random.random()
        #     else:
        #         if links>mitte and links >rechts:
        #             self.rotation -= 45
        #         elif rechts>mitte and rechts > links:
        #             self.rotation +=45
            
        
        # auswertung
        
        #bewegung


        while self.rotation<0:
            self.rotation += 360
        while self.rotation>360:
            self.rotation -= 360
        pos_i = (int(self.pos[0]),int( self.pos[1]))
        col_map = get_neighborhood(self.umwelt.map,pos_i,1)
        
        move_x = np.cos(self.rotation/180*np.pi)#*self.geschwindigkeit
        move_y = np.sin(self.rotation/180*np.pi)#*self.geschwindigkeit
        #pos_i_neu = (int(self.pos[0]+move_x),int( self.pos[1]+move_y))
        #colmap_ 0 ist wand 1 ist frei
        
        i,j = np.where(col_map == 0)


        #if col_map[int(self.pos[0]+move_x)-int(pos_i[0]),int(self.pos[1]+move_y)-int(pos_i[1])]==0: 
        if len(i)>0:    
            i,j = np.where(col_map == 1)
            if len(i) == 0:
                move_y = 0
                move_x = 0
                print(col_map,i,j,self.pos)
                print('ant in the wall')
            else:
                
                x = np.random.randint(len(i))
                #print(col_map,i,j,x,self.pos)
                move_x = (i[x]-1)
                move_y = (j[x]-1)
            # self.rotation = np.random.random()*360
            # move_x = np.cos(self.rotation/180*np.pi)#*self.geschwindigkeit
            # move_y = np.sin(self.rotation/180*np.pi)#*self.geschwindigkeit
        
        # if self.pos[1] + move_y > self.umwelt.hoehe-20 or self.pos[1]+move_y < 0:
        #     move_y = move_y * -1

        # if self.pos[0] + move_x > self.umwelt.breite-20 or self.pos[0]+move_x < 0:
        #     move_x = move_x * -1
        self.pos = (self.pos[0]+move_x, self.pos[1]+move_y)
        pos_i = (int(self.pos[0]+move_x),int( self.pos[1]+move_y))
        
        #get_neighborhood(self.umwelt.map,())

        #pheromone

        if self.count_event%6 == 0:
            change_val = 255-255*f_logistic(self.count_event/100-3,1,1,0.5)
            change_val = 255
            if not self.trage_obj: # suche futter
                #change_val = min(255,50+255-255*f_logistic(self.count_event/100-3,1,1,0.5))
                self.colony.change_phero(0,change_val,pos_i)
            else: #suche colony
                #change_val = min(255,150+255-255*f_logistic(self.count_event/100-3,1,1,0.5))
                self.colony.change_phero(1,change_val,pos_i)

        if move_x != 0:
            self.rotation = np.arctan2(-move_y, move_x)/np.pi*(-180)
            
        elif move_y !=0:
            self.rotation = np.sign(move_y)*180
            
            pass

        self.count_event += 1