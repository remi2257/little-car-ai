import pygame.locals as pygame_const

# -----ENV---- #

size_larg = 1280
# size_haut = size_larg
size_haut = 720

FPS_MAX = 30
list_break = [pygame_const.K_q, pygame_const.K_ESCAPE]

nbr_bots = 3

# -- CAR PARAMETERS -- #

# SPEED/MOVEMENT
speed_max = 30.0
n0_speed = 15.0

step_dir = 6.0

step_angle = 5.0

# LIDAR

height_LIDAR = 7
width_LIDAR = 5
offset_LIDAR = 1

# -- DIRECTION -- #

# BOT
bot_DOWN, bot_RIGHT, bot_UP, bot_LEFT = 0, 1, 2, 3

# HUMAN / IA
gas_ON, gas_BRAKE, gas_OFF = 0, 1, 2
dir_LEFT, dir_RIGHT, dir_NONE = 3, 4, 6

# -- TRACK -- #
road_path = "images/road/"

track_part_1w = {
    "xx": None,
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
}

track_part_1w_practicable = {
    "xx": False,
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

}

track_part_2w_path = {
    "xx": None,
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

}

bot_possible_moves_2w = {
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
}


