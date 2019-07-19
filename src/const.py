import pygame.locals as pygame_const

# -----ENV---- #
game_name = "Little Car AI"
background_path = "images/background.jpg"

size_larg = 1600  # 1280
# size_haut = size_larg
size_haut = 900  # 720

grid_w_lim = 32
grid_h_lim = 24

# ---INIT PARAMETERS ---#
init_car_x = 260.0
init_car_y = 140.0

FPS_MAX_init = 30
FPS_MAX_max = 240
list_break = [pygame_const.K_q, pygame_const.K_ESCAPE]

font_size = 20

theta_0 = -90.0

# TRAINING
models_path = "raw_models/"

trained_model_path = "results_training/"

nbr_AI_per_gen = 50
rate_survivors = 0.2

nbr_survivors = int(nbr_AI_per_gen * rate_survivors)

weight_on_road = 10
lower_bound_fitness = -1000

max_mutation_rate = 1.0
decay_mutation_rate = 0.95

copy_mutation_rate = 0.08

generation_duration_max_sec = 30
generation_duration_max_frame = generation_duration_max_sec * FPS_MAX_init

generation_duration_init_sec = 1
generation_duration_init_frame = generation_duration_init_sec * FPS_MAX_init

gen_dur_incr_ratio_max = 1.2
generation_duration_incr_sec = 1
generation_duration_incr_frame = generation_duration_incr_sec * FPS_MAX_init

path_train_save = "results_training/"

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
    "sr": road_path + "start_right.png",

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
    "sr": [bot_RIGHT],

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
    "sr": True,

}

track_files_path = "track/"
list_track = [
    "track/track0.tra",
    "track/track1.tra",
    "track/track2.tra"
]

# COLORS

COLOR_GREEN = (0, 255, 0)
COLOR_GREEN_LIGHT = (64, 255, 64)
COLOR_GREEN_BRIGHT = (128, 255, 128)
COLOR_ORANGE = (255, 128, 0)
COLOR_RED = (255, 0, 0)
COLOR_RED_LIGHT = (255, 64, 64)
COLOR_RED_BRIGHT = (255, 128, 128)
COLOR_BLUE = (0, 0, 128)
COLOR_BLUE_LIGHT = (0, 64, 255)
COLOR_BLUE_BRIGHT = (0, 180, 255)

COLORS_LIGHT = [COLOR_GREEN_LIGHT, COLOR_RED_LIGHT, COLOR_BLUE_LIGHT, COLOR_GREEN_LIGHT]
COLORS_BRIGHT = [COLOR_GREEN_BRIGHT, COLOR_RED_BRIGHT, COLOR_BLUE_BRIGHT, COLOR_GREEN_BRIGHT]

# Stupid Name

track_names_list = [
    "hardcore_track",
    "Legendary",
    "Stronger",
    "Better",
    "Faster",
]

# -- MENU -- #

menu_button_h = 125
menu_button_w = 350
offset_h = 50

nbr_buttons = 4

first_button_y = 200

buttons_y = [first_button_y + i * (offset_h + menu_button_h) for i in range(nbr_buttons)]

state_MENU, state_HUMAN, state_AI, state_TRAIN, state_DRAW = 0, 1, 2, 3, 4

title_path = "images/others/title_menu.png"

buttons_img_path = "images/buttons/"

button_list_name = [
    "human",
    "ai",
    "train",
    "draw",
]

buttons_off_path = [buttons_img_path + name + "_off.png" for name in button_list_name]
buttons_on_path = [buttons_img_path + name + "_on.png" for name in button_list_name]
buttons_push_path = [buttons_img_path + name + "_push.png" for name in button_list_name]

button_save_on = buttons_img_path + "save_on.png"
button_save_off = buttons_img_path + "save_off.png"

menu_trackbar_w = 150
menu_trackbar_h = 400
