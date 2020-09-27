import math
import pygame
from math import cos, sin, radians, exp
from enum import Enum
from src.const import *

from src.objects.LIDAR import LIDAR


class Command(Enum):
    pass


class CommandDir(Command):
    LEFT = 1
    NONE = 2
    RIGHT = 3


class CommandGas(Command):
    BRAKE = 1
    OFF = 2
    ON = 3


class Car:
    def __init__(self, track):
        # INIT VARIABLES
        self._track = track

        self._theta = 0.0
        self._speed = 0.0
        self._speed_max = track.speed_max
        self._x_speed = 0.0
        self._y_speed = 0.0
        self._rest_pos_x = 0.0
        self._rest_pos_y = 0.0
        self._n_speed = 0.0
        self._fitness = 0
        self._bonus_checkpoints = 0

        # Set startPosition
        self._x_init = track.init_car_x
        self._y_init = track.init_car_y

        # Count time outside road to penalize
        self._time_outside_road = 0
        self._on_road = True

        self._last_dir_cmd = CommandDir.NONE
        self._last_gas_cmd = CommandGas.OFF

        # GEN CAR IMAGE
        self._img = self._gen_car_img(path_audi)
        if track.start_direction == dir_RIGHT:
            self._img = pygame.transform.rotate(self._img, theta_0)

        self._actual_img = self._img

        # SET POSITION
        self._position_car = self._actual_img.get_rect()
        self._position_car = self._position_car.move(self._x_init, self._y_init)

        # GEN LIDAR
        self._lidar_case_size = self._track.lidar_case_size
        self._lidar_grid_car_x = width_grid_LIDAR // 2
        self._lidar_grid_car_y = height_grid_LIDAR - offset_y_LIDAR - 1

        self._lidar = LIDAR()

        self._refresh_lidar()

        # Checkpoints
        self._checkpoints = self.set_checkpoints()

    # Is aptly named
    def actualize_direction_and_gas(self, new_commands):
        for command in new_commands:
            self.actualize_direction_or_gas(command)

    def actualize_direction_or_gas(self, new_command):
        if isinstance(new_command, CommandGas):
            self.calculate_new_speed(new_command)
            self._last_gas_cmd = new_command

        elif isinstance(new_command, CommandDir):
            self.calculate_new_angle(new_command)

            self._actual_img = pygame.transform.rotate(self._img, self._theta)
            new_rect = self._actual_img.get_rect()
            self._position_car = new_rect.move(self.new_pos_after_turn(new_rect))
            self._last_dir_cmd = new_command

    def calculate_new_speed(self, command):
        if not self._on_road:
            if (1 - exp(-self._n_speed / n0_speed)) > 0.3:
                # If speed at more than 30% of the maximum
                # self.n_speed = self.n_speed - 4
                self._speed = max(self._speed * 0.70, 0)
                self.recalculate_n_speed()

        if command == CommandGas.OFF:
            self._speed = max(self._speed * 0.97, 0)
            self.recalculate_n_speed()

        elif command == CommandGas.BRAKE and self._speed > 1:
            self._speed = max(self._speed * 0.90, 0)
            self.recalculate_n_speed()
        else:

            if command == CommandGas.BRAKE:
                self._n_speed = max(self._n_speed - 2.0, -n0_speed / 2)

            else:  # if command == CommandGas.ON
                if self._on_road:
                    self._n_speed = min(self._n_speed + 1.0, max_n_speed)
                else:
                    self._n_speed = min(self._n_speed + .3, max_n_speed)

            if self._n_speed > 0:
                self._speed = self._speed_max * (1 - exp(-self._n_speed / n0_speed))
            else:
                self._speed = - 0.5 * self._speed_max * (1 - exp(self._n_speed / n0_speed))

    def recalculate_n_speed(self):
        if self._speed > 0:
            self._n_speed = -n0_speed * math.log2(1 - (self._speed / self._speed_max))
        else:
            self._n_speed = n0_speed * math.log2(1 - (self._speed / self._speed_max))

    def reduce_all_speeds(self, fact):
        self._speed = max(self._speed - fact, 0)
        self._x_speed = max(self._x_speed - fact, 0)
        self._y_speed = max(self._y_speed - fact, 0)

    def calculate_new_angle(self, command):
        if command == CommandDir.LEFT:
            self._theta += car_step_angle
        elif command == CommandDir.RIGHT:
            self._theta -= car_step_angle

        drift_fact = min(drift_factor_cst * math.pow(self._speed / self._speed_max, 2), drift_factor_max)
        self._x_speed = drift_fact * self._x_speed + (1 - drift_fact) * round(self._speed * cos(radians(self._theta)),
                                                                              6)
        self._y_speed = drift_fact * self._y_speed + (1 - drift_fact) * round(-self._speed * sin(radians(self._theta)),
                                                                              6)

    def move_car(self):
        # The fact is that pygame delete post comma digits
        # We save them !
        # print(50 * "*")
        # print("Before : {} / {}".format(self.rest_pos_x, self.rest_pos_y))
        self._rest_pos_x, x_move_int = math.modf(self._x_speed + self._rest_pos_x)
        self._rest_pos_y, y_move_int = math.modf(self._y_speed + self._rest_pos_y)

        # print("After : {} / {}".format(self.rest_pos_x, self.rest_pos_y))
        self._position_car = self._position_car.move(x_move_int,
                                                     y_move_int)

    def move_car_and_refresh_lidar(self):
        # Car
        self.move_car()
        # Lidar
        self._refresh_lidar()

        self._on_road = self._lidar.is_practicable(self._lidar_grid_car_y, self._lidar_grid_car_x)

    def get_position_left_top(self):
        return tuple([self._position_car.x,
                      self._position_car.y])

    def get_position_center(self):
        return tuple([self._position_car.centerx,
                      self._position_car.centery])

    def new_pos_after_turn(self, new_rect):
        return tuple([self._position_car.centerx - new_rect.w // 2,
                      self._position_car.centery - new_rect.h // 2])

    def reset_car(self):
        self._theta = 0.0
        self._speed = 0.0
        self._x_speed = 0.0
        self._y_speed = 0.0
        self._rest_pos_x = 0.0
        self._rest_pos_y = 0.0
        self._n_speed = 0.0
        self._fitness = 0
        self._bonus_checkpoints = 0
        self._time_outside_road = 0

        self._actual_img = pygame.transform.rotate(self._img, self._theta)
        new_rect = self._actual_img.get_rect()
        self._position_car = new_rect.move(self._x_init,
                                           self._y_init)

        self._refresh_lidar()

        self.reset_checkpoints()

    def _refresh_lidar(self):
        car_x, car_y = self.get_position_center()

        for i in range(height_grid_LIDAR):
            for j in range(width_grid_LIDAR):
                dx_rel_grid = (j - self._lidar_grid_car_x) * self._lidar_case_size
                dy_rel_grid = (i - self._lidar_grid_car_y) * self._lidar_case_size

                # /!\ I took theta = 0° when pointing left but the lidar map is pointing top
                dx_rel = dx_rel_grid * cos(radians(self._theta - 90.0)) + dy_rel_grid * sin(radians(self._theta - 90.0))
                dy_rel = -dx_rel_grid * sin(radians(self._theta - 90.0)) + dy_rel_grid * cos(
                    radians(self._theta - 90.0))

                true_x = round(dx_rel + car_x)
                true_y = round(dy_rel + car_y)

                true_x_grid = true_x // self._track.case_size
                true_y_grid = true_y // self._track.case_size

                if 0 < true_x_grid < self._track.grid_w and 0 < true_y_grid < self._track.grid_h:
                    road_type = self._track.get_road_name(true_y_grid, true_x_grid)

                else:
                    road_type = "xx"

                # is_practicable = track_part_1w_practicable[corresponding_square]
                is_practicable = "x" not in road_type

                self._lidar.refresh_case(i, j, road_type, is_practicable, [true_x, true_y])

    # ----Fitness & Checkpoints---#

    # Use some functions to calculate new fitness
    def refresh_fitness_v1(self):
        if self._on_road:
            self._fitness += max(self._speed, 0) * weight_on_road / FPS_MAX_init

            self._time_outside_road = max(0, self._time_outside_road - 0.1)
        else:
            self._time_outside_road += 1
            self._fitness -= 40 * (max(self._speed, 0) + weight_on_road + self._time_outside_road) / FPS_MAX_init

    def refresh_fitness_v2(self):  # With Checkpoint
        if self._on_road:
            self._fitness += max(self._speed, 0) * weight_on_road / FPS_MAX_init

            self._time_outside_road = max(0, self._time_outside_road - 0.1)

            if self._checkpoints:
                # Check if on checkpoint
                x, y = self.get_position_center()
                x_grid = x // self._track.case_size
                y_grid = y // self._track.case_size

                for checkpoint in self._checkpoints:
                    if not checkpoint[1]:
                        continue
                    if y_grid == checkpoint[0][0] and x_grid == checkpoint[0][1]:
                        self._fitness += boost_checkpoint
                        self._bonus_checkpoints += boost_checkpoint
                        checkpoint[1] = False
                        # print("ON CHECKPOINT")
                        break
                # Todo Ne pas reset directement les CP sinon ça fait doublon
                if not any([cp[1] for cp in self._checkpoints]):
                    self.reset_checkpoints()
                    # print("RESET CHECKPOINT")
        else:
            self._time_outside_road += 1
            self._fitness -= max(self._speed, 0) * self._time_outside_road * weight_on_road / FPS_MAX_init

    def set_checkpoints(self):
        my_list = []
        for checkpoint in self._track.checkpoints:
            x, y = self.get_position_center()
            x_grid = x // self._track.case_size
            y_grid = y // self._track.case_size
            if x_grid != checkpoint[1] or y_grid != checkpoint[0]:
                my_list.append([checkpoint, True])
            else:
                my_list.append([checkpoint, False])
        if not my_list:
            return None
        # set first at 0
        # my_list[0][1] = False
        return my_list

    def reset_checkpoints(self):
        for checkpoint in self._checkpoints:
            checkpoint[1] = True

    def _gen_car_img(self, path_img):
        img = pygame.image.load(path_img).convert_alpha()
        width = img.get_width()
        height = img.get_height()
        ratio = float(width / height)
        car_len = self._track.car_size
        if ratio < 1:
            width = car_len
            height = int(car_len * ratio)
        else:
            height = car_len
            width = int(car_len / ratio)

        img_resize = pygame.transform.scale(img, (height, width))
        return img_resize

    @property
    def last_dir_cmd(self):
        return self._last_dir_cmd

    @property
    def last_gas_cmd(self):
        return self._last_gas_cmd

    @property
    def fitness(self):
        return self._fitness

    @property
    def actual_img(self):
        return self._actual_img

    @property
    def lidar_grid_car_x(self):
        return self._lidar_grid_car_x

    @property
    def lidar_grid_car_y(self):
        return self._lidar_grid_car_y

    def lidar_is_practicable(self, i, j):
        return self._lidar.is_practicable(i, j)

    def lidar_get_true_pos(self, i, j):
        return self._lidar.get_true_pos(i, j)
