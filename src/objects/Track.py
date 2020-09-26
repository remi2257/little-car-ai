import numpy as np
import pygame

from src.const import *


class Track:
    def __init__(self, track_path, double_road=True):
        # Open and parse track file
        self.__grid_raw, self.__grid_h, self.__grid_w = parse_track_file(track_path)

        # Longeur & Largeur d'une case
        self.__case_size = min(big_window_haut // self.__grid_h, big_window_larg // self.__grid_w)

        # Taille de l'affichage du circuit
        self.im_w = self.__case_size * self.__grid_w
        self.im_h = self.__case_size * self.__grid_h

        # --Car--#
        self.__speed_max = speed_max_raw / max(self.__grid_h, self.__grid_w)
        self.__double_road = double_road  # If double road, car are 2 times less wide than road
        self.__car_size = self.__case_size // (1 + int(self.__double_road))

        # - Infos on track
        self.__grid_practicable, self.__checkpoints = self.init_grid_n_checkp()
        self.__last_checkpoint_id = 0

        # Init position of cars
        self.init_car_grid_x, self.init_car_grid_y, self.start_direction = self.look_for_start_point()
        self.init_car_x = (0.5 + self.init_car_grid_x) * self.__case_size
        self.init_car_y = (0.5 + self.init_car_grid_y) * self.__case_size

    def init_grid_n_checkp(self):
        grid_practicable = np.zeros((self.__grid_h, self.__grid_w), dtype=bool)
        checkpoints = []
        for i in range(self.__grid_h):
            for j in range(self.__grid_w):
                small_name = self.__grid_raw[i][j]
                if "x" in small_name:
                    continue
                # self.start_spots_bot.append([i, j])
                grid_practicable[i][j] = True
                if "c" in small_name:
                    # self.__grid_raw[i][j] = self.__grid_raw[i][j][:-1]
                    checkpoints.append([i, j])

        if len(checkpoints) == 1:
            checkpoints = []
        return grid_practicable, checkpoints

    def look_for_start_point(self):
        sum_add = 0
        while True:
            sum_add += 1
            for j in reversed(range(min(sum_add, self.__grid_w))):
                for i in range(min(sum_add - j, self.__grid_h)):
                    if self.__grid_practicable[i][j]:
                        if "u" in self.__grid_raw[i][j]:
                            direction = dir_UP
                        else:
                            direction = dir_RIGHT
                        return j, i, direction

    @property
    def grid_h(self):
        return self.__grid_h

    @property
    def grid_w(self):
        return self.__grid_w

    @property
    def case_size(self):
        return self.__case_size

    @property
    def car_size(self):
        return self.__car_size

    def get_road_name(self, i, j):
        return self.__grid_raw[i][j]

    @property
    def lidar_case_size(self):
        return self.__case_size // (1 + int(self.__double_road))

    @property
    def speed_max(self):
        return self.__speed_max

    @property
    def checkpoints(self):
        return self.__checkpoints

    def gen_track_background(self, background):
        # start_points = []
        # Browse Track
        for i in range(self.grid_h):
            for j in range(self.grid_w):
                small_name = self.__grid_raw[i][j]
                if "x" in small_name:  # If grass, background already good
                    continue

                im_name = roads_path + "road_{}.png".format(small_name)
                im = pygame.image.load(im_name).convert_alpha()
                im = pygame.transform.scale(im, (self.case_size, self.case_size))

                background.blit(im, (self.case_size * j, self.case_size * i))


def parse_track_file(track_path):
    try:
        with open(track_path) as f:
            lines_raw = f.readlines()
            grid = [line.strip().split() for line in lines_raw if line != "\n"]
    except FileNotFoundError as e:
        import sys
        print(e, "Check path is good")
        sys.exit(3)
    return grid, len(grid), len(grid[0])


class Checkpoint:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        if direction in [dir_DOWN, dir_UP]:
            self.orientation = dir_RIGHT
        else:
            self.orientation = dir_DOWN

        self.line = None

    def line_crossed(self):
        pass


if __name__ == '__main__':
    from src.const import background_path
    import pygame.locals as pygame_const
    from src.usesful_func import start_pygame, should_stop_pygame

    track_ = Track("tracks/Legendary_1.tra")
    # print(track_.grid_raw)

    start_pygame()

    window = pygame.display.set_mode((big_window_larg, big_window_haut), )  # RESIZABLE

    background_im = pygame.image.load(background_path).convert()
    track_.gen_track_background(background_im)

    window.blit(background_im, (0, 0))

    stop = False
    while not stop:
        for event in pygame.event.get():
            if should_stop_pygame(event):
                stop = True

        pygame.display.flip()
