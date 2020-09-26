from uix.widgets.Button import Button
from src.const import menu_button_w, menu_button_h

'''
You can either select it or not
'''


class ButtonOnOff(Button):
    def __init__(self, x_center, y, img_on, img_off):
        x = x_center - menu_button_w // 2

        Button.__init__(self, (x, y, menu_button_w, menu_button_h))

        self.img_on = self.gen_button_img(img_on)
        self.img_off = self.gen_button_img(img_off)

        self.imgs = {False: self.img_off,
                     True: self.img_on}

        self.is_selected = False

    def draw_button_image(self, window, mouse_pressed=False):
        window.blit(self.actual_button_image, (self.x, self.y))

    def on_press(self, *args, **kwargs):
        self.is_selected = not self.is_selected

    @property
    def actual_button_image(self):
        return self.imgs[self.is_selected]
