import pygame

from src.const import *


class Button:
    def __init__(self, rect):

        self.rect = rect # Rect corresponding to (x,y,w,h)
        self.mouse_on = False # True if mouse is on the button

    def get_rect_menu_pos(self):
        raise NotImplementedError

    def mouse_on_button(self, mouse_x, mouse_y):
        x, y, w, h = self.rect
        if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
            self.mouse_on = True
        else:
            self.mouse_on = False

        return self.mouse_on

    def draw_button_image(self, window, mouse_pressed=False):
        raise NotImplementedError

    def gen_button_img(self, path_img, new_width=menu_button_w):
        if path_img is None:
            return None, None
        img = pygame.image.load(path_img).convert_alpha()
        width = img.get_width()
        height = img.get_height()

        ratio = float(width / height)

        new_height = int(new_width / ratio)

        img_resize = pygame.transform.scale(img, (new_width, new_height))
        return img_resize, new_width

    def run_action(self, **dict_parameters):
        raise NotImplementedError
