import sys
from World import World
from Nest import Nest
from FoodCluster import FoodCluster
from EnginePygame import EnginePygame
from Map import Map

def main():
    scene = 1
    if len(sys.argv) == 1:
        print((" +++ You can load different scenes +++ "))
        print((" +++ python MainAntSimulation.py [num] +++ "))
    else:
        scene = int(sys.argv[1])
        if scene < 1 or scene > 4: scene = 5

    engine = EnginePygame()
    world = World(1150,680)
    engine.setup(world)
    world.setup(engine)

    if scene == 1:
        world.add(Map("assets/maps/map_dyno.png"))
        world.add(Nest(position = (226,166), spawn_rate=50, max_ants = 500))
        world.add(FoodCluster(position = (648,616), amount=200))
        world.add(FoodCluster(position = (1056,622), amount=400))
        world.add(FoodCluster(position = (1006,108), amount=600))
    elif scene == 2:
        world.add(Map("assets/maps/map_decision_equal.png"))
        world.add(Nest(position = (60,326), spawn_rate=50, max_ants = 500))
        world.add(FoodCluster(position = (1080,326), amount=2000))
    elif scene == 3:
        world.add(Map("assets/maps/map_decision_different.png"))
        world.add(Nest(position = (64,223), spawn_rate=50, max_ants = 500))
        world.add(FoodCluster(position = (1080,206), amount=2000))
    elif scene == 4:
        world.add(Map("assets/maps/map_maze.png"))
        world.add(Nest(position = (430,390), spawn_rate=50, max_ants = 500))
        world.add(FoodCluster(position = (1020,80), amount=2000))
    elif scene == 5:
        world.add(Nest(position = world.randomPosition(100), spawn_rate=50, max_ants = 500))
        world.add(FoodCluster(position = world.randomPosition(100), amount=1000))
        world.add(FoodCluster(position = world.randomPosition(100), amount=1000))
        world.add(FoodCluster(position = world.randomPosition(100), amount=1000))
        world.add(FoodCluster(position = world.randomPosition(100), amount=1000))


    world.run()
    engine.startRenderLoop()  # sync call, execution waits here

if __name__ == '__main__':
    main()