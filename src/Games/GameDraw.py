import numpy as np
import pygame

from src.const import *


class GameDraw:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption(game_name)

        self.grid_h = draw_h_grid
        self.grid_w = draw_w_grid

        self.grid_size = min(big_window_haut // self.grid_h, big_window_larg // self.grid_w)

        self.im_w = self.grid_size * self.grid_w
        self.im_h = self.grid_size * self.grid_h

        self.grid_practicable = np.zeros((self.grid_h, self.grid_w), dtype=bool)
        self.grid_cut = None
        self.grid_cut = None

        self.missing_parts = np.zeros((self.grid_h, self.grid_w), dtype=bool)

        self.grid_checkpoints = np.zeros((self.grid_h, self.grid_w), dtype=bool)
        self.grid_checkpoints_cut = None
        self.should_put_checkpoint = False

        # Generate Window
        self.window_w = self.im_w
        self.window_h = self.im_h

        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        # Mouse infos
        self.last_x = 0
        self.last_y = 0
        self.is_holding_left = False

        # Font
        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.msg_text = None
        self.text_duration = 0

        # Generate Background
        self.background = pygame.image.load(background_path).convert()

        # self.button_save = ButtonPress(self.im_w - 3 * self.grid_size, self.im_h - 3 * self.grid_size,
        #                                action=self.save_map,
        #                                path_img_off=button_save_off,
        #                                path_img_push=button_save_on,
        #                                button_w=3 * self.grid_size)
        self.already_save = False

        self.gen_track_background()

        self.actualize()

        # For Saving
        from random import choice
        self.track_id = 0
        self.track_raw_name = choice(track_names_list)
        self.track_name = "track/{}_{}.tra".format(self.track_raw_name, self.track_id)

    def actualize(self, pos=None):
        self.window.blit(self.background, (0, 0))
        if pos:
            mouse_x = pos[0]
            mouse_y = pos[1]
            new_x = mouse_x // self.grid_size
            new_y = mouse_y // self.grid_size

            if self.is_holding_left: # If button is pushed
                if not (new_y == self.last_y and new_x == self.last_x): # Si on est pas au même endroit qu'avant
                    if new_y != 0 and new_x != 0 and new_y != self.grid_h - 1 and new_x != self.grid_w - 1:
                        # si on est pas sur les bords
                        self.grid_practicable[new_y][new_x] = not self.grid_practicable[new_y][new_x]
                self.last_x = new_x
                self.last_y = new_y
            else:
                self.already_save = False

            # if self.button_save.mouse_on_button(mouse_x, mouse_y):
            #     if self.is_holding_left and not self.already_save:
            #         self.button_save.run_action()
            #         self.already_save = True

            if self.should_put_checkpoint:
                self.grid_practicable[new_y][new_x] = True

                self.grid_checkpoints[new_y][new_x] = not self.grid_checkpoints[new_y][new_x]
                self.should_put_checkpoint = False

        for i in range(self.grid_h):
            for j in range(self.grid_w):

                if self.missing_parts[i][j]:
                    rect_pos = tuple([self.grid_size * j, self.grid_size * i,
                                      self.grid_size, self.grid_size])
                    pygame.draw.rect(self.window, COLOR_RED, rect_pos)

                elif self.grid_checkpoints[i][j]:
                    rect_pos = tuple([self.grid_size * j, self.grid_size * i,
                                      self.grid_size, self.grid_size])
                    pygame.draw.rect(self.window, COLOR_BLUE_BRIGHT, rect_pos)

                elif self.grid_practicable[i][j]:
                    rect_pos = tuple([self.grid_size * j, self.grid_size * i,
                                      self.grid_size, self.grid_size])
                    pygame.draw.rect(self.window, (50, 50, 50), rect_pos)

        # self.button_save.draw_button_image(self.background)

        self.display_text()

        # pygame.display.update()
        pygame.display.flip()

    def gen_track_background(self):
        # Generate Track
        for i in range(self.grid_h):
            line_h_start = [0, i * self.grid_size]
            line_h_stop = [self.im_w, i * self.grid_size]
            pygame.draw.line(self.background, (0, 0, 0), line_h_start, line_h_stop)
        for i in range(self.grid_w):
            line_w_start = [i * self.grid_size, 0]
            line_w_stop = [i * self.grid_size, self.im_h]
            pygame.draw.line(self.background, (0, 0, 0), line_w_start, line_w_stop)

        # self.button_save.draw_button_image(self.background)

        msg = self.font.render("C : Checkpoint   F : Free   S : Save", True, COLOR_RED)
        self.background.blit(msg, (40, self.im_h - self.grid_size))

    def save_map(self):
        import os
        self.missing_parts = np.zeros((self.grid_h, self.grid_w), dtype=bool)

        if not self.check_viable_track():
            self.msg_text = "Circuit pas viable, toutes les cases doivent avoir au mina 2 connexions"
            return None

        self.cut_grids()

        while os.path.isfile(self.track_name):
            self.track_id += 1
            self.track_name = "track/{}_{}.tra".format(self.track_raw_name, self.track_id)

        h, w = self.grid_cut.shape

        grid_reconstruct1 = np.zeros((self.grid_h, self.grid_w), dtype='object')
        grid_reconstruct_final = np.zeros((self.grid_h, self.grid_w), dtype='object')

        for i in range(h):
            for j in range(w):
                if not self.grid_cut[i][j]:
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

                if self.grid_checkpoints_cut[i][j]:
                    grid_reconstruct_final[i][j] += "c"

        file_track = open(self.track_name, "w+")

        for i in range(h):
            for j in range(w):
                file_track.write(grid_reconstruct_final[i][j])

                file_track.write(" ")
            file_track.write("\n")

        self.msg_text = "Track recorded as {}".format(self.track_name.split("/")[1])
        file_track.close()

    def check_viable_track(self):
        if not np.any(self.grid_practicable):
            return False
        missing_part = False
        for i in range(1, self.grid_h - 1):
            for j in range(1, self.grid_w - 1):
                if self.grid_practicable[i][j]:
                    connexion_count = 0
                    if self.grid_practicable[i][j - 1]:
                        connexion_count += 1
                    if self.grid_practicable[i][j + 1]:
                        connexion_count += 1

                    if self.grid_practicable[i - 1][j]:
                        connexion_count += 1

                    if self.grid_practicable[i + 1][j]:
                        connexion_count += 1

                    if connexion_count < 2:
                        missing_part = True
                        self.missing_parts[i][j] = True

        return not missing_part

    def cut_grids(self):
        self.grid_cut = self.grid_practicable.copy()
        self.grid_checkpoints_cut = self.grid_checkpoints.copy()
        while not np.any(self.grid_cut[1]):  # On coupe en Haut
            self.grid_cut = np.delete(self.grid_cut, 0, axis=0)
            self.grid_checkpoints_cut = np.delete(self.grid_checkpoints_cut, 0, axis=0)

        while not np.any(self.grid_cut[-2]):  # On coupe en Bas
            self.grid_cut = np.delete(self.grid_cut, -1, axis=0)
            self.grid_checkpoints_cut = np.delete(self.grid_checkpoints_cut, -1, axis=0)

        while not np.any(self.grid_cut[:, 1]):  # On coupe à gauche
            self.grid_cut = np.delete(self.grid_cut, 0, axis=1)
            self.grid_checkpoints_cut = np.delete(self.grid_checkpoints_cut, 0, axis=1)

        while not np.any(self.grid_cut[:, -2]):  # On coupe à droite
            self.grid_cut = np.delete(self.grid_cut, -1, axis=1)
            self.grid_checkpoints_cut = np.delete(self.grid_checkpoints_cut, -1, axis=1)

    def find_izi_piece(self, i, j):
        part_str = ""
        if self.grid_cut[i - 1][j]:
            part_str += "u"
        if self.grid_cut[i + 1][j]:
            part_str += "d"
        if self.grid_cut[i][j - 1]:
            part_str += "l"
        if self.grid_cut[i][j + 1]:
            part_str += "r"

        return part_str

    def free_map(self):
        self.grid_practicable = np.zeros((self.grid_h, self.grid_w), dtype=bool)

    def checkpoint_cmd(self):
        self.should_put_checkpoint = True

    def display_text(self):
        if self.msg_text is not None:
            msg = self.font.render(self.msg_text, True, COLOR_RED)
            self.window.blit(msg, (40, 40))
            self.text_duration += 1
            if self.text_duration > 240:
                self.msg_text = None
                self.text_duration = 0
