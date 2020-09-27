"""

import random

import pygame

from src.const import *

Pas utilisé en ce moment mais fonctionnel
"""

"""

class CarBot:
    def __init__(self, track, path_img="images/vehicles/car_bot.png"):
        # -- INIT IMAGES ---- #

        img = pygame.image.load(path_img).convert_alpha()
        width = img.get_width()
        height = img.get_height()
        ratio = float(width / height)
        car_max_len = track.__car_size
        self.double_road = track.__double_road
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

        # -- INIT Rest ---- #
        self.y_grid, self.x_grid = track.start_spots.pop(0)

        self.direction = -1

        self.next_direction = -1

        self.get_first_dir(track.grid)

        self.actual_img = self.imgs[self.direction]

        self.position_car = self.actual_img.get_rect()

        yc = self.y_grid * track.__case_size + track.__case_size // 2
        xc = self.x_grid * track.__case_size + track.__case_size // 2
        if self.double_road:
            xc, yc = self.adjust_double_road(xc, yc, track.__case_size)
        # y_init = yc - self.position_car.height // 2
        # x_init = xc - self.position_car.width // 2
        self.position_car = self.position_car.move(xc - self.position_car.centerx, yc - self.position_car.centery)

        self.can_change_dir = False  # IN NEW CASE

    def get_first_dir(self, grid):
        possible_moves = bot_possible_moves_1w[grid[self.y_grid][self.x_grid]]
        self.direction = possible_moves[random.randrange(len(possible_moves))]

    def adjust_double_road(self, xc, yc, grid_size):
        if self.direction == dir_LEFT:
            yc -= grid_size // 4
        elif self.direction == dir_RIGHT:
            yc += grid_size // 4
        elif self.direction == dir_UP:
            xc += grid_size // 4
        elif self.direction == dir_DOWN:
            xc -= grid_size // 4

        return xc, yc

    def actualize_direction_bot(self, grid_size):
        change = False
        if self.next_direction == dir_DOWN:
            dist_from_turn = abs(grid_size // 4 - self.position_car.centerx % grid_size)
            if dist_from_turn < 0.6 * step_dir:
                change = True
        elif self.next_direction == dir_UP:
            dist_from_turn = abs(3 * grid_size // 4 - self.position_car.centerx % grid_size)
            if dist_from_turn < 0.6 * step_dir:
                change = True
        elif self.next_direction == dir_RIGHT:
            dist_from_turn = abs(3 * grid_size // 4 - self.position_car.centery % grid_size)
            if dist_from_turn < 0.6 * step_dir:
                change = True
        elif self.next_direction == dir_LEFT:
            dist_from_turn = abs(grid_size // 4 - self.position_car.centery % grid_size)
            if dist_from_turn < 0.6 * step_dir:
                change = True

        if change:
            self.direction = self.next_direction
            self.actual_img = self.imgs[self.direction]
            new_rect = self.actual_img.get_rect()
            self.position_car = new_rect.move(self.new_pos(new_rect))

    def get_next_dir(self, grid):
        possible_moves = bot_possible_moves_1w[grid[self.y_grid][self.x_grid]].copy()

        opposite_dir = self.give_opposite_direction()
        possible_moves.remove(opposite_dir)
        # if possible_moves == [self.direction]:
        #     return False
        self.next_direction = possible_moves[random.randrange(len(possible_moves))]
        self.can_change_dir = False

    def move_car_bot(self, track):
        if self.can_change_dir:
            self.get_next_dir(track.grid)
        if self.next_direction != self.direction:  # Should Turn
            self.actualize_direction_bot(track.__case_size)

        if self.direction == dir_DOWN:
            self.position_car = self.position_car.move(0, step_dir)
        elif self.direction == dir_UP:
            self.position_car = self.position_car.move(0, -step_dir)

        elif self.direction == dir_RIGHT:
            self.position_car = self.position_car.move(step_dir, 0)

        elif self.direction == dir_LEFT:
            self.position_car = self.position_car.move(-step_dir, 0)

        new_case_x = self.position_car.centerx // track.__case_size
        new_case_y = self.position_car.centery // track.__case_size
        if new_case_x != self.x_grid:
            # dist_from_center = abs(track.grid_size // 2 - self.position_car.centerx % track.grid_size)
            # if dist_from_center < step_dir:
            self.x_grid = new_case_x
            self.can_change_dir = True
        elif new_case_y != self.y_grid:
            # dist_from_center = abs(track.grid_size // 2 - self.position_car.centery % track.grid_size)
            # if dist_from_center < step_dir:
            self.y_grid = new_case_y
            self.can_change_dir = True

    def get_position_left_top(self):
        return tuple([self.position_car.x,
                      self.position_car.y])

    def get_position_center(self):
        return tuple([self.position_car.centerx,
                      self.position_car.centery])

    def new_pos(self, new_rect):
        return tuple([self.position_car.centerx - new_rect.rect_w // 2,
                      self.position_car.centery - new_rect.h // 2])

    def give_opposite_direction(self):
        return (self.direction + 2) % 4


    """
