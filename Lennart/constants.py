from enum import IntEnum
import math


# ===== GENERAL SETTINGS =====

WINDOW_WIDTH = 1200                         # default: 1200 | world<XX>.png won't work otherwise
WINDOW_HEIGHT = 800                         # default: 800 | world<XX>.png won't work otherwise
CELL_SIZE = 5                               # used for world cell type grid and phero grids
FPS_LIMIT = 60                              # default: 60 | also try: 40

MAX_ANTS_PER_COLONY = 200                   # default: 200 | also try: 50, 500
INIT_FOOD_PER_CELL = 2                      # default: 5
FOOD_DEPLETABLE = True                      # default: True

BG_COLOR = (0, 0, 0)                        # background color (= empty cells)
PHERO_COLORS = [                            # pheromone colors for different colonies
    [(0, 255, 0), (0, 0, 255)],             # first is 'TO_FOOD', second is 'TO_HOME'
    [(255, 255, 0), (255, 0, 0)],
    [(255, 255, 255), (255, 127, 0)],
]   
WORLD_PATH = 'img/world02.png'              # window size must be 1200x800 for these to work
# world01 = no walls
# world02 = horizontal / vertical walls
# world03 = curved walls
# world04 = double bridge (equal length)
# world05 = double bridge (unequal length)
# world06 = two colonies (todo: different ant colors for each colony)

# ===== ANT SETTINGS =====

# MOVEMENT
MAX_SPEED = 100                             # default: 100 | also try: 50, 150
ACCEL = 10                                  # default: 10 | also try: 3, 6, 15
OBSTACLE_STEER_STRENGTH = 5                 # default: 5
TARGET_STEER_STRENGTH = 3                   # default: 3 | only for steering to food / home, not pheromones
RANDOM_STEER_STRENGTH = 0.9                 # default: 0.6 | also try: 0.3, 0.9, 1.2
PHERO_WEIGHT = 1                            # default: 1 | for steering to pheros
RANDOM_STEER_UPDATE_MAX_INTERVAL = 1        # default: 1 (in seconds)
TARGET_STEER_UPDATE_INTERVAL = 0.15         # default: 0.15 (in seconds) | also try: 0.05, 0.1
COLLISION_RADIUS = 2                        # default: 2 | probably not needed
OBSTACLE_STEER_UPDATE_INTERVAL = 0.1        # default: 0.5 | also try: 0.1
OBSTACLE_SPOT_DIST = 10                     # default: 20 | also try: 10
OBSTACLE_SPOT_ANGLE = 60                    # default: 60
USE_SIMPLE_PHERO_STEERING = False           # if 'True', only evaluate one cell in fixed disance per sensor
USE_PHERO_MASK_MAX_INSTEAD_OF_SUM = False   # 'True' doesn't work well

# PLACING PHEROMONES
DIST_BETWEEN_MARKERS = 10                   # default: 10 | also try: 3, 25
PHERO_PLACEMENT_AMOUNT_HALVING_TIME = 10    # default: 5 | also try: 10

# SENSING FOOD + PHEROS
MAP_SENSOR_DIST = 50                        # default: 50 | only used for spotting food cells atm
MAP_SENSOR_ANGLE = 60                       # default: 60 | only used for spotting food cells atm
PHERO_SENSOR_DIST = 50                      # default: 50 | also try: 25
PHERO_SENSOR_ANGLE = 60                     # default: 60 | also try: 30, 90

# IMAGE + PHERO MASK LIST
IMG_ROT_STEP = 1                            # default: 1 | must be divisor of 360
IMG_LIST_SIZE = 360 // IMG_ROT_STEP
PHERO_MASK_ROT_STEP = 1                     # default: 1 | must be divisor of 360
PHERO_MASK_LIST_SIZE = 360 // PHERO_MASK_ROT_STEP

# ===== PHERO GRID SETTINGS =====

# PHERO_DECAY_UPDATE_INTERVAL = FPS_LIMIT // 4
PHERO_DECAY_UPDATE_INTERVAL = 0.25          # default: 0.25
# PHERO_IMG_UPDATE_INTERVAL = FPS_LIMIT // 10
PHERO_IMG_UPDATE_INTERVAL = 0.1             # default: 0.1
PHERO_MAX_STRENGTH = 250                    # default: 250
PHERO_DECAY_AMOUNT = 2                      # default: 2 | also try: 1, 5
PHERO_ADD_AMOUNT = 100                      # default: 100 | also try: 50, 250
PHERO_ARR_OFFSET = math.ceil(
    PHERO_SENSOR_DIST / CELL_SIZE)          # if this doesn't work, use '10'

# ===== DEBUG SETTINGS =====

DEBUG_DRAW_SENSOR_MASKS = False             # not working atm


class AntMode(IntEnum):
    TO_FOOD = 0
    TO_HOME = 1


class PheroType(IntEnum):
    TO_FOOD = 0
    TO_HOME = 1


class CellType(IntEnum):
    OUT_OF_BOUNDS = -1
    EMPTY = 0
    WALL = 1
    FOOD = 2
