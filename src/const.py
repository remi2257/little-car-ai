import os
from enum import Enum


def get_screen_infos_linux(ratio_screen_window):
    import subprocess

    cmd = ['xrandr']
    cmd2 = ['grep', '*']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()

    resolution_string, junk = p2.communicate()
    try:
        resolution = resolution_string.split()[0].decode('utf8')
        width, height = resolution.split('x')
    except IndexError:
        width = 1200
        height = 800
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
images_path = "src/uix/images/"
background_path = os.path.join(images_path, "background.jpg")

ratio_screen_window_ = 1.2
big_window_larg, big_window_haut = get_screen_infos_linux(ratio_screen_window_)

# ---INIT PARAMETERS ---#
FPS_MAX_init = 30
FPS_MAX_max = 240

font_size_global = round(big_window_haut / 45)

# TRAINING
raw_models_path = "models/raw/"

trained_model_path = "models/trained/"

# -- CAR PARAMETERS -- #
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

height_grid_LIDAR = 7
width_grid_LIDAR = 5
offset_y_LIDAR = 0

circle_size = max(1, int(round(big_window_larg / 1920) * 3))


# -- DIRECTION -- #

# Dir for Track & BOT
class Direction(Enum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3


# --- IMAGES --- #
im_others_path = os.path.join(images_path, "others/")

# -- TRACK -- #
track_files_path = "tracks/"

roads_path = os.path.join(images_path, "road/")

track_part_1w = {
    "x": None,
    "xx": None,
    "xxx": None,
    "ud": roads_path + "road_ud.png",
    "lr": roads_path + "road_lr.png",
    "dr": roads_path + "road_dr.png",
    "dl": roads_path + "road_dl.png",
    "ur": roads_path + "road_ur.png",
    "ul": roads_path + "road_ul.png",
    "ulr": roads_path + "road_ulr.png",
    "udr": roads_path + "road_udr.png",
    "udl": roads_path + "road_udl.png",
    "dlr": roads_path + "road_dlr.png",
    "dlr1": roads_path + "road_dlr1.png",
    "dlr2": roads_path + "road_dlr2.png",
    "dlr3": roads_path + "road_dlr3.png",
    "udlr": roads_path + "road_udlr.png",
    "sr": roads_path + "start_right.png",

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

# -- MENU -- #
title_path = os.path.join(images_path, "others/title_menu.png")

buttons_img_path = os.path.join(images_path, "buttons/")
