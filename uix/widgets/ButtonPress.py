from uix.widgets.Button import Button

from src.const import menu_button_w, menu_button_h

'''
You can press this button to launch an action
'''


class ButtonPress(Button):
    def __init__(self, x_center, y, path_img_off, path_img_on, path_img_push, **kwargs):
        x = x_center - menu_button_w // 2
        Button.__init__(self, (x, y, menu_button_w, menu_button_h), **kwargs)

        self._img_off = self.gen_button_img(path_img_off)
        self._img_on = self.gen_button_img(path_img_on)
        self._img_push = self.gen_button_img(path_img_push)

    def draw_button_image(self, window, mouse_pressed=False):
        if self._mouse_on:
            if self._img_push is None:
                window.blit(self._img_on, (self.x, self.y))
            elif self._img_on is None:
                window.blit(self._img_push, (self.x, self.y))

            elif mouse_pressed:
                window.blit(self._img_push, (self.x, self.y))

            else:
                window.blit(self._img_on, (self.x, self.y))
        else:
            window.blit(self._img_off, (self.x, self.y))
