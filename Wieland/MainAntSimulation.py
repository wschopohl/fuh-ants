from World import World
from Nest import Nest
from FoodCluster import FoodCluster
from EnginePygame import EnginePygame
from Map import Map

def main():
    engine = EnginePygame()
    world = World(1200,800)
    engine.setup(world)
    world.setup(engine)

    # world.add(Nest(position = world.randomPosition(100), spawn_rate=50, max_ants = 500))
    # world.add(FoodCluster(position = world.randomPosition(100), amount=1000))
    # world.add(FoodCluster(position = world.randomPosition(100), amount=1000))
    # world.add(FoodCluster(position = world.randomPosition(100), amount=1000))
    # world.add(FoodCluster(position = world.randomPosition(100), amount=1000))

    # world.add(Nest(position = (600,400), spawn_rate=50, max_ants = 500))
    # world.add(FoodCluster(position = (100,100), amount=1000))
    # world.add(FoodCluster(position = (1100,700), amount=1000))
    # world.add(FoodCluster(position = (100,700), amount=1000))
    # world.add(FoodCluster(position = (1100,100), amount=1000))

    # world.add(Map("assets/map_ugly.png"))
    # world.add(Nest(position = (100,420), spawn_rate=50, max_ants = 500))
    # world.add(FoodCluster(position = (1000,420), amount=1000))

    world.add(Map("assets/map_ugly2.png"))
    world.add(Nest(position = (226,216), spawn_rate=50, max_ants = 100))
    # world.add(FoodCluster(position = (648,656), amount=1000))
    world.add(FoodCluster(position = (1056,662), amount=1000))
    #world.add(FoodCluster(position = (1006,148), amount=1000))

    world.run()
    engine.startRenderLoop()  # sync call, execution waits here

if __name__ == '__main__':
    main()