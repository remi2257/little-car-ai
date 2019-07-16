from play_ai import run_play_ai
from play_human import run_play_human
from start_draw_map import run_draw_map
from start_menu import run_menu
from start_train import run_train
from src.const import *

# --- INIT Variables--- #

stop = False
ret_menu = 0

actual_state = state_MENU

while not stop:
    if actual_state == state_MENU:
        ret_menu = run_menu()
        if ret_menu == 0:
            stop = True
        else:
            actual_state = ret_menu

    else:
        if actual_state == state_HUMAN:
            run_play_human()
        elif actual_state == state_AI:
            run_play_ai()
        elif actual_state == state_TRAIN:
            run_train()
        elif actual_state == state_DRAW:
            run_draw_map()

        actual_state = state_MENU

