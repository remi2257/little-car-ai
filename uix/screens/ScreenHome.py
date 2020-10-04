import pygame
from pygame_gui.elements import UIButton

from uix.screens.abstract import ScreenBase
# from uix.my_gui.screens import run_draw_map
# from uix.my_gui.screens import run_play_ai
# from uix.my_gui.screens import run_play_human
# from uix.my_gui.screens import run_train
from src.const import *

FPS_MAX = 30

window_size = (big_window_haut, big_window_haut)

buttons_dict = {
    "Play !": "run_play_human",
    "Play AI": "run_play_ai",
    "Train": "run_train",
    "Draw !": "run_draw_map",
}

menu_button_w = round(big_window_haut / 3.5)
menu_button_h = round(menu_button_w / 2.13)

offset_h = round(20 * big_window_haut / 700)

nbr_buttons = 4

first_button_y = round(200 * big_window_haut / 800)

buttons_y = [first_button_y + i * (offset_h + menu_button_h) for i in range(nbr_buttons)]


class ScreenHome(ScreenBase):
    def __init__(self):
        super(ScreenHome, self).__init__(window_size=window_size,
                                         fps_max=FPS_MAX)

        self._buttons_action = self.gen_buttons()

        # Add buttons
        # self._buttons_action = [ButtonPress(self._window_w // 2, buttons_y[i],
        #                                     path_img_on=buttons_on_path[i], path_img_off=buttons_off_path[i],
        #                                     path_img_push=buttons_push_path[i],
        #                                     on_press=actions[i])
        #                         for i in range(4)]
        #
        # self._button_save_train = ButtonOnOff(int(0.2 * self._window_w), int(8 * self._window_h / 10),
        #                                       img_on=button_save_on,
        #                                       img_off=button_save_off,
        #                                       size=(0.7 * menu_button_w, 0.7 * menu_button_h))

        # self._buttons = self._buttons_action + [self._button_save_train]

        # self._button_overlap = None

        # Add selection Pane
        # self._select_pane_track = SelectionPaneTrack()
        #
        # self._select_pane_model_train = SelectionPaneModelTrain()
        #
        # self._select_pane_model_raw = SelectionPaneModelRaw()

        # Generate Background which contains everything that do not move
        self._background = pygame.image.load(background_path).convert()
        self._img_logo = gen_logo_img(title_path)

        self._gen_menu_background()

        self.actualize()

    def gen_buttons(self):
        buttons = {}
        for i, (label, callback) in enumerate(buttons_dict.items()):
            button_layout_rect = pygame.Rect(self._window_w // 2 - menu_button_w // 2, buttons_y[i],
                                             menu_button_w, menu_button_h)
            button = UIButton(relative_rect=button_layout_rect,
                              text=label,
                              manager=self._ui_manager)
            buttons[button] = callback
        return buttons

    def gen_background(self):
        pass

    def actualize(self, pos=None):
        pass

    def _gen_menu_background(self):
        # Draw logo
        logo_x = (self._window_w - self._img_logo.get_width()) // 2
        self._background.blit(self._img_logo, (logo_x, offset_h))

    def reset_window_size(self):
        self._window = pygame.display.set_mode((self._window_w, self._window_h))

    def reset_n_reload(self):
        self.reset_window_size()


def gen_logo_img(path_img):
    img = pygame.image.load(path_img).convert_alpha()
    width = img.get_width()
    height = img.get_height()

    ratio = float(width / height)

    new_height = int(menu_button_h * 1.0)
    new_width = int(new_height * ratio)

    img_resize = pygame.transform.scale(img, (new_width, new_height))
    return img_resize


def run_home_screen():
    ScreenHome().run()


if __name__ == '__main__':
    run_home_screen()
