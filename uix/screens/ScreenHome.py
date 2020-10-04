import pygame
from pygame_gui.elements import UIButton

from uix.screens.abstract.ScreenBase import ScreenBase
from src.const import *

from uix.screens.ScreenDrawTrack import run_draw_map
# from uix.my_gui.screens.ScreenPlayAI import run_play_ai
# from uix.my_gui.screens.ScreenPlayHuman import run_play_human
# from uix.my_gui.screens.ScreenTrainRandomEvolv import run_train


FPS_MAX = 30

window_size = (big_window_haut, big_window_haut)

buttons_dict = {
    "Play !": "run_play_human",
    "Play AI": "run_play_ai",
    "Train": "run_train",
    "Draw !": run_draw_map,
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

        # Add buttons
        self._buttons_action = self._gen_buttons_action()

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
        self._background = self._gen_background()

        # self.actualize_screen()

    def _gen_buttons_action(self):
        buttons = {}
        for i, (label, callback) in enumerate(buttons_dict.items()):
            button_layout_rect = pygame.Rect(self._window_w // 2 - menu_button_w // 2, buttons_y[i],
                                             menu_button_w, menu_button_h)
            button = UIButton(relative_rect=button_layout_rect,
                              text=label,
                              manager=self._ui_manager)
            buttons[button] = callback
        return buttons

    def _gen_background(self):
        background = super(ScreenHome, self)._gen_background()
        img_logo = gen_logo_img(title_path)
        # Draw logo
        logo_x = (self._window_w - img_logo.get_width()) // 2
        background.blit(img_logo, (logo_x, offset_h))
        return background

    def _button_pressed_handle(self, button):
        if button not in self._buttons_action:
            return
        self._buttons_action[button]()
        self.reset_n_reload()

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
