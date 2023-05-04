import pygame

class CollisionPygame():
    def __init__(self):
        pass

    def check(self, single, cluster):
        pgsprite = single.sprite
        pggroup = cluster[0].sprite.groups()
        if pgsprite == None or pggroup == []:
            return []
        
        pggroup = pggroup[0]
        pgobjs = pygame.sprite.spritecollide(pgsprite, pggroup, False)
        objs = [pgobj.ant for pgobj in pgobjs]
        return objs