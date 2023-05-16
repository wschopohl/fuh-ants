import umwelt
import pygame



############
# Konstanten
############

#def Farben
ORANGE  = ( 255, 140, 0)
SCHWARZ = ( 0, 0, 0)
GRAU = ( 150, 150, 150)
WEISS   = ( 255, 255, 255)
GRUEN_PHEROA = (0, 255, 0)

#Weltgroesse
F_breite = 800
F_hoehe = 600


# init Grafik
pygame.init()
# Bilder

#BG/map

bg_map = pygame.image.load("Johannes/map_01.png")
ameise = pygame.image.load("Johannes/walking_ant.png")

ameise_frame_h = 248
ameise_frame_b = 202

ameise_frame = []

print(ameise_frame)
# Fenster öffnen
screen = pygame.display.set_mode((F_breite, F_hoehe))


surf_phero_a = pygame.Surface((F_breite, F_hoehe), pygame.SRCALPHA)
surf_phero_a.fill([0,255,0,0])
#surf_phero_a_alpha = pygame.surfarray.pixels_alpha(surf_phero_a)

surf_phero_b = pygame.Surface((F_breite, F_hoehe), pygame.SRCALPHA)
surf_phero_b.fill([0,0,255,0])
#surf_phero_b_alpha = pygame.surfarray.pixels_alpha(surf_phero_b)

for n in range(62): #62 sprites auf 8x8 grid
    i = n%8
    j = n//8
    ameise_frame.append(ameise.subsurface(pygame.Rect((i*ameise_frame_b,j*ameise_frame_h,ameise_frame_b,ameise_frame_h))).convert_alpha())

#init Umwelt

Umwelt = umwelt.umwelt(F_breite,F_hoehe)

Umwelt.map = pygame.surfarray.array2d(bg_map)
Umwelt.add_colony()




spielaktiv = True
clock = pygame.time.Clock()
ant_frame = 0

# Schleife Hauptprogramm
while spielaktiv:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False
            print("Spieler hat Quit-Button angeklickt")
        # elif event.type == pygame.KEYDOWN:
        #     print("Spieler hat Taste gedrückt")
        #     if event.key == pygame.K_RIGHT:
        #         print("Spieler hat Pfeiltaste rechts gedrückt")
        #     elif event.key == pygame.K_LEFT:
        #         print("Spieler hat Pfeiltaste links gedrückt")
        #     elif event.key == pygame.K_UP:
        #         print("Spieler hat Pfeiltaste hoch gedrückt")
        #     elif event.key == pygame.K_DOWN:
        #         print("Spieler hat Pfeiltaste runter gedrückt")
        #     elif event.key == pygame.K_SPACE:
        #         print("Spieler hat Leertaste gedrückt")
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     print("Spieler hast Maus angeklickt")   
    
    # Spiellogik hier integrieren
    Umwelt.update()
    # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)
    #screen.fill(ORANGE)
    screen.blit(bg_map,(0,0))
    ant_frame += 1

    if ant_frame >61:
        ant_frame = 0
        #print(clock.get_fps(),len(Umwelt.ants))
    if ant_frame %15==0:
        for colony in Umwelt.colonys:
            if len(colony.ants)<150:
                colony.add_ant()
            # else:
            #     if ant_frame %30==0:
            #         colony.add_ant()
            

    for food in Umwelt.food_places:
        pygame.draw.circle(screen, SCHWARZ, food.pos, 20)

    for colony in Umwelt.colonys:
        #äphero_map = pygame.surfarray.make_surface(colony.phero[0])
        #phero_map.set_colorkey(0)
        #surf_phero_a.set_alpha(colony.phero[0])
        pygame.draw.circle(screen, GRAU, colony.pos, 20)
        surf_phero_a_alpha = pygame.surfarray.pixels_alpha(surf_phero_a)
        surf_phero_a_alpha[:] = colony.phero[0]#.astype('uint8')
        del surf_phero_a_alpha
        screen.blit(surf_phero_a,(0,0))
        surf_phero_b_alpha = pygame.surfarray.pixels_alpha(surf_phero_b)
        surf_phero_b_alpha[:] = colony.phero[1]#.astype('uint8')
        del surf_phero_b_alpha
        screen.blit(surf_phero_b,(0,0))
        for ant in colony.ants:
            screen.blit(pygame.transform.rotozoom(ameise_frame[ant_frame],-ant.rotation-90,0.05),(ant.pos[0]-9,ant.pos[1]-9,))
    #)pygame.transform.scale(ameise_frame[ant_frame],(20,20)),(ballpos_x,ballpos_y))
    
    pygame.display.flip()
    # Refresh-Zeiten festlegen
    clock.tick(120)