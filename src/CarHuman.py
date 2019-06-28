import random
from src.const import *
import pygame
from math import cos, sin, radians, exp
import numpy as np


class CarHuman:
    def __init__(self, track, lidar_w, lidar_h, path_img="images/vehicles/Audi.png"):
        # INIT VARIABLES
        self.theta = 0.0
        self.speed = 0.0
        self.n_speed = 0.0

        self.last_dir_cmd = dir_NONE
        self.last_gas_cmd = gas_OFF
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
        self.lidar_grid_size = track.grid_size // (1 + int(track.double_road))
        self.lidar_grid_car_x = width_LIDAR // 2
        self.lidar_grid_car_y = height_LIDAR - offset_LIDAR - 1

        self.lidar_w_img, self.lidar_h_img = lidar_w, lidar_h
        self.lidar_w_rect, self.lidar_h_rect = lidar_w // width_LIDAR, lidar_h // height_LIDAR
        self.refresh_LIDAR()

    def actualize_direction_and_gas(self, new_commands):
        for command in new_commands:
            self.actualize_direction_or_gas(command)

    def actualize_direction_or_gas(self, new_command):
        if new_command in [gas_OFF, gas_BRAKE, gas_ON]:
            if new_command == gas_ON:
                self.calculate_new_speed()
            elif new_command == gas_BRAKE:
                self.calculate_new_speed(accelerate=False)
            self.last_gas_cmd = new_command

        else:
            if new_command == dir_LEFT:
                self.calculate_new_angle(left=True)
            elif new_command == dir_RIGHT:
                self.calculate_new_angle(left=False)

            self.actual_img = pygame.transform.rotate(self.img, self.theta)
            new_rect = self.actual_img.get_rect()
            self.position_car = new_rect.move(self.new_pos(new_rect))
            self.last_dir_cmd = new_command

    def calculate_new_speed(self, accelerate=True):
        if accelerate:
            self.n_speed += 1.0
        else:
            self.n_speed = max(self.n_speed - 2.0, -10)

        if self.n_speed > 0:
            self.speed = speed_max * (1 - exp(-self.n_speed / n0_speed))
        else:
            self.speed = - 0.25 * speed_max * (1 - exp(self.n_speed / n0_speed))

    def calculate_new_angle(self, left=True):
        if left:
            self.theta += step_angle
        else:
            self.theta -= step_angle

    def move_car_and_refresh_window(self, window=None):
        # Car
        self.position_car = self.position_car.move(round(self.speed * cos(radians(self.theta))),
                                                   round(- self.speed * sin(radians(self.theta))))

        # Window
        self.refresh_LIDAR(window)

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
                dx_rel_grid = (j - self.lidar_grid_car_x) * self.lidar_grid_size
                dy_rel_grid = (i - self.lidar_grid_car_y) * self.lidar_grid_size

                # /!\ I took theta = 0° when pointing left but the lidar map is pointing top
                dx_rel = dx_rel_grid * cos(radians(self.theta - 90)) + dy_rel_grid * sin(radians(self.theta - 90))
                dy_rel = -dx_rel_grid * sin(radians(self.theta - 90)) + dy_rel_grid * cos(radians(self.theta - 90))

                true_dx = dx_rel + car_x
                true_dy = dy_rel + car_y

                true_x_grid = int(true_dx // self.track.grid_size)
                true_y_grid = int(true_dy // self.track.grid_size)

                if 0 < true_x_grid < self.track.grid_w and 0 < true_y_grid < self.track.grid_h:
                    corresponding_square = self.track.grid[true_y_grid][true_x_grid]

                else:
                    corresponding_square = "xx"

                self.lidar_mat[i][j] = corresponding_square

                is_practicable = track_part_1w_practicable[corresponding_square]

                self.lidar_filtered[i][j] = is_practicable

                if window is not None:
                    # Print Points & Result
                    point_pos = tuple([int(true_dx), int(true_dy)])
                    rect_pos = tuple([self.track.im_w + j * self.lidar_w_rect + erode_LIDAR_grid,
                                      offset_LIDAR_grid_y + i * self.lidar_h_rect + erode_LIDAR_grid,
                                      self.lidar_w_rect - 2 * erode_LIDAR_grid,
                                      self.lidar_h_rect - 2 * erode_LIDAR_grid])

                    if is_practicable:
                        color = COLOR_GREEN
                    else:
                        color = COLOR_RED

                    pygame.draw.circle(window, color, point_pos, 4, 2)
                    pygame.draw.rect(window, color, rect_pos)

        if window is not None:
            point_pos = tuple([round(self.track.im_w + (self.lidar_grid_car_x + 0.5) * self.lidar_w_rect),
                               offset_LIDAR_grid_y + round((self.lidar_grid_car_y + 0.5) * self.lidar_h_rect)])

            pygame.draw.circle(window, COLOR_BLUE, point_pos, 4, 2)