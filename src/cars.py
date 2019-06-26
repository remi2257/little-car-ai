import random
from src.const import *
import pygame
from math import cos, sin, radians, exp


class Car:
    def __init__(self, car_len=car_max_len, path_img="images/vehicles/Audi.png"):
        self.theta = 0.0
        self.speed = 0.0
        self.n_speed = 0.0

        img = pygame.image.load(path_img).convert_alpha()
        width = img.get_width()
        height = img.get_height()
        ratio = float(width / height)
        if ratio < 1:
            self.width = car_len
            self.height = int(car_len * ratio)
        else:
            self.height = car_len
            self.width = int(car_len / ratio)

        img_resize = pygame.transform.scale(img, (self.height, self.width))

        self.img = pygame.transform.rotate(img_resize, 270.0)

        self.actual_img = self.img

        self.position_car = self.actual_img.get_rect()

        self.position_car = self.position_car.move(200.0, 200.0)

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

    def move_car(self):
        self.position_car = self.position_car.move(self.speed * cos(radians(self.theta)),
                                                   - self.speed * sin(radians(self.theta)))

    def get_position_left_top(self):
        return tuple([self.position_car.x,
                      self.position_car.y])

    def get_position_center(self):
        return tuple([self.position_car.centerx,
                      self.position_car.centery])

    def new_pos(self, new_rect):
        return tuple([self.position_car.centerx - new_rect.w // 2,
                      self.position_car.centery - new_rect.h // 2])


class CarBot:
    def __init__(self, track, path_img="images/vehicles/car_bot.png"):
        # -- INIT IMAGES ---- #

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

        # -- INIT Rest ---- #
        self.y_grid, self.x_grid = track.start_spots.pop(0)

        self.direction = -1

        self.get_first_dir(track.track_grid)

        self.actual_img = self.imgs[self.direction]

        self.position_car = self.actual_img.get_rect()

        yc = self.y_grid * track.grid_size + track.grid_size // 2
        xc = self.x_grid * track.grid_size + track.grid_size // 2
        # y_init = yc - self.position_car.height // 2
        # x_init = xc - self.position_car.width // 2
        self.position_car = self.position_car.move(xc - self.position_car.centerx, yc - self.position_car.centery)

        self.can_change_dir = False

    def get_first_dir(self, track_grid):
        possible_moves = bot_possible_moves[track_grid[self.y_grid][self.x_grid]]
        self.direction = possible_moves[random.randrange(len(possible_moves))]

    def actualize_direction_bot(self, track_grid):
        change = self.get_next_dir(track_grid)

        if change:
            # ex_rect = self.actual_img.get_rect()
            self.actual_img = self.imgs[self.direction]
            # self.position_car = self.actual_img.get_rect().move(self.get_position_left_top())
            new_rect = self.actual_img.get_rect()
            self.position_car = new_rect.move(self.new_pos(new_rect))
            self.can_change_dir = False

    def get_next_dir(self, track_grid):
        if not self.can_change_dir:
            return False

        possible_moves = bot_possible_moves[track_grid[self.y_grid][self.x_grid]].copy()

        opposite_dir = give_opposite_direction(self.direction)
        possible_moves.remove(opposite_dir)
        # if possible_moves == [self.direction]:
        #     return False
        ex_move = self.direction
        self.direction = possible_moves[random.randrange(len(possible_moves))]
        if ex_move == self.direction:
            return False
        return True

    def move_car_bot(self, track):
        self.actualize_direction_bot(track.track_grid)

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
            dist_from_center = abs(track.grid_size // 2 - self.position_car.centerx % track.grid_size)
            if dist_from_center < step_dir:
                self.x_grid = new_case_x
                self.can_change_dir = True
        elif new_case_y != self.y_grid:
            dist_from_center = abs(track.grid_size // 2 - self.position_car.centery % track.grid_size)
            if dist_from_center < step_dir:
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
