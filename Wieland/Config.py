AntMoveDistance = 1
AntAngleVariation = 20
AntAngleStep = 10
AntSleepTime = 0.001
AntPheromoneDrop = 5
AntSenseRadius = 120
AntFieldOfView = 70
AntWallViewDistance = AntMoveDistance + AntAngleStep + 5
AntWallSearchAngle = 15



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
MaxFoodSize = 200