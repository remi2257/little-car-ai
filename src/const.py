import pygame.locals as pygame_const

# -----ENV---- #
size_larg = 1600  # 1280
# size_haut = size_larg
size_haut = 900  # 720

init_car_x = 260.0
init_car_y = 140.0

FPS_MAX = 30
list_break = [pygame_const.K_q, pygame_const.K_ESCAPE]

font_size = 20

# TRAINING
nbr_AI_per_gen = 20
rate_survivors = 0.2

nbr_survivors = int(nbr_AI_per_gen * rate_survivors)

weight_on_road = 10
lower_bound_fitness = -1000

max_mutation_rate = 1.0
decay_mutation_rate = 0.95

copy_mutation_rate = 0.08

generation_duration_max_sec = 30
generation_duration_max_frame = generation_duration_max_sec * FPS_MAX

generation_duration_init_sec = 1
generation_duration_init_frame = generation_duration_init_sec * FPS_MAX

generation_duration_incr_sec = 1
generation_duration_incr_frame = generation_duration_incr_sec * FPS_MAX

path_train_save = "results/"

# -- CAR PARAMETERS -- #
nbr_bots = 0
path_audi = "images/vehicles/Audi.png"
path_viper = "images/vehicles/Black_viper.png"
path_car_survivor = "images/vehicles/Car.png"

# SPEED/MOVEMENT
speed_max = 30.0
n0_speed = 15.0
max_n_speed = 40

step_dir = 6.0

step_angle = 7.0

drift_factor_cst = 1.3
drift_factor_max = 0.93

# LIDAR

height_LIDAR = 7
width_LIDAR = 5
offset_y_LIDAR = 0

LIDAR_width_img = 150
erode_LIDAR_grid = 2
offset_LIDAR_grid_x = 20
offset_LIDAR_grid_y = 20

# -- DIRECTION -- #

# BOT
bot_DOWN, bot_RIGHT, bot_UP, bot_LEFT = 0, 1, 2, 3

# HUMAN / IA
gas_ON, gas_BRAKE, gas_OFF = 0, 1, 2
dir_LEFT, dir_RIGHT, dir_NONE = 3, 4, 5

# Direction arrows & Pedals

width_arrows_pedals = 100
offset_arrows_pedals = 50

im_others_path = "images/others/"

img_pedals_arrows = {
    gas_ON: im_others_path + "pedals_gas.png",
    gas_BRAKE: im_others_path + "pedals_brake.png",
    gas_OFF: im_others_path + "pedals_off.png",
    dir_LEFT: im_others_path + "arrows_left.png",
    dir_RIGHT: im_others_path + "arrows_right.png",
    dir_NONE: im_others_path + "arrows_off.png",
}

# -- TRACK -- #
road_path = "images/road/"

track_part_1w = {
    "x": None,
    "xx": None,
    "xxx": None,
    "ud": road_path + "road_ud.png",
    "lr": road_path + "road_lr.png",
    "dr": road_path + "road_dr.png",
    "dl": road_path + "road_dl.png",
    "ur": road_path + "road_ur.png",
    "ul": road_path + "road_ul.png",
    "ulr": road_path + "road_ulr.png",
    "udr": road_path + "road_udr.png",
    "udl": road_path + "road_udl.png",
    "dlr": road_path + "road_dlr.png",
    "udlr": road_path + "road_udlr.png",

}

bot_possible_moves_1w = {
    "ud": [bot_UP, bot_DOWN],
    "lr": [bot_LEFT, bot_RIGHT],
    "dr": [bot_RIGHT, bot_DOWN],
    "dl": [bot_LEFT, bot_DOWN],
    "ur": [bot_UP, bot_RIGHT],
    "ul": [bot_UP, bot_LEFT],
    "ulr": [bot_UP, bot_LEFT, bot_RIGHT],
    "udr": [bot_UP, bot_DOWN, bot_RIGHT],
    "udl": [bot_UP, bot_LEFT, bot_DOWN],
    "dlr": [bot_DOWN, bot_LEFT, bot_RIGHT],
    "udlr": [bot_DOWN, bot_UP, bot_LEFT, bot_RIGHT],
}

track_part_1w_practicable = {
    "x": False,
    "xx": False,
    "xxx": False,
    "ud": True,
    "lr": True,
    "dr": True,
    "dl": True,
    "ur": True,
    "ul": True,
    "ulr": True,
    "udr": True,
    "udl": True,
    "dlr": True,
    "udlr": True,

}
# COLORS

COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
