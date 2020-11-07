import pygame

from src.const import *

from pygame_gui.elements import UIButton
from src.uix.widgets.ItemDropdown import ItemDropdown

from src.uix.screens.abstract.ScreenBase import ScreenBase

from src.uix.screens.ScreenPlayHuman import run_play_human
from src.uix.screens.ScreenPlayAI import run_play_ai
from src.uix.screens.ScreenTrainRandomEvolv import run_train
from src.uix.screens.ScreenDrawTrack import run_draw_map

FPS_MAX = 30

window_size = (big_window_haut, big_window_haut)

buttons_dict = {
    "Play !": run_play_human,
    "Play AI": run_play_ai,
    "Train": run_train,
    "Draw !": run_draw_map,
}

menu_button_w = round(big_window_haut / 3.7)
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
        self._button_save_train = self._gen_save_button()
        self._button_use_trained_model = self._gen_use_trained_model_button()

        # Add selection Pane
        self._dropdown_tracks = self._gen_dropdown_tracks()

        self._dropdown_trained_models = self._gen_dropdown_model_trained()
        self._dropdown_trained_models.hide()

        self._dropdown_raw_models = self._gen_dropdown_model_design()

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

    def _gen_save_button(self):
        button_layout_rect = pygame.Rect(int(0.05 * self._window_w), int(8 * self._window_h / 10),
                                         menu_button_w // 2, menu_button_h // 2)
        button = UIButton(relative_rect=button_layout_rect,
                          text="Save",
                          manager=self._ui_manager)
        button.select()
        return button

    def _gen_use_trained_model_button(self):
        x_center, y_center, w, h = int(0.8 * self._window_w), int(
            8 * self._window_h / 10), menu_button_w, menu_button_h // 2
        centered_rect = (x_center - w // 2, y_center - h // 2, w, h)

        button_layout_rect = pygame.Rect(*centered_rect)
        button = UIButton(relative_rect=button_layout_rect,
                          text="Use Trained Model ?",
                          manager=self._ui_manager)
        return button

    def _gen_dropdown_tracks(self):
        x = big_window_haut // 5
        y = big_window_haut // 2
        title = "Choose Track"

        return ItemDropdown(rect=(x, y, menu_button_w, menu_button_h // 2), manager=self._ui_manager,
                            folder=track_files_path, extension=".tra", text=title)

    def _gen_dropdown_model_trained(self):
        x = 8 * big_window_haut // 10
        y = int(0.4 * big_window_haut)
        title = "Trained Model"

        return ItemDropdown(rect=(x, y, menu_button_w, menu_button_h // 2), manager=self._ui_manager,
                            folder=trained_model_path, extension=".h5", text=title)

    def _gen_dropdown_model_design(self):
        x = 8 * big_window_haut // 10
        y = int(0.6 * big_window_haut)
        title = "Model Design"

        return ItemDropdown(rect=(x, y, menu_button_w, menu_button_h // 2), manager=self._ui_manager,
                            folder=raw_models_path, extension=".net", text=title)

    def _gen_background(self):
        background = super(ScreenHome, self)._gen_background()
        img_logo = gen_logo_img(title_path)
        # Draw logo
        logo_x = (self._window_w - img_logo.get_width()) // 2
        background.blit(img_logo, (logo_x, offset_h))
        return background

    def _button_pressed_handle(self, button):
        if button in self._buttons_action:
            self._buttons_action[button](**self.dropdown_kwargs)
            self.reset_n_reload()
        elif button == self._button_save_train:
            if self._button_save_train.is_selected:
                self._button_save_train.unselect()
            else:
                self._button_save_train.select()
        elif button == self._button_use_trained_model:
            if self._button_use_trained_model.is_selected:
                self._button_use_trained_model.unselect()

                self._dropdown_raw_models.show()
                self._dropdown_trained_models.hide()

            else:
                self._button_use_trained_model.select()

                self._dropdown_raw_models.hide()
                self._dropdown_trained_models.show()

    @property
    def dropdown_kwargs(self):
        if self._button_use_trained_model.is_selected:
            nn_file_path = self._dropdown_trained_models.get_item()
        else:
            nn_file_path = self._dropdown_raw_models.get_item()
        dict_parameters = {
            "track_path": self._dropdown_tracks.get_item(),
            "nn_file_path": nn_file_path,
            "save_train": self._button_save_train.is_selected,
        }
        return dict_parameters

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
