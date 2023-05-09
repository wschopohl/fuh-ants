from World import World
from Nest import Nest
from FoodCluster import FoodCluster
from EnginePygame import EnginePygame
import Const

def main():
    engine = EnginePygame()
    world = World(1200,800)
    engine.setup(world)
    world.setup(engine)

    # world.add(Nest(position = world.randomPosition(100), spawn_rate=50, max_ants = 500))
    # world.add(FoodCluster(position = world.randomPosition(100), amount=1000))
    # world.add(FoodCluster(position = world.randomPosition(100), amount=1000))

    world.add(Nest(position = (600,400), spawn_rate=50, max_ants = 500))
    world.add(FoodCluster(position = (100,100), amount=1000))
    world.add(FoodCluster(position = (1100,700), amount=1000))
    world.add(FoodCluster(position = (100,700), amount=1000))
    world.add(FoodCluster(position = (1100,100), amount=1000))

    world.run()
    engine.startRenderLoop()  # sync call, execution waits here

if __name__ == '__main__':
    main()