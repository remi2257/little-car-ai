from src.const import *
import pygame
import numpy as np


class GameDraw:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Little Car AI")

        self.grid_h = grid_h_lim
        self.grid_w = grid_w_lim

        self.grid_size = min(size_haut // self.grid_h, size_larg // self.grid_w)

        self.im_w = self.grid_size * self.grid_w
        self.im_h = self.grid_size * self.grid_h

        self.grid_practicable = np.zeros((self.grid_h, self.grid_w), dtype=bool)
        self.grid_cut = None

        # Generate Window
        self.window_w = self.im_w
        self.window_h = self.im_h

        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        # Generate Background
        self.background = pygame.image.load(background_path).convert()

        self.gen_track_background()

        # Mouse infos
        self.last_x = 0
        self.last_y = 0
        self.is_holding = False

        self.actualize()

        # For Saving
        from random import choice
        self.track_id = 0
        self.track_raw_name = choice(track_names_list)
        self.track_name = "track/{}_{}.tra".format(self.track_raw_name, self.track_id)

    def actualize(self, pos=None):
        self.window.blit(self.background, (0, 0))

        if self.is_holding and pos:
            new_x = pos[0] // self.grid_size
            new_y = pos[1] // self.grid_size
            if not (self.is_holding and new_y == self.last_y and new_x == self.last_x):
                if new_y != 0 and new_x != 0 and new_y != self.grid_h - 1 and new_x != self.grid_w - 1:
                    self.grid_practicable[new_y][new_x] = not self.grid_practicable[new_y][new_x]
            self.last_x = new_x
            self.last_y = new_y

        for i in range(self.grid_h):
            for j in range(self.grid_w):
                if self.grid_practicable[i][j]:
                    rect_pos = tuple([self.grid_size * j, self.grid_size * i,
                                      self.grid_size, self.grid_size])
                    pygame.draw.rect(self.window, (50, 50, 50), rect_pos)

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

    def save_map(self):
        import os

        if not self.check_viable_track():
            print("Circuit pas viable, toutes les cases doivent avoir au mina 2 connexions")
            return None

        self.cut_grid()

        while os.path.isfile(self.track_name):
            self.track_id += 1
            self.track_name = "track/{}_{}.tra".format(self.track_raw_name, self.track_id)

        file_track = open(self.track_name, "w+")
        h, w = self.grid_cut.shape

        for i in range(h):
            for j in range(w):
                if not self.grid_cut[i][j]:
                    file_track.write("xx")

                else:
                    file_track.write(self.find_adapted_piece(i, j))

                file_track.write(" ")
            file_track.write("\n")

        print("Track enregistré sous le nom de", self.track_name.split("/")[1])
        file_track.close()

    def check_viable_track(self):
        if not np.any(self.grid_practicable):
            return False
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
                        return False

        return True

    def cut_grid(self):
        self.grid_cut = self.grid_practicable.copy()
        while not np.any(self.grid_cut[1]):  # On coupe en Haut
            self.grid_cut = np.delete(self.grid_cut, 0, axis=0)

        while not np.any(self.grid_cut[-2]):  # On coupe en Bas
            self.grid_cut = np.delete(self.grid_cut, -1, axis=0)

        while not np.any(self.grid_cut[:, 1]):  # On coupe à gauche
            self.grid_cut = np.delete(self.grid_cut, 0, axis=1)

        while not np.any(self.grid_cut[:, -2]):  # On coupe à droite
            self.grid_cut = np.delete(self.grid_cut, -1, axis=1)

    def find_adapted_piece(self, i, j):
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

    def clean_map(self):
        self.grid_practicable = np.zeros((self.grid_h, self.grid_w), dtype=bool)
