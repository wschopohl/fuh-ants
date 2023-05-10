import world
import view
import keyboard
from misc import *
from constants import *

import sys
import pygame
import cProfile
import pstats


debug("python version: {}.{}.{}".format(
    sys.version_info[0], sys.version_info[1], sys.version_info[2]))
debug("pygame version: {}".format(pygame.version.ver))

width = WIDTH
height = HEIGHT
nbants = NBANTS
nturns = NTURNS

if len(sys.argv) == 2:
    nturns = int(sys.argv[1])
assert(nturns >= 0)

# initialization
pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()
world = world.World(width, height)
world.addBlock((int(width/2)-20, int(height/2)+20), (40, 5))
world.addFood((0, 0), (20, 20))
world.addFood((width-20, 0), (20, 20))
world.addFood((0, height-20), (20, 20))
world.addFood((width-20, height-20), (20, 20))
colony1 = world.addColony((int(width/2), int(height/2)), nbants, "blue")
colony2 = world.addColony((int(width/2)+20, int(height/2)-20), nbants, "magenta")

kb = keyboard.KeyboardController(world)
gv = view.GraphicView(world)


cp = cProfile.Profile()
cp.enable()

# main loop
turn = 0
while nturns == 0 or turn < nturns:
    # make sure game doesn't run at more than FPS frames per second
    dt = clock.tick(view.FPS)
    if not kb.tick(dt):
        break
    world.update(dt)
    turn += 1
    gv.update(dt)
    if(turn % 10 == 0):
        print("{} {} {}".format(turn, colony1.getColor(), colony1.getFood()))
        print("{} {} {}".format(turn, colony2.getColor(), colony2.getFood()))

# quit
print("Game Over!")
pygame.quit()

# profiler
cp.disable()
# cp.print_stats()
cp.dump_stats("mystats")
p = pstats.Stats("mystats")
p.strip_dirs()
p.sort_stats("cumulative").print_stats(20)
p.sort_stats("time").print_stats(10)
