import pygame

from .Widget import Widget


class Button(Widget):
    def __init__(self, rect, **kwargs):
        super(Button, self).__init__(**kwargs)

        self._rect = rect  # Rect corresponding to (x,y,w,h)
        self._mouse_on = False  # True if mouse is on the button

    def get_rect_menu_pos(self):
        return self._rect

    def mouse_on_button(self, mouse_x, mouse_y):
        x, y, w, h = self._rect
        if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
            self._mouse_on = True
        else:
            self._mouse_on = False

        return self._mouse_on

    def draw_button_image(self, window, mouse_pressed=False):
        raise NotImplementedError

    def gen_button_img(self, path_img):
        if path_img is None:
            return None, None
        img = pygame.image.load(path_img).convert_alpha()

        img_resize = pygame.transform.scale(img, (self.w, self.h))
        return img_resize

    @property
    def x(self):
        return self._rect[0]

    @property
    def y(self):
        return self._rect[1]

    @property
    def w(self):
        return self._rect[2]

    @property
    def h(self):
        return self._rect[3]
