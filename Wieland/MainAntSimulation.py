from World import World
from Nest import Nest, Unlimited
from EnginePygame import EnginePygame

def main():
    world = World(800,600)
    world.add(Nest(position = world.randomPosition(), spawn_rate=20, max_ants = 100))
    world.run()

    engine = EnginePygame()
    engine.setup(world)
    engine.startRenderLoop()  # sync call, execution waits here

    world.stop()

if __name__ == '__main__':
    main()