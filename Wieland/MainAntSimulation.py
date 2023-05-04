from World import World
from Nest import Nest
from FoodCluster import FoodCluster
from EnginePygame import EnginePygame
import Const

def main():
    engine = EnginePygame()
    world = World(800,600)
    engine.setup(world)
    world.setup(engine)

    world.add(Nest(position = world.randomPosition(100), spawn_rate=4, max_ants = 100))
    world.add(FoodCluster(position = world.randomPosition(100), amount=100))

    world.run()
    engine.startRenderLoop()  # sync call, execution waits here

if __name__ == '__main__':
    main()