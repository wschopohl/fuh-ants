AntMoveDistance = 1
AntAngleVariation = 20
AntAngleStep = 10
AntSleepTime = 0.001
AntPheromoneDrop = 5
AntSenseRadius = 120
AntFieldOfView = 70
AntWallViewDistance = AntMoveDistance + AntAngleStep + 5
AntWallSearchAngle = 15

RandomSteeringUpdateIntervalMin = 4     # lowest possible number of direction updates where the random steering angle stays the same
RandomSteeringUpdateIntervalMax = 12    # highest possible number of direction updates where the random steering angle stays the same
RandomSteeringWeight = 1                # applied to reduce the strength of random steering if there's a trail to follow (was 0.2 in Wieland's version)

AntPoisonedLifespan = 500               # total lifetime left for poisoned and (in steps)
AntSenseRadiusPoisonPheromones = 60     # used instead of AntSenseRadius for sensing poison pheromones

# graphical configs
NestImageFile = "assets/nest.png"
AntImageFile = "assets/ant_small.png"
AntViewMaskFile = "assets/ant_small_view_mask.png"
#AntFoodPosition = (10,10)
AntFoodPosition = (12,9)
AntMiddlePosition = (9,9)
AntFoodSize = 2.5

NestSize = 20
FoodSize = 0.03

PheromoneSize = 2
PheromoneDecay = 0.001
PheromoneDistanceReduce = 0.1
PheromoneMapTileSize = 15

# The maximum food size that can be placed per mouse click (interaction) is defined as follows 
MaxUserFoodSize = 400
UseThreading = False
UseNumpy = True
