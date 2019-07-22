import pygame

from src.const import *
from src.Menu.Button import *

'''
You can either select it or not
'''

class ButtonOnOff(Button):
    def __init__(self, x, y, img_on, img_off):

        self.img_on, self.w = self.gen_button_img(img_on, new_width=menu_button_w // 2)
        self.img_off, _ = self.gen_button_img(img_off, new_width=menu_button_w // 2)

        self.imgs = [self.img_off, self.img_on]

        self.rect_x = x
        self.rect_y = y

        self.rect = self.get_rect_menu_pos()

        Button.__init__(self, self.rect)

        self.mouse_on = False
        self.is_selected = False

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
        # if self.mouse_on:
        #     window.blit(self.imgs[int(not self.is_selected)], (self.rect_x, self.rect_y))
        # else:
        window.blit(self.imgs[int(self.is_selected)], (self.rect_x, self.rect_y))

    def run_action(self, **dict_parameters):
        self.is_selected = not self.is_selected
