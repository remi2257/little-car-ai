import pygame.locals as pygame_const

# -----ENV---- #

size_larg = 1280
# size_haut = size_larg
size_haut = 720

grid_under_sample = 16

car_max_len = max(size_larg, size_haut) // grid_under_sample

FPS_MAX = 30
list_break = [pygame_const.K_q, pygame_const.K_ESCAPE]

nbr_bots = 1

# -- DIRECTION -- #

DOWN, RIGHT, UP, LEFT = 0, 1, 2, 3

step_dir = 6

# -- TRACK -- #
road_path = "images/road/"

track_part = {
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

bot_possible_moves = {
    "ud": [UP, DOWN],
    "lr": [LEFT, RIGHT],
    "dr": [RIGHT, DOWN],
    "dl": [LEFT, DOWN],
    "ur": [UP, RIGHT],
    "ul": [UP, LEFT],
    "ulr": [UP, LEFT, RIGHT],
    "udr": [UP, DOWN, RIGHT],
    "udl": [UP, LEFT, DOWN],
    "dlr": [DOWN, LEFT, RIGHT],
}
