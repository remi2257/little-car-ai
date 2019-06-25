import random
from src.const import *
import pygame


class Car:
    def __init__(self, path_img="images/vehicles/Audi.png"):
        self.x = size_larg // 2
        self.y = size_haut // 2

        img = pygame.image.load(path_img).convert_alpha()
        width = img.get_width()
        height = img.get_height()
        ratio = float(width / height)
        if ratio < 1:
            self.width = car_max_len
            self.height = int(car_max_len * ratio)
        else:
            self.height = car_max_len
            self.width = int(car_max_len / ratio)

        img_resize = pygame.transform.scale(img, (self.height, self.width))

        self.up = img_resize
        # self.down = img_resize
        self.left = pygame.transform.rotate(img_resize, 90)
        self.down = pygame.transform.rotate(img_resize, 180)
        self.right = pygame.transform.rotate(img_resize, 270)

        self.imgs = [self.down, self.right, self.up, self.left]

        self.direction = RIGHT

        self.actual_img = self.imgs[self.direction]

        # self.position_car = self.actual_img.get_rect()

    def actualize_direction(self, new_dir):
        self.direction = new_dir
        self.actual_img = self.imgs[self.direction]

    def move_car(self):
        if self.direction == DOWN:
            # self.position_car = self.position_car.move(0, step_dir)
            self.y += step_dir
        elif self.direction == UP:
            self.y -= step_dir
            # self.position_car = self.position_car.move(0, -step_dir)
        elif self.direction == RIGHT:
            self.x += step_dir
            # self.position_car = self.position_car.move(step_dir, 0)
        elif self.direction == LEFT:
            self.x -= step_dir
            # self.position_car = self.position_car.move(-step_dir, 0)


class CarBot: #TODO Ajuster le centre de masse pour que la voiture apparaisse au bon endroit : get_rect() ?
    def __init__(self, track, path_img="images/vehicles/car_bot.png"):
        self.y_grid, self.x_grid = track.start_spots.pop(0)


        img = pygame.image.load(path_img).convert_alpha()
        width = img.get_width()
        height = img.get_height()
        ratio = float(width / height)
        if ratio < 1:
            self.width = car_max_len
            self.height = int(car_max_len * ratio)
        else:
            self.height = car_max_len
            self.width = int(car_max_len / ratio)

        img_resize = pygame.transform.scale(img, (self.height, self.width))

        self.up = img_resize
        self.left = pygame.transform.rotate(img_resize, 90)
        self.down = pygame.transform.rotate(img_resize, 180)
        self.right = pygame.transform.rotate(img_resize, 270)

        self.imgs = [self.down, self.right, self.up, self.left]

        possible_moves = bot_possible_moves[track.track_grid[self.y_grid][self.x_grid]]
        self.direction = possible_moves[random.randrange(len(possible_moves))]

        self.actual_img = self.imgs[self.direction]

        # self.position_car = self.actual_img.get_rect()

        self.can_change_dir = True

        self.y = self.y_grid * track.grid_size
        self.x = self.x_grid * track.grid_size

    def actualize_direction_bot(self, track_grid):
        change = self.get_next_dir(track_grid)

        if change:
            self.actual_img = self.imgs[self.direction]
            self.can_change_dir = False

    def get_next_dir(self, track_grid):
        if not self.can_change_dir:
            return False

        possible_moves = bot_possible_moves[track_grid[self.y_grid][self.x_grid]].copy()

        opposite_dir = give_opposite_direction(self.direction)
        possible_moves.remove(opposite_dir)
        len_possible_moves = len(possible_moves)
        self.direction = possible_moves[random.randrange(len_possible_moves)]
        return True

    def move_car_bot(self, track):
        self.actualize_direction_bot(track.track_grid)

        if self.direction == DOWN:
            # self.position_car = self.position_car.move(0, step_dir)
            self.y += step_dir
            new_case_y = self.y // track.grid_size
            if new_case_y != self.y_grid:
                self.y_grid = new_case_y
                self.can_change_dir = True
        elif self.direction == UP:
            self.y -= step_dir
            new_case_y = self.y // track.grid_size
            if new_case_y != self.y_grid:
                self.y_grid = new_case_y
                self.can_change_dir = True
        elif self.direction == RIGHT:
            self.x += step_dir
            new_case_x = self.x // track.grid_size
            if new_case_x != self.x_grid:
                self.x_grid = new_case_x
                self.can_change_dir = True
        elif self.direction == LEFT:
            self.x -= step_dir
            new_case_x = self.x // track.grid_size
            if new_case_x != self.x_grid:
                self.x_grid = new_case_x
                self.can_change_dir = True

    def get_mass_center(self):
        y_m = self.y - self.height//2
        x_m = self.x - self.width//2

        return y_m,x_m


def give_opposite_direction(direction):
    return (direction + 2) % 4
