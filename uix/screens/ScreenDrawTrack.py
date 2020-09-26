import pygame
import numpy as np
# import os
from random import choice
from enum import Enum

from uix.screens.ScreenBase import ScreenBase
from src.const import *

GRID_HEIGHT = 24
GRID_WIDTH = 32

track_names_list = [
    "hardcore_track",
    "Legendary",
    "Stronger",
    "Better",
    "Faster",
]


class Grid:
    class Case(Enum):
        MISSING = -2
        GRASS = -1
        ROAD = 1
        CHECKPOINT = 2

    colors_dict = {
        Case.MISSING: COLOR_RED,
        Case.ROAD: (50, 50, 50),
        Case.CHECKPOINT: COLOR_BLUE_BRIGHT,
    }

    def __init__(self, grid_h, grid_w):
        self.__grid = np.zeros((grid_h, grid_w), dtype=object)
        self.__missing_grid = np.zeros((grid_h, grid_w), dtype=bool)
        self.clean_grid()

    def clean_grid(self):
        for i in range(self.__grid.shape[0]):
            for j in range(self.__grid.shape[1]):
                self.__grid[i][j] = Grid.Case.GRASS
        self.reset_missing()

    def reset_missing(self):
        self.__missing_grid.fill(False)

    def is_practicable(self, i, j):
        return self.__grid[i][j].value > 0

    def is_road(self, i, j):
        return self.__grid[i][j] == Grid.Case.ROAD

    def is_checkpoint(self, i, j):
        return self.__grid[i][j] == Grid.Case.CHECKPOINT

    def is_missing(self, i, j):
        return self.__grid[i][j] == Grid.Case.MISSING

    def is_grass(self, i, j):
        return self.__grid[i][j] == Grid.Case.GRASS

    def get_color(self, i, j):
        if self.__missing_grid[i][j]:
            return self.colors_dict[Grid.Case.MISSING]
        return self.colors_dict[self.__grid[i][j]]

    def invert_road_grass(self, i, j):
        val = self.__grid[i][j].value
        if val > 0:
            self.__grid[i][j] = Grid.Case.GRASS
        else:
            self.__grid[i][j] = Grid.Case.ROAD

    def set_unset_checkpoint(self, i, j):
        if self.__grid[i][j] != Grid.Case.CHECKPOINT:
            self.__grid[i][j] = Grid.Case.CHECKPOINT
        else:
            self.__grid[i][j] = Grid.Case.ROAD

    def set_as_missing(self, i, j):
        self.__missing_grid[i][j] = True

    @property
    def practicable(self):
        return np.where((self.__grid == Grid.Case.ROAD) | (self.__grid == Grid.Case.CHECKPOINT), True, False)

    @property
    def checkpoints(self):
        return np.where(self.__grid == Grid.Case.CHECKPOINT, True, False)


