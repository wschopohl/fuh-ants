from Ant import Ant

class Colony:
    

    def __init__(self, screen ,ant_count = 1):
        self.ants = []
        self.screen = screen
        for i in range (ant_count):
            self.ants.append(Ant(screen,self))

        

    def update(self, elapsed):
        for ant in self.ants:
            ant.update(elapsed)

            # Make sure the ant is not moving out of the window
            if ant.ant_pos[0] <= 0 or ant.ant_pos[0] >= self.screen.WIDTH:
                ant.ant_pos[0] *= -1

            if ant.ant_pos[1] <= 0 or ant.ant_pos[1] >= self.screen.HEIGHT:
             ant.ant_pos[1] *= -1


   