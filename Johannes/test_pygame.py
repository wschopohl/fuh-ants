
#https://www.python-lernen.de/pygame-animation.htm

#https://www.python-lernen.de/pygame-tastatur-abfragen.htm Tatstaur-abkuerzungen

#ant-graphic https://opengameart.org/content/walking-ant-with-parts-and-rigged-spriter-file

import pygame
from numpy import arctan2,pi,sign

pygame.init()


# genutzte Farbe
ORANGE  = ( 255, 140, 0)
ROT     = ( 255, 0, 0)
GRUEN   = ( 0, 255, 0)
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)

#Konstanten
F_breite = 640
F_hoehe = 480

# Bilder
ameise = pygame.image.load("walking_ant.png")

ameise_frame_h = 248
ameise_frame_b = 202

ameise_frame = []

print(ameise_frame)
# Fenster öffnen
screen = pygame.display.set_mode((F_breite, F_hoehe))


surf = pygame.Surface((1616,1984))
for n in range(62): #62 sprites auf 8x8 grid
    i = n%8
    j = n//8
    #ameise_frame.append((i*ameise_frame_b,j*ameise_frame_h,(i+1)*ameise_frame_b+1,(j+1)*ameise_frame_h))
    #ameise_frame.append(ameise.subsurface(pygame.Rect((i*ameise_frame_b,j*ameise_frame_h,(i+1)*ameise_frame_b,(j+1)*ameise_frame_h))))
    ameise_frame.append(ameise.subsurface(pygame.Rect((i*ameise_frame_b,j*ameise_frame_h,ameise_frame_b,ameise_frame_h))).convert_alpha())
    




#titel
pygame.display.set_caption("Unser erstes Pygame-Spiel")

# solange die Variable True ist, soll das Spiel laufen
spielaktiv = True
clock = pygame.time.Clock()
ant_frame = 0



ballpos_x = 10
ballpos_y = 30

bewegung_x = 2
bewegung_y = 2

# Schleife Hauptprogramm
while spielaktiv:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False
            print("Spieler hat Quit-Button angeklickt")
        elif event.type == pygame.KEYDOWN:
            print("Spieler hat Taste gedrückt")
            if event.key == pygame.K_RIGHT:
                print("Spieler hat Pfeiltaste rechts gedrückt")
            elif event.key == pygame.K_LEFT:
                print("Spieler hat Pfeiltaste links gedrückt")
            elif event.key == pygame.K_UP:
                print("Spieler hat Pfeiltaste hoch gedrückt")
            elif event.key == pygame.K_DOWN:
                print("Spieler hat Pfeiltaste runter gedrückt")
            elif event.key == pygame.K_SPACE:
                print("Spieler hat Leertaste gedrückt")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Spieler hast Maus angeklickt")   
    
    # Spiellogik hier integrieren
    
    # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)
    screen.fill(ORANGE)
    ant_frame += 1

    if ant_frame >61:
        ant_frame = 0
    
    if ballpos_y > F_hoehe-20 or ballpos_y < 0:
        bewegung_y = bewegung_y * -1

    if ballpos_x > F_breite-20 or ballpos_x < 0:
        bewegung_x = bewegung_x * -1
    ballpos_x += bewegung_x
    ballpos_y += bewegung_y

    if bewegung_x != 0:
        rot = arctan2(-bewegung_y,-bewegung_x)/pi*-180+90
        print(rot)
    else:
        rot = sign(bewegung_y)*180

    #pygame.draw.ellipse(screen, WEISS, [ballpos_x, ballpos_y, 20, 20])
    #pic = pygame.transform.smoothscale_by(ameise_frame[ant_frame],0.1)
    #screen.blit(pic,(ballpos_x,ballpos_y))
    screen.blit(pygame.transform.rotozoom(ameise_frame[ant_frame],rot,0.05),(ballpos_x,ballpos_y))#)pygame.transform.scale(ameise_frame[ant_frame],(20,20)),(ballpos_x,ballpos_y))
    
    # Fenster aktualisieren
    pygame.display.flip()
    # Refresh-Zeiten festlegen
    clock.tick(60)
