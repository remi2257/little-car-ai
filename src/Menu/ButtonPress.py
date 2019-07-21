import pygame

from src.const import *
from src.Menu.Button import *


class ButtonPress(Button):
    def __init__(self, x, y, action, path_img_off, path_img_on=None, path_img_push=None, button_w=menu_button_w):

        self.img_off, self.w = self.gen_button_img(path_img_off, new_width=button_w)
        self.img_on, _ = self.gen_button_img(path_img_on, new_width=button_w)
        self.img_push, _ = self.gen_button_img(path_img_push, new_width=button_w)

        self.rect_x = x - self.img_off.get_width() // 2
        self.rect_y = y

        self.rect = self.get_rect_menu_pos()

        Button.__init__(self, self.rect)

        self.action = action
        self.mouse_on = False

    def get_rect_menu_pos(self):
        return tuple([self.rect_x, self.rect_y,
                      self.w, menu_button_h])

    def mouse_on_button(self, mouse_x, mouse_y):
        x, y, w, h = self.rect
        if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
            self.mouse_on = True
        else:
            self.mouse_on = False

        return self.mouse_on

    def draw_button_image(self, window, mouse_pressed=False):
        if self.mouse_on:
            if self.img_push is None:
                window.blit(self.img_on, (self.rect_x, self.rect_y))
            elif self.img_on is None:
                window.blit(self.img_push, (self.rect_x, self.rect_y))

            elif mouse_pressed:
                window.blit(self.img_push, (self.rect_x, self.rect_y))

            else:
                window.blit(self.img_on, (self.rect_x, self.rect_y))
        else:
            window.blit(self.img_off, (self.rect_x, self.rect_y))

    def run_action(self, **dict_parameters):

        self.action(**dict_parameters)
