import math
import pygame
from math import cos, sin, radians, exp

from src.const import *
from src.objects.Track import Track


class CarHuman:
    def __init__(self, track: Track, lidar_w, lidar_h):
        # INIT VARIABLES
        self.theta = 0.0
        self.speed = 0.0
        self.speed_max = track.speed_max
        self.x_speed = 0.0
        self.y_speed = 0.0
        self.rest_pos_x = 0.0
        self.rest_pos_y = 0.0
        self.n_speed = 0.0
        self.fitness = 0
        self.bonus_checkpoints = 0

        # Set startPosition
        self.x_init = track.init_car_x
        self.y_init = track.init_car_y

        # Count time outside road to penalize
        self.time_outside_road = 0
        self.on_road = True

        self.last_dir_cmd = wheel_NONE
        self.last_gas_cmd = gas_OFF

        # GEN CAR IMAGE
        self.img = gen_car_img(track, path_audi)
        if track.start_direction == dir_RIGHT:
            self.img = pygame.transform.rotate(self.img, theta_0)

        self.actual_img = self.img

        # SET POSITION
        self.position_car = self.actual_img.get_rect()
        self.position_car = self.position_car.move(self.x_init, self.y_init)

        # self.actual_grid_x = None
        # self.actual_grid_y = None

        # GEN LIDAR
        self.track = track
        self.lidar_grid_size = track.grid_size // (1 + int(track.double_road))
        self.lidar_grid_car_x = width_LIDAR // 2
        self.lidar_grid_car_y = height_LIDAR - offset_y_LIDAR - 1

        self.lidar_w_img, self.lidar_h_img = lidar_w, lidar_h
        self.lidar_w_rect, self.lidar_h_rect = lidar_w // width_LIDAR, lidar_h // height_LIDAR

        self.lidar_mat = []
        self.lidar_filtered = []
        for _ in range(height_LIDAR):
            self.lidar_mat.append(width_LIDAR * [""])
            self.lidar_filtered.append(width_LIDAR * [False])

        self.refresh_LIDAR()

        # Checkpoints
        self.checkpoints = self.set_checkpoints(track)

    # Is aptly named
    def actualize_direction_and_gas(self, new_commands):
        for command in new_commands:
            self.actualize_direction_or_gas(command)

    def actualize_direction_or_gas(self, new_command):
        if new_command in [gas_OFF, gas_BRAKE, gas_ON]:
            self.calculate_new_speed(new_command)
            self.last_gas_cmd = new_command

        else:
            self.calculate_new_angle(new_command)

            self.actual_img = pygame.transform.rotate(self.img, self.theta)
            new_rect = self.actual_img.get_rect()
            self.position_car = new_rect.move(self.new_pos_after_turn(new_rect))
            self.last_dir_cmd = new_command

    def calculate_new_speed(self, command):
        if not self.on_road:
            if (1 - exp(-self.n_speed / n0_speed)) > 0.3:
                #  If speed at more than 30% of the maximum
                # self.n_speed = self.n_speed - 4
                self.speed = max(self.speed * 0.70, 0)
                self.recalculate_n_speed()

        if command == gas_OFF:
            self.speed = max(self.speed * 0.97, 0)
            self.recalculate_n_speed()

        elif command == gas_BRAKE and self.speed > 1:
            self.speed = max(self.speed * 0.90, 0)
            self.recalculate_n_speed()
        else:

            if command == gas_BRAKE:
                self.n_speed = max(self.n_speed - 2.0, -n0_speed / 2)

            else:  # if command == gas_ON
                if self.on_road:
                    self.n_speed = min(self.n_speed + 1.0, max_n_speed)
                else:
                    self.n_speed = min(self.n_speed + .3, max_n_speed)

            if self.n_speed > 0:
                self.speed = self.speed_max * (1 - exp(-self.n_speed / n0_speed))
            else:
                self.speed = - 0.5 * self.speed_max * (1 - exp(self.n_speed / n0_speed))

    def recalculate_n_speed(self):
        if self.speed > 0:
            self.n_speed = -n0_speed * math.log2(1 - (self.speed / self.speed_max))
        else:
            self.n_speed = n0_speed * math.log2(1 - (self.speed / self.speed_max))


    def reduce_all_speeds(self, fact):
        self.speed = max(self.speed - fact, 0)
        self.x_speed = max(self.x_speed - fact, 0)
        self.y_speed = max(self.y_speed - fact, 0)

    def calculate_new_angle(self, command):
        if command == wheel_LEFT:
            self.theta += car_step_angle
        elif command == wheel_RIGHT:
            self.theta -= car_step_angle

        drift_fact = min(drift_factor_cst * math.pow(self.speed / self.speed_max, 2), drift_factor_max)
        self.x_speed = drift_fact * self.x_speed + (1 - drift_fact) * round(self.speed * cos(radians(self.theta)), 6)
        self.y_speed = drift_fact * self.y_speed + (1 - drift_fact) * round(-self.speed * sin(radians(self.theta)), 6)

    def move_car(self):
        # The fact is that pygame delete post comma digits
        # We save them !
        # print(50 * "*")
        # print("Before : {} / {}".format(self.rest_pos_x, self.rest_pos_y))
        self.rest_pos_x, x_move_int = math.modf(self.x_speed + self.rest_pos_x)
        self.rest_pos_y, y_move_int = math.modf(self.y_speed + self.rest_pos_y)

        # print("After : {} / {}".format(self.rest_pos_x, self.rest_pos_y))
        self.position_car = self.position_car.move(x_move_int,
                                                   y_move_int)

    def move_car_and_refresh_LIDAR(self, window=None):
        # Car
        self.move_car()
        # Window
        self.refresh_LIDAR(window)
        self.on_road = self.lidar_filtered[self.lidar_grid_car_y][self.lidar_grid_car_x]

    def get_position_left_top(self):
        return tuple([self.position_car.x,
                      self.position_car.y])

    def get_position_center(self):
        return tuple([self.position_car.centerx,
                      self.position_car.centery])

    def new_pos_after_turn(self, new_rect):
        return tuple([self.position_car.centerx - new_rect.rect_w // 2,
                      self.position_car.centery - new_rect.h // 2])

    def reset_car(self):
        self.theta = 0.0
        self.speed = 0.0
        self.x_speed = 0.0
        self.y_speed = 0.0
        self.rest_pos_x = 0.0
        self.rest_pos_y = 0.0
        self.n_speed = 0.0
        self.fitness = 0
        self.bonus_checkpoints = 0
        self.time_outside_road = 0

        self.actual_img = pygame.transform.rotate(self.img, self.theta)
        new_rect = self.actual_img.get_rect()
        self.position_car = new_rect.move(self.x_init,
                                          self.y_init)

        self.refresh_LIDAR()

        self.reset_checkpoints()

    def refresh_LIDAR(self, window=None):
        car_x, car_y = self.get_position_center()

        for i in range(height_LIDAR):
            for j in range(width_LIDAR):
                dx_rel_grid = (j - self.lidar_grid_car_x) * self.lidar_grid_size
                dy_rel_grid = (i - self.lidar_grid_car_y) * self.lidar_grid_size

                # /!\ I took theta = 0° when pointing left but the lidar map is pointing top
                dx_rel = dx_rel_grid * cos(radians(self.theta - 90.0)) + dy_rel_grid * sin(radians(self.theta - 90.0))
                dy_rel = -dx_rel_grid * sin(radians(self.theta - 90.0)) + dy_rel_grid * cos(radians(self.theta - 90.0))

                true_dx = round(dx_rel + car_x)
                true_dy = round(dy_rel + car_y)

                true_x_grid = true_dx // self.track.grid_size
                true_y_grid = true_dy // self.track.grid_size

                if 0 < true_x_grid < self.track.grid_w and 0 < true_y_grid < self.track.grid_h:
                    corresponding_square = self.track.grid_raw[true_y_grid][true_x_grid]

                else:
                    corresponding_square = "xx"

                self.lidar_mat[i][j] = corresponding_square

                # is_practicable = track_part_1w_practicable[corresponding_square]
                is_practicable = "x" not in corresponding_square

                self.lidar_filtered[i][j] = is_practicable

                if window is not None:
                    # Print Points & Result
                    point_pos = tuple([true_dx, true_dy])
                    rect_pos = tuple([self.track.im_w + j * self.lidar_w_rect + erode_LIDAR_grid,
                                      offset_LIDAR_grid_y + i * self.lidar_h_rect + erode_LIDAR_grid,
                                      self.lidar_w_rect - 2 * erode_LIDAR_grid,
                                      self.lidar_h_rect - 2 * erode_LIDAR_grid])

                    if is_practicable:
                        color = COLOR_GREEN
                    else:
                        color = COLOR_RED

                    pygame.draw.circle(window, color, point_pos, circle_size)
                    pygame.draw.rect(window, color, rect_pos)

        if window is not None:
            point_pos = tuple([round(self.track.im_w + (self.lidar_grid_car_x + 0.5) * self.lidar_w_rect),
                               offset_LIDAR_grid_y + round((self.lidar_grid_car_y + 0.5) * self.lidar_h_rect)])

            pygame.draw.circle(window, COLOR_BLUE, point_pos, 4, 2)

    # ----Fitness & Checkpoints---#

    # Use some functions to calculate new fitness
    def refresh_fitness_v1(self):
        if self.on_road:
            self.fitness += max(self.speed, 0) * weight_on_road / FPS_MAX_init

            self.time_outside_road = max(0, self.time_outside_road - 0.1)
        else:
            self.time_outside_road += 1
            self.fitness -= 40 * (max(self.speed, 0) + weight_on_road + self.time_outside_road) / FPS_MAX_init

    def refresh_fitness_v2(self):  # With Checkpoint
        if self.on_road:
            self.fitness += max(self.speed, 0) * weight_on_road / FPS_MAX_init

            self.time_outside_road = max(0, self.time_outside_road - 0.1)

            if self.checkpoints:
                # Check if on checkpoint
                x, y = self.get_position_center()
                x_grid = x // self.track.grid_size
                y_grid = y // self.track.grid_size

                for checkpoint in self.checkpoints:
                    if not checkpoint[1]:
                        continue
                    if y_grid == checkpoint[0][0] and x_grid == checkpoint[0][1]:
                        self.fitness += boost_checkpoint
                        self.bonus_checkpoints += boost_checkpoint
                        checkpoint[1] = False
                        # print("ON CHECKPOINT")
                        break
                #  Todo Ne pas reset directement les CP sinon ça fait doublon
                if not any([cp[1] for cp in self.checkpoints]):
                    self.reset_checkpoints()
                    # print("RESET CHECKPOINT")
        else:
            self.time_outside_road += 1
            self.fitness -= max(self.speed, 0) * self.time_outside_road * weight_on_road / FPS_MAX_init

    def set_checkpoints(self, track):
        my_list = []
        for checkpoint in track.checkpoints:
            x, y = self.get_position_center()
            x_grid = x // self.track.grid_size
            y_grid = y // self.track.grid_size
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
        for checkpoint in self.checkpoints:
            checkpoint[1] = True


def gen_car_img(track, path_img):
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
    return img_resize
