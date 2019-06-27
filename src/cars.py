import random
from src.const import *
import pygame
from math import cos, sin, radians, exp
import numpy as np


class Car:
    def __init__(self, track, path_img="images/vehicles/Audi.png"):
        # INIT VARIABLES
        self.theta = 0.0
        self.speed = 0.0
        self.n_speed = 0.0
        # self.lidar_mat = np.zeros((height_LIDAR, width_LIDAR), dtype=str)
        self.lidar_mat = []
        self.lidar_filtered = []
        for _ in range(height_LIDAR):
            self.lidar_mat.append(width_LIDAR * [""])
            self.lidar_filtered.append(width_LIDAR * [False])

        # GEN CAR IMAGE
        img = pygame.image.load(path_img).convert_alpha()
        width = img.get_width()
        height = img.get_height()
        ratio = float(width / height)
        car_len = track.car_size
        if ratio < 1:
            width = car_len
            height = int(car_len * ratio)
        else:
            height = car_len
            width = int(car_len / ratio)

        img_resize = pygame.transform.scale(img, (height, width))
        self.img = pygame.transform.rotate(img_resize, 270.0)
        self.actual_img = self.img

        # SET POSITION
        self.position_car = self.actual_img.get_rect()

        self.position_car = self.position_car.move(150.0, 150.0)

        # GEN LIDAR
        self.track = track
        self.lidar_grid_car_x = width_LIDAR // 2
        self.lidar_grid_car_y = height_LIDAR - offset_LIDAR - 1
        self.refresh_LIDAR()

    def actualize_direction(self, new_dir):
        if new_dir == gas_ON:
            self.calculate_new_speed()
        elif new_dir == gas_BRAKE:
            self.calculate_new_speed(accelerate=False)
        else:
            if new_dir == dir_LEFT:
                self.calculate_new_angle(left=True)
            elif new_dir == dir_RIGHT:
                self.calculate_new_angle(left=False)

            self.actual_img = pygame.transform.rotate(self.img, self.theta)
            new_rect = self.actual_img.get_rect()
            self.position_car = new_rect.move(self.new_pos(new_rect))

    def calculate_new_speed(self, accelerate=True):
        if accelerate:
            self.n_speed += 1.0
        else:
            self.n_speed -= 1.0

        if self.n_speed > 0:
            self.speed = speed_max * (1 - exp(-self.n_speed / n0_speed))
        else:
            self.speed = - 0.25 * speed_max * (1 - exp(self.n_speed / n0_speed))

    def calculate_new_angle(self, left=True):
        if left:
            self.theta += step_angle
        else:
            self.theta -= step_angle

    def move_car(self, window=None):
        self.position_car = self.position_car.move(round(self.speed * cos(radians(self.theta))),
                                                   round(- self.speed * sin(radians(self.theta))))
        self.refresh_LIDAR(window)
        # print(np.array(self.lidar_mat))

    def get_position_left_top(self):
        return tuple([self.position_car.x,
                      self.position_car.y])

    def get_position_center(self):
        return tuple([self.position_car.centerx,
                      self.position_car.centery])

    def new_pos(self, new_rect):
        return tuple([self.position_car.centerx - new_rect.w // 2,
                      self.position_car.centery - new_rect.h // 2])

    def refresh_LIDAR(self, window=None):
        car_x, car_y = self.get_position_center()

        for i in range(height_LIDAR):
            for j in range(width_LIDAR):
                dx_rel_grid = (j - self.lidar_grid_car_x) * self.track.grid_size
                dy_rel_grid = (i - self.lidar_grid_car_y) * self.track.grid_size

                # /!\ I took theta = 0° when pointing left but the lidar map is pointing top
                dx_rel = dx_rel_grid * cos(radians(self.theta - 90)) + dy_rel_grid * sin(radians(self.theta - 90))
                dy_rel = -dx_rel_grid * sin(radians(self.theta - 90)) + dy_rel_grid * cos(radians(self.theta - 90))

                true_dx = dx_rel + car_x
                true_dy = dy_rel + car_y

                true_x_grid = int(true_dx // self.track.grid_size)
                true_y_grid = int(true_dy // self.track.grid_size)

                if 0 < true_x_grid < self.track.grid_w and 0 < true_y_grid < self.track.grid_h:
                    corresponding_square = self.track.track_grid[true_y_grid][true_x_grid]

                else:
                    corresponding_square = "xx"

                self.lidar_mat[i][j] = corresponding_square
                
                is_practicable = track_part_1w_practicable[corresponding_square]
                
                self.lidar_filtered[i][j] = is_practicable

                if window is not None:
                    if is_practicable:
                        pygame.draw.circle(window, (0, 255, 0), (
                            int(true_dx), int(true_dy)), 4, 2)
                    else :
                        pygame.draw.circle(window, (255, 0, 0), (
                            int(true_dx), int(true_dy)), 4, 2)


class CarBot:
    def __init__(self, track, path_img="images/vehicles/car_bot.png"):
        # -- INIT IMAGES ---- #

        img = pygame.image.load(path_img).convert_alpha()
        width = img.get_width()
        height = img.get_height()
        ratio = float(width / height)
        car_max_len = track.car_size
        self.double_road = track.double_road
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

        self.get_first_dir(track.track_grid)

        self.actual_img = self.imgs[self.direction]

        self.position_car = self.actual_img.get_rect()

        yc = self.y_grid * track.grid_size + track.grid_size // 2
        xc = self.x_grid * track.grid_size + track.grid_size // 2
        if self.double_road:
            xc, yc = self.adjust_double_road(xc, yc, track.grid_size)
        # y_init = yc - self.position_car.height // 2
        # x_init = xc - self.position_car.width // 2
        self.position_car = self.position_car.move(xc - self.position_car.centerx, yc - self.position_car.centery)

        self.can_change_dir = False  #  IN NEW CASE

    def get_first_dir(self, track_grid):
        possible_moves = bot_possible_moves_1w[track_grid[self.y_grid][self.x_grid]]
        self.direction = possible_moves[random.randrange(len(possible_moves))]

    def adjust_double_road(self, xc, yc, grid_size):
        if self.direction == bot_LEFT:
            yc -= grid_size // 4
        elif self.direction == bot_RIGHT:
            yc += grid_size // 4
        elif self.direction == bot_UP:
            xc += grid_size // 4
        elif self.direction == bot_DOWN:
            xc -= grid_size // 4

        return xc, yc

    def actualize_direction_bot(self, grid_size):
        change = False
        if self.next_direction == bot_DOWN:
            dist_from_turn = abs(grid_size // 4 - self.position_car.centerx % grid_size)
            if dist_from_turn < 0.6 * step_dir:
                change = True
        elif self.next_direction == bot_UP:
            dist_from_turn = abs(3 * grid_size // 4 - self.position_car.centerx % grid_size)
            if dist_from_turn < 0.6 * step_dir:
                change = True
        elif self.next_direction == bot_RIGHT:
            dist_from_turn = abs(3 * grid_size // 4 - self.position_car.centery % grid_size)
            if dist_from_turn < 0.6 * step_dir:
                change = True
        elif self.next_direction == bot_LEFT:
            dist_from_turn = abs(grid_size // 4 - self.position_car.centery % grid_size)
            if dist_from_turn < 0.6 * step_dir:
                change = True

        if change:
            self.direction = self.next_direction
            self.actual_img = self.imgs[self.direction]
            new_rect = self.actual_img.get_rect()
            self.position_car = new_rect.move(self.new_pos(new_rect))

    def get_next_dir(self, track_grid):
        possible_moves = bot_possible_moves_1w[track_grid[self.y_grid][self.x_grid]].copy()

        opposite_dir = give_opposite_direction(self.direction)
        possible_moves.remove(opposite_dir)
        # if possible_moves == [self.direction]:
        #     return False
        self.next_direction = possible_moves[random.randrange(len(possible_moves))]
        self.can_change_dir = False

    def move_car_bot(self, track):
        if self.can_change_dir:
            self.get_next_dir(track.track_grid)
        if self.next_direction != self.direction:  # Should Turn
            self.actualize_direction_bot(track.grid_size)

        if self.direction == bot_DOWN:
            self.position_car = self.position_car.move(0, step_dir)
        elif self.direction == bot_UP:
            self.position_car = self.position_car.move(0, -step_dir)

        elif self.direction == bot_RIGHT:
            self.position_car = self.position_car.move(step_dir, 0)

        elif self.direction == bot_LEFT:
            self.position_car = self.position_car.move(-step_dir, 0)

        new_case_x = self.position_car.centerx // track.grid_size
        new_case_y = self.position_car.centery // track.grid_size
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
        return tuple([self.position_car.centerx - new_rect.w // 2,
                      self.position_car.centery - new_rect.h // 2])


def give_opposite_direction(direction):
    return (direction + 2) % 4
