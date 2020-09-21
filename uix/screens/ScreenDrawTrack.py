import pygame
import numpy as np
# import os
from random import choice
from enum import Enum

from src.const import *
from src.usesful_func import start_pygame, should_stop_pygame

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
        self.clean_grid()

    def clean_grid(self):
        for i in range(self.__grid.shape[0]):
            for j in range(self.__grid.shape[1]):
                self.__grid[i][j] = Grid.Case.GRASS

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
        return self.colors_dict[self.__grid[i][j]]

    def invert_case(self, i, j):
        val = self.__grid[i][j].value
        if val > 0:
            self.__grid[i][j] = Grid.Case.GRASS
        else:
            self.__grid[i][j] = Grid.Case.ROAD

    def set_as_checkpoint(self, i, j):
        self.__grid[i][j] = Grid.Case.CHECKPOINT

    @property
    def practicable(self):
        return np.where(self.__grid in [Grid.Case.ROAD, Grid.Case.CHECKPOINT], True, False)

    @property
    def checkpoints(self):
        return np.where(self.__grid == Grid.Case.CHECKPOINT, True, False)


class ScreenDrawTrack:
    def __init__(self):
        start_pygame()

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
        # # Grid practicable contains whereas each case contains road (True) or grass (False)
        # self.__grid_practicable = Grid(self.__grid_height, self.__grid_width)
        # # Grid containing missing circuit part
        # self.__missing_parts = self.generate_grid_false()
        # # Grid contraining checkpoint
        # self.__grid_checkpoints = self.generate_grid_false()

        self.__grid = Grid(self.__grid_height, self.__grid_width)

        # True if next point is checkpoint
        self.__should_put_checkpoint = False

        self.__grid_cut = None
        self.__grid_checkpoints_cut = None

        # - Mouse infos
        self.__mouse_last_x = 0
        self.__mouse_last_y = 0
        self.__mouse_is_holding_left = False

        # - Saving option
        self.__already_save = False

        # For Saving
        self.__track_id = 0
        self.__track_raw_name = choice(track_names_list)
        self.__track_name = "track/{}_{}.tra".format(self.__track_raw_name, self.__track_id)
        # self.button_save = ButtonPress(self.im_w - 3 * self.grid_size, self.im_h - 3 * self.grid_size,
        #                                action=self.__save_map,
        #                                path_img_off=button_save_off,
        #                                path_img_push=button_save_on,
        #                                button_w=3 * self.grid_size)

        # Finish init by generating the first image !
        self.actualize()

    # - Visualization

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

        if self.__mouse_is_holding_left:  # If button is pushed
            if self._mouse_has_moved(new_x, new_y):
                # self.__grid_practicable[new_y][new_x] = not self.__grid_practicable[new_y][new_x]
                self.__grid.invert_case(new_y, new_x)
            self.__mouse_last_x = new_x
            self.__mouse_last_y = new_y
        else:
            self.__already_save = False

        # if self.button_save.mouse_on_button(mouse_x, mouse_y):
        #     if self.is_holding_left and not self.already_save:
        #         self.button_save.run_action()
        #         self.already_save = True

        if self.__should_put_checkpoint:
            # self.__grid_practicable[new_y][new_x] = True
            self.__grid.set_as_checkpoint(new_y, new_x)
            # self.__grid_checkpoints[new_y][new_x] = not self.__grid_checkpoints[new_y][new_x]
            self.__should_put_checkpoint = False

    def _mouse_has_moved(self, new_x, new_y):
        # Si on est pas au même endroit qu'avant
        if new_y == self.__mouse_last_y or new_x == self.__mouse_last_x:
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

    # - Callbacks

    def mouse_on_release(self):
        self.__mouse_is_holding_left = False
        self.__mouse_last_x = self.__mouse_last_y = -1

    def mouse_on_press(self):
        self.__mouse_is_holding_left = True

    def callback_save_map(self):
        self.__save_map()

    def free_map(self):
        self.__grid.clean_grid()

    def checkpoint_cmd(self):
        self.__should_put_checkpoint = not self.__should_put_checkpoint

    # - Functions

    def __save_map(self):
        self.__missing_parts = np.zeros((self.__grid_height, self.__grid_width), dtype=bool)

        if not self.check_viable_track():
            self.__msg_text = "Circuit pas viable, toutes les cases doivent avoir au mina 2 connexions"
            return None

        self.cut_grids()

        while os.path.isfile(self.__track_name):
            self.__track_id += 1
            self.__track_name = "track/{}_{}.tra".format(self.__track_raw_name, self.__track_id)

        h, w = self.__grid_cut.shape

        grid_reconstruct1 = np.zeros((self.__grid_height, self.__grid_width), dtype=object)
        grid_reconstruct_final = np.zeros((self.__grid_height, self.__grid_width), dtype=object)

        for i in range(h):
            for j in range(w):
                if not self.__grid_cut[i][j]:
                    grid_reconstruct1[i][j] = "xx"
                else:
                    grid_reconstruct1[i][j] = self.find_izi_piece(i, j)

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

        file_track = open(self.__track_name, "w+")

        for i in range(h):
            for j in range(w):
                file_track.write(grid_reconstruct_final[i][j])

                file_track.write(" ")
            file_track.write("\n")

        self.__msg_text = "Track recorded as {}".format(self.__track_name.split("/")[1])
        file_track.close()

    def generate_grid_false(self):
        return np.zeros((self.__grid_height, self.__grid_width), dtype=bool)

    def check_viable_track(self):
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
                        self.__missing_parts[i][j] = True

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

    def find_izi_piece(self, i, j):
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

    def display_text(self):
        if self.__msg_text is not None:
            msg = self.__font.render(self.__msg_text, True, COLOR_RED)
            self.__window.blit(msg, (40, 40))
            self.__text_duration += 1
            if self.__text_duration > 240:
                self.__msg_text = None
                self.__text_duration = 0


def run_draw_map(**_kwargs):
    # --- INIT Variable--- #

    stop = False

    # --- INIT Game--- #

    screen = ScreenDrawTrack()

    # Boucle infinie
    while not stop:
        # pygame.time.Clock().tick(240)
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            # Si un de ces événements est de type QUIT
            if should_stop_pygame(event):
                stop = True  # On arrête la boucle
            elif event.type == pygame_const.MOUSEBUTTONDOWN:
                screen.mouse_on_press()
            elif event.type == pygame_const.MOUSEBUTTONUP:
                screen.mouse_on_release()
            # if pygame.mouse.get_pressed()[0]:  # See if the user has clicked or dragged their mouse
            elif event.type == pygame_const.KEYDOWN:
                if event.key == pygame_const.K_s:  # S : Save
                    screen.callback_save_map()
                elif event.key == pygame_const.K_f:  # F : Free
                    screen.free_map()
                elif event.key == pygame_const.K_c:  # C : Checkpoint
                    screen.checkpoint_cmd()
        pos = pygame.mouse.get_pos()

        screen.actualize(pos)


if __name__ == '__main__':
    run_draw_map()
    # TODO : Refresh pas en live
    # Todo : Revoir le save