class ScreenDrawTrack(ScreenBase):
    def __init__(self):
        super(ScreenDrawTrack, self).__init__()

        # -- Init drawing settings
        self.__grid_height = GRID_HEIGHT
        self.__grid_width = GRID_WIDTH

        self.__grid_shape = min(big_window_haut // self.__grid_height, big_window_larg // self.__grid_width)

        self.__im_w = self.__grid_shape * self.__grid_width
        self.__im_h = self.__grid_shape * self.__grid_height

        # - Text
        self.__font = pygame.font.Font('freesansbold.ttf', 28)
        self.__msg_text = None
        self.__text_duration = 0

        # Generate Window
        self.__window_w = self.__im_w
        self.__window_h = self.__im_h

        self.__window = pygame.display.set_mode((self.__window_w, self.__window_h))

        # Generate Background
        self.__background = pygame.image.load(background_path).convert()
        self.__gen_track_background()

        # -- Grid manipulation arrays
        self.__grid = Grid(self.__grid_height, self.__grid_width)

        # True if next point is checkpoint
        self.__should_put_checkpoint = False

        self.__grid_cut = None
        self.__grid_checkpoints_cut = None

        # - Mouse infos
        self.__mouse_last_x = -1
        self.__mouse_last_y = -1

        # - Saving option
        self.__already_save = False

        # For Saving
        self.__track_id = 0
        self.__track_raw_name = choice(track_names_list)
        self.__track_name = ""

        # Finish init by generating the first image !
        self.actualize()

    # - Visualization

    def keydown_handle(self, key):
        if key == pygame_const.K_s:  # S : Save
            self.callback_save_map()
        elif key == pygame_const.K_f:  # F : Free
            self.free_map()
        elif key == pygame_const.K_c:  # C : Checkpoint
            self.checkpoint_cmd()

    def actualize(self, pos=None):
        self.__window.blit(self.__background, (0, 0))

        if pos:
            self._mouse_pos_effect(pos)

        for i in range(self.__grid_height):
            for j in range(self.__grid_width):
                if self.__grid.is_grass(i, j):
                    continue
                rect_pos = tuple([self.__grid_shape * j, self.__grid_shape * i,
                                  self.__grid_shape, self.__grid_shape])
                pygame.draw.rect(self.__window, self.__grid.get_color(i, j), rect_pos)

        # self.button_save.draw_button_image(self.background)

        self.display_text()

        # pygame.display.update()
        pygame.display.flip()

    def _mouse_pos_effect(self, pos):
        mouse_x = pos[0]
        mouse_y = pos[1]
        new_x = mouse_x // self.__grid_shape
        new_y = mouse_y // self.__grid_shape

        if self._mouse_is_holding_left:  # If button is pushed
            if self._mouse_has_moved(new_x, new_y):
                self.__grid.invert_road_grass(new_y, new_x)
            self.__mouse_last_x = new_x
            self.__mouse_last_y = new_y
        else:
            self.__already_save = False

        if self.__should_put_checkpoint:
            self.__grid.set_unset_checkpoint(new_y, new_x)
            self.__should_put_checkpoint = False

    def _mouse_has_moved(self, new_x, new_y):
        # Si on est pas au même endroit qu'avant
        if new_y == self.__mouse_last_y and new_x == self.__mouse_last_x:
            return False

        # si on est pas sur les bords
        if new_y == 0 or new_x == 0:
            return False
        if new_y == self.__grid_height - 1 or new_x == self.__grid_width - 1:
            return False

        return True

    def __gen_track_background(self):
        # Generate Track
        for i in range(self.__grid_height):
            line_h_start = [0, i * self.__grid_shape]
            line_h_stop = [self.__im_w, i * self.__grid_shape]
            pygame.draw.line(self.__background, (0, 0, 0), line_h_start, line_h_stop)
        for i in range(self.__grid_width):
            line_w_start = [i * self.__grid_shape, 0]
            line_w_stop = [i * self.__grid_shape, self.__im_h]
            pygame.draw.line(self.__background, (0, 0, 0), line_w_start, line_w_stop)

        # self.button_save.draw_button_image(self.background)

        msg = self.__font.render("C : Checkpoint   F : Free   S : Save", True, COLOR_RED)
        self.__background.blit(msg, (40, self.__im_h - self.__grid_shape))

    def display_text(self):
        if self.__msg_text is not None:
            msg = self.__font.render(self.__msg_text, True, COLOR_RED)
            self.__window.blit(msg, (40, 40))
            self.__text_duration += 1
            if self.__text_duration > 240:
                self.__msg_text = None
                self.__text_duration = 0

    # - Callbacks

    def on_mouse_release(self, **kwargs):
        super(ScreenDrawTrack, self).on_mouse_release()
        self.__mouse_last_x = self.__mouse_last_y = -1

    def callback_save_map(self):
        self.__save_map()

    def free_map(self):
        self.__grid.clean_grid()

    def checkpoint_cmd(self):
        self.__should_put_checkpoint = not self.__should_put_checkpoint

    # - Functions

    def __save_map(self):
        if not self.check_viable_track():
            self.__msg_text = "Circuit pas viable, toutes les cases doivent avoir au mina 2 connexions"
            return None

        # Erasing empty borders
        self.cut_grids()

        # Converting bool grid to strin grid
        grid_reconstruct_final = self.generate_str_map()

        # - Saving - #
        while not self.__track_name or os.path.isfile(self.__track_name):
            self.__track_id += 1
            self.__track_name = os.path.join(track_files_path,
                                             "{}_{}.tra".format(self.__track_raw_name, self.__track_id))

        file_track = open(self.__track_name, "w+")
        h, w = self.__grid_cut.shape

        for i in range(h):
            for j in range(w):
                raw_str = grid_reconstruct_final[i][j]
                clean_str = [" " + raw_str + " ", raw_str + " ", raw_str][len(raw_str) - 2]
                file_track.write(clean_str)

                file_track.write(" ")
            file_track.write("\n")

        self.__msg_text = "Track recorded as {}".format(self.__track_name.split("/")[1])
        file_track.close()

    def check_viable_track(self):
        self.__grid.reset_missing()
        grid_practicable = self.__grid.practicable
        if not np.any(grid_practicable):
            return False
        missing_part = False
        for i in range(1, self.__grid_height - 1):
            for j in range(1, self.__grid_width - 1):
                if grid_practicable[i][j]:
                    connexion_count = 0
                    if grid_practicable[i][j - 1]:
                        connexion_count += 1
                    if grid_practicable[i][j + 1]:
                        connexion_count += 1

                    if grid_practicable[i - 1][j]:
                        connexion_count += 1

                    if grid_practicable[i + 1][j]:
                        connexion_count += 1

                    if connexion_count < 2:
                        missing_part = True
                        self.__grid.set_as_missing(i, j)

        return not missing_part

    def cut_grids(self):
        self.__grid_cut = self.__grid.practicable
        self.__grid_checkpoints_cut = self.__grid.checkpoints
        while not np.any(self.__grid_cut[1]):  # On coupe en Haut
            self.__grid_cut = np.delete(self.__grid_cut, 0, axis=0)
            self.__grid_checkpoints_cut = np.delete(self.__grid_checkpoints_cut, 0, axis=0)

        while not np.any(self.__grid_cut[-2]):  # On coupe en Bas
            self.__grid_cut = np.delete(self.__grid_cut, -1, axis=0)
            self.__grid_checkpoints_cut = np.delete(self.__grid_checkpoints_cut, -1, axis=0)

        while not np.any(self.__grid_cut[:, 1]):  # On coupe à gauche
            self.__grid_cut = np.delete(self.__grid_cut, 0, axis=1)
            self.__grid_checkpoints_cut = np.delete(self.__grid_checkpoints_cut, 0, axis=1)

        while not np.any(self.__grid_cut[:, -2]):  # On coupe à droite
            self.__grid_cut = np.delete(self.__grid_cut, -1, axis=1)
            self.__grid_checkpoints_cut = np.delete(self.__grid_checkpoints_cut, -1, axis=1)

    def generate_str_map(self):
        h, w = self.__grid_cut.shape

        grid_reconstruct1 = np.zeros((self.__grid_height, self.__grid_width), dtype=object)
        grid_reconstruct_final = np.zeros((self.__grid_height, self.__grid_width), dtype=object)

        for i in range(h):
            for j in range(w):
                if not self.__grid_cut[i][j]:
                    grid_reconstruct1[i][j] = "xx"
                else:
                    grid_reconstruct1[i][j] = self.find_base_piece(i, j)

        for i in range(h):
            for j in range(w):
                val = grid_reconstruct1[i][j]
                grid_reconstruct_final[i][j] = val

                if val == "xx":
                    continue
                if val == 'dlr':
                    diag_right = False
                    diag_left = False
                    if grid_reconstruct1[i + 1][j + 1] != 'xx':
                        diag_right = True
                    if grid_reconstruct1[i + 1][j - 1] != 'xx':
                        diag_left = True

                    if diag_right:
                        if diag_left:
                            grid_reconstruct_final[i][j] = 'dlr3'
                        else:
                            grid_reconstruct_final[i][j] = 'dlr2'
                    elif diag_left:
                        grid_reconstruct_final[i][j] = 'dlr1'

                elif val == 'ulr':
                    diag_right = False
                    diag_left = False
                    if grid_reconstruct1[i - 1][j + 1] != 'xx':
                        diag_right = True
                    if grid_reconstruct1[i - 1][j - 1] != 'xx':
                        diag_left = True

                    if diag_right:
                        if diag_left:
                            grid_reconstruct_final[i][j] = 'ulr3'
                        else:
                            grid_reconstruct_final[i][j] = 'ulr2'
                    elif diag_left:
                        grid_reconstruct_final[i][j] = 'ulr1'

                elif val == 'udr':
                    diag_up = False
                    diag_down = False
                    if grid_reconstruct1[i - 1][j + 1] != 'xx':
                        diag_up = True
                    if grid_reconstruct1[i + 1][j + 1] != 'xx':
                        diag_down = True

                    if diag_up:
                        if diag_down:
                            grid_reconstruct_final[i][j] = 'udr3'
                        else:
                            grid_reconstruct_final[i][j] = 'udr1'
                    elif diag_down:
                        grid_reconstruct_final[i][j] = 'udr2'

                elif val == 'udl':
                    diag_up = False
                    diag_down = False
                    if grid_reconstruct1[i - 1][j - 1] != 'xx':
                        diag_up = True
                    if grid_reconstruct1[i + 1][j - 1] != 'xx':
                        diag_down = True

                    if diag_up:
                        if diag_down:
                            grid_reconstruct_final[i][j] = 'udl3'
                        else:
                            grid_reconstruct_final[i][j] = 'udl1'
                    elif diag_down:
                        grid_reconstruct_final[i][j] = 'udl2'

                elif val == 'ur':
                    if grid_reconstruct1[i - 1][j + 1] != 'xx':
                        grid_reconstruct_final[i][j] = 'ur1'
                elif val == 'dr':
                    if grid_reconstruct1[i + 1][j + 1] != 'xx':
                        grid_reconstruct_final[i][j] = 'dr1'
                elif val == 'ul':
                    if grid_reconstruct1[i - 1][j - 1] != 'xx':
                        grid_reconstruct_final[i][j] = 'ul1'
                elif val == 'dl':
                    if grid_reconstruct1[i + 1][j - 1] != 'xx':
                        grid_reconstruct_final[i][j] = 'dl1'

                if self.__grid_checkpoints_cut[i][j]:
                    grid_reconstruct_final[i][j] += "c"

        return grid_reconstruct_final

    def find_base_piece(self, i, j):
        part_str = ""
        if self.__grid_cut[i - 1][j]:
            part_str += "u"
        if self.__grid_cut[i + 1][j]:
            part_str += "d"
        if self.__grid_cut[i][j - 1]:
            part_str += "l"
        if self.__grid_cut[i][j + 1]:
            part_str += "r"

        return part_str


def run_draw_map(**_kwargs):
    ScreenDrawTrack().run()


if __name__ == '__main__':
    run_draw_map()
