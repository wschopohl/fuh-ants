import pygame

class CollisionPygame():
    def __init__(self):
        pass

    def check(self, single, cluster):
        (pgsprite, pggroup) = self.getPGObjects(single, cluster)
        if pgsprite == None: return []

        pgobjs = pygame.sprite.spritecollide(pgsprite, pggroup, False)
        objs = [pgobj.ant for pgobj in pgobjs]
        return objs
    
    def getNearby(self, single, cluster, radius, type):
        (pgsprite, pggroup) = self.getPGObjects(single, cluster)
        if pgsprite == None: return []

        pgsprite.radius = radius
        pgobjs = pygame.sprite.spritecollide(pgsprite, pggroup, False, pygame.sprite.collide_circle)
        objs = [pgobj.pheromone for pgobj in pgobjs]
        ret_objs = list(filter(lambda obj: obj.type == type, objs))
        return ret_objs


    def getPGObjects(self, single, cluster):
        if cluster == []: return (None, None)
        pgsprite = single.sprite
        pggroup = cluster[0].sprite.groups()
        if pgsprite == None or pggroup == []:
            return (None, None)
        
        pggroup = pggroup[0]
        return (pgsprite, pggroup)