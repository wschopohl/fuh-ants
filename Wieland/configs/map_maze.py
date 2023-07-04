import Config

Config.AntMoveDistance = 1
Config.AntAngleVariation = 15
Config.AntAngleStep = 10
Config.AntSleepTime = 0.001
Config.AntPheromoneDrop = 5
Config.AntSenseRadius = 30
Config.AntNestSenseRadius = 100
Config.AntFieldOfView = 70
Config.AntWallViewDistance = Config.AntMoveDistance + Config.AntAngleStep + 5
Config.AntWallSearchAngle = 33

Config.RandomSteeringUpdateIntervalMin = 4     # lowest possible number of direction updates where the random steering angle stays the same
Config.RandomSteeringUpdateIntervalMax = 12    # highest possible number of direction updates where the random steering angle stays the same
Config.RandomSteeringWeight = 1                # applied to reduce the strength of random steering if there's a trail to follow (was 0.2 in Wieland's version)

Config.AntPoisonedLifespan = 500               # total lifetime left for poisoned and (in steps)
Config.AntSenseRadiusPoisonPheromones = 60     # used instead of AntSenseRadius for sensing poison pheromones

Config.PheromoneDecay = 0.0005
Config.PheromoneDistanceReduce = 0.1
Config.PheromoneMapTileSize = 5