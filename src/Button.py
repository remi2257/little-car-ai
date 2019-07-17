from src.const import *
import pygame
import numpy as np


class Button:
    def __init__(self, ind, actions, windows_w):

        self.img_on = gen_button_img(buttons_on_path[ind])
        self.img_off = gen_button_img(buttons_off_path[ind])
        self.img_push = gen_button_img(buttons_push_path[ind])

        self.rect_x = windows_w // 2 - self.img_on.get_width() // 2
        self.rect = self.get_rect_menu_pos(ind)
        self.rect_y = self.rect[1]

        self.action = actions[ind]
        self.mouse_on = False

    def get_rect_menu_pos(self, rect_id):
        return tuple([self.rect_x, buttons_y[rect_id],
                      menu_button_w, menu_button_h])

    def mouse_on_button(self, mouse_x, mouse_y):
        x, y, w, h = self.rect
        if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
            self.mouse_on = True
        else:
            self.mouse_on = False

        return self.mouse_on

    def draw_button_image(self, window, mouse_pressed=False):
        if self.mouse_on:
            if mouse_pressed:
                window.blit(self.img_push, (self.rect_x, self.rect_y))

            else:
                window.blit(self.img_on, (self.rect_x, self.rect_y))
        else:
            window.blit(self.img_off, (self.rect_x, self.rect_y))

    def run_action(self):
        self.action()


def gen_button_img(path_img):
    img = pygame.image.load(path_img).convert_alpha()
    width = img.get_width()
    height = img.get_height()

    ratio = float(width / height)

    new_height = menu_button_h
    new_width = int(new_height * ratio)

    img_resize = pygame.transform.scale(img, (new_width, new_height))
    return img_resize
