import pygame.locals as pygame_const
from math import ceil
import os


def get_screen_infos_linux(ratio_screen_window):
    import subprocess

    cmd = ['xrandr']
    cmd2 = ['grep', '*']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()

    resolution_string, junk = p2.communicate()
    resolution = resolution_string.split()[0].decode('utf8')
    width, height = resolution.split('x')
    # print(width,height)
    return int(int(width) // ratio_screen_window), int(int(height) // ratio_screen_window)


def get_screen_infos(ratio_screen_window):
    import tkinter

    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    return int(int(width) // ratio_screen_window), int(int(height) // ratio_screen_window)


# -----ENV---- #
game_name = "Little Car AI"
images_path = "uix/images/"
background_path = os.path.join(images_path, "background.jpg")

ratio_screen_window_ = 1.2
big_window_larg, big_window_haut = get_screen_infos_linux(ratio_screen_window_)
# big_window_larg = 1600  # 1280
# big_window_haut = big_window_larg
# big_window_haut = 900  # 720


# ---INIT PARAMETERS ---#
init_car_x = 260.0
init_car_y = 140.0

FPS_MAX_init = 30
FPS_MAX_max = 240
list_break = [pygame_const.K_q, pygame_const.K_ESCAPE]

font_size_global = round(big_window_haut / 45)

theta_0 = -90.0

# TRAINING
models_path = "raw_models/"

trained_model_path = "results_training/"

nbr_AI_per_gen = 28
rate_survivors = 0.25

nbr_survivors = int(nbr_AI_per_gen * rate_survivors)

weight_on_road = 10
lower_bound_fitness = -1000

boost_checkpoint = 250

max_mutation_rate = 1.0
decay_mutation_rate = 0.95

copy_mutation_rate = 0.08

generation_duration_max_sec = 20
generation_duration_max_frame = generation_duration_max_sec * FPS_MAX_init

generation_duration_init_sec = 1
generation_duration_init_frame = generation_duration_init_sec * FPS_MAX_init

gen_dur_incr_ratio_max = 1.2
generation_duration_incr_sec = 1
generation_duration_incr_frame = generation_duration_incr_sec * FPS_MAX_init

path_train_save = "results_training/"

# -- CAR PARAMETERS -- #
nbr_bots = 0
path_vehicles = os.path.join(images_path, "vehicles")
path_audi = os.path.join(path_vehicles, "Audi.png")
path_viper = os.path.join(path_vehicles, "Black_viper.png")
path_car_survivor = os.path.join(path_vehicles, "Car.png")

# SPEED/MOVEMENT
speed_max_raw = 300.0  # Speed has to be divide by number of cases
n0_speed = 15.0
max_n_speed = 40

step_dir = 9.0

car_step_angle = 5.0

drift_factor_cst = 1.3
drift_factor_max = 0.93

# LIDAR

height_LIDAR = 7
width_LIDAR = 5
offset_y_LIDAR = 0

LIDAR_width_img = ceil(big_window_haut / (20 * 8)) * 20
erode_LIDAR_grid = 1 + int(big_window_larg / 1500)
offset_LIDAR_grid_x = 20
offset_LIDAR_grid_y = 20

circle_size = max(1, int(round(big_window_larg / 1920) * 3))

# -- DIRECTION -- #

# Dir for Track & BOT
dir_DOWN, dir_RIGHT, dir_UP, dir_LEFT = 0, 1, 2, 3

# HUMAN / IA
gas_ON, gas_BRAKE, gas_OFF = 0, 1, 2
wheel_LEFT, wheel_RIGHT, wheel_NONE = 3, 4, 5

# Direction arrows & Pedals

width_arrows_pedals = round(big_window_haut / 12)
offset_arrows_pedals = round(big_window_haut / 20)

im_others_path = os.path.join(images_path, "others/")

img_pedals_arrows = {
    gas_ON: im_others_path + "pedals_gas.png",
    gas_BRAKE: im_others_path + "pedals_brake.png",
    gas_OFF: im_others_path + "pedals_off.png",
    wheel_LEFT: im_others_path + "arrows_left.png",
    wheel_RIGHT: im_others_path + "arrows_right.png",
    wheel_NONE: im_others_path + "arrows_off.png",
}

# -- TRACK -- #
road_path = os.path.join(images_path, "road/")

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
    "dlr1": road_path + "road_dlr1.png",
    "dlr2": road_path + "road_dlr2.png",
    "dlr3": road_path + "road_dlr3.png",
    "udlr": road_path + "road_udlr.png",
    "sr": road_path + "start_right.png",

}

bot_possible_moves_1w = {
    "ud": [dir_UP, dir_DOWN],
    "lr": [dir_LEFT, dir_RIGHT],
    "dr": [dir_RIGHT, dir_DOWN],
    "dl": [dir_LEFT, dir_DOWN],
    "ur": [dir_UP, dir_RIGHT],
    "ul": [dir_UP, dir_LEFT],
    "ulr": [dir_UP, dir_LEFT, dir_RIGHT],
    "udr": [dir_UP, dir_DOWN, dir_RIGHT],
    "udl": [dir_UP, dir_LEFT, dir_DOWN],
    "dlr": [dir_DOWN, dir_LEFT, dir_RIGHT],
    "udlr": [dir_DOWN, dir_UP, dir_LEFT, dir_RIGHT],
    "sr": [dir_RIGHT],

}

track_part_1w_practicable = {
    "x": False,
    "xx": False,
    "xxx": False,
    "ud": True,
    "lr": True,
    "lr1": True,
    "lr2": True,
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

track_files_path = "tracks/"
list_track = [
    "tracks/race_tiny.tra",
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


# -- MENU -- #
# 521 x 246 = ratio de 2.13
menu_button_w = round(big_window_haut / 3.5)
menu_button_h = round(menu_button_w / 2.13)

offset_h = round(20 * big_window_haut / 700)

nbr_buttons = 4

first_button_y = round(200 * big_window_haut / 800)

buttons_y = [first_button_y + i * (offset_h + menu_button_h) for i in range(nbr_buttons)]

state_MENU, state_HUMAN, state_AI, state_TRAIN, state_DRAW = 0, 1, 2, 3, 4

title_path = os.path.join(images_path, "others/title_menu.png")

buttons_img_path = os.path.join(images_path, "buttons/")

menu_selection_w = round(150 * 900 / big_window_haut)
menu_selection_h = round(400 * 900 / big_window_haut)
