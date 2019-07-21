import numpy as np
import pygame

from src.const import *


class Track:
    def __init__(self, track_path, double_road=True):
        self.grid, self.grid_h, self.grid_w = parse_track_file(track_path)
        self.speed_max = speed_max_raw / max(self.grid_h, self.grid_w)

        self.double_road = double_road

        self.grid_size = min(size_haut // self.grid_h, size_larg // self.grid_w)

        self.im_w = self.grid_size * self.grid_w
        self.im_h = self.grid_size * self.grid_h

        self.car_size = self.grid_size // (1 + int(self.double_road))

        self.grid_practicable = np.zeros((self.grid_h, self.grid_w), dtype=bool)
        self.start_spots_bot = []

        self.init_grid_practicable()

        # self.init_car_x = init_car_x
        # self.init_car_y = init_car_y
        self.init_car_grid_x, self.init_car_grid_y, self.start_direction = self.look_for_start_point()
        self.init_car_x = (0.5 + self.init_car_grid_x) * self.grid_size
        self.init_car_y = (0.5 + self.init_car_grid_y) * self.grid_size

        # Checkpoints
        self.checkpoints = [[self.init_car_grid_y, self.init_car_grid_x]]  # Grid Coordinates - Not x/y
        self.last_checkpoint_id = 0

    def init_grid_practicable(self):
        for i in range(self.grid_h):
            for j in range(self.grid_w):
                small_name = self.grid[i][j]
                if "x" in small_name:
                    continue

                self.start_spots_bot.append([i, j])
                self.grid_practicable[i][j] = True

    def look_for_start_point(self):
        sum_add = 0
        while True:
            sum_add += 1
            for j in reversed(range(min(sum_add, self.grid_w))):
                for i in range(min(sum_add - j, self.grid_h)):
                    if self.grid_practicable[i][j]:
                        if "u" in self.grid[i][j]:
                            direction = dir_UP
                        else:
                            direction = dir_RIGHT
                        return j, i, direction


def parse_track_file(track_path):
    try:
        with open(track_path) as f:
            lines_raw = f.readlines()
            lines = [line.strip() for line in lines_raw if line != "\n"]
            grid = [line.split(" ") for line in lines]
    except FileNotFoundError as e:
        import sys
        print(e, "Bye bye")
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
    import pygame.locals as pygame_const

    pygame.init()
    pygame.time.Clock().tick(30)

    pygame.display.set_caption("My GamePlay")

    window = pygame.display.set_mode((size_larg, size_haut), )  # RESIZABLE

    background_path = "images/background.jpg"
    background_im = pygame.image.load(background_path).convert()

    track = Track("track/track1.tra", background_im)
    print(track.grid)

    window.blit(background_im, (0, 0))

    stop = False
    # Boucle infinie
    while not stop:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                stop = True  # On arrête la boucle

        pygame.display.flip()
