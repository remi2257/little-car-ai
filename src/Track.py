from src.const import *
import numpy as np
import pygame


class Track:
    def __init__(self, track_path, double_road=True):
        self.grid, self.grid_h, self.grid_w = parse_track_file(track_path)
        self.double_road = double_road

        self.grid_size = min(size_haut // self.grid_h, size_larg // self.grid_w)

        self.im_w = self.grid_size * self.grid_w
        self.im_h = self.grid_size * self.grid_h

        self.car_size = self.grid_size // (1 + int(self.double_road))

        self.grid_practicable = np.zeros((self.grid_h, self.grid_w), dtype=bool)
        self.start_spots = []


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


def parse_track_file_v1(track_path):
    with open(track_path) as f:
        lines_raw = f.readlines()
        lines = [line.strip() for line in lines_raw if line != "\n"]
        height = int(lines.pop(0).split(" ")[-1])
        width = int(lines.pop(0).split(" ")[-1])
        lines.pop(0)
        grid = [line.split(" ") for line in lines]
    return grid, height, width


if __name__ == '__main__':
    import pygame.locals as pygame_const

    pygame.init()
    pygame.time.Clock().tick(30)

    pygame.display.set_caption("My Game")

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
