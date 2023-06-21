""" Defines some colors """

from Pheromone import Type as PheromoneType

Background = (220, 220, 220)
UserLine = (0, 0, 0)
Nest = (92,22,9)
Ant = (135,62,35)
FoodCluster = (121,169,25)
FoodClusterPoisoned = (127,0,127)
Description = (0, 0, 0)

UserWalls = (128,52,2,255)
InfoText = (0,0,100)

PheromoneColors = {
    PheromoneType.HOME.value : (168,34,8),
    PheromoneType.FOOD.value : (121,169,25),
    PheromoneType.POISON.value : (127,0,127)
}
