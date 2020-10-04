from uix.my_gui.screens.abstract import ScreenBase
from uix.my_gui.screens import run_draw_map
from uix.my_gui.screens import run_play_ai
from uix.my_gui.screens import run_play_human
from uix.my_gui.screens import run_train

# List functions which should be linked to buttons
actions = [run_play_human, run_play_ai, run_train, run_draw_map]

FPS_MAX = 30

button_list_name = [
    "human",
    "ai",
    "train",
    "draw",
]

buttons_off_path = [buttons_img_path + name + "_off.png" for name in button_list_name]
buttons_on_path = [buttons_img_path + name + "_on.png" for name in button_list_name]
buttons_push_path = [buttons_img_path + name + "_push.png" for name in button_list_name]

button_save_on = buttons_img_path + "save_on.png"
button_save_off = buttons_img_path + "save_off.png"


class ScreenHome(ScreenBase):
    def __init__(self):
        super(ScreenHome, self).__init__(window_size=(big_window_haut, big_window_haut),
                                         fps_max=FPS_MAX)

        # Add buttons
        self._buttons_action = [ButtonPress(self._window_w // 2, buttons_y[i],
                                            path_img_on=buttons_on_path[i], path_img_off=buttons_off_path[i],
                                            path_img_push=buttons_push_path[i],
                                            on_press=actions[i])
                                for i in range(4)]

        self._button_save_train = ButtonOnOff(int(0.2 * self._window_w), int(8 * self._window_h / 10),
                                              img_on=button_save_on,
                                              img_off=button_save_off,
                                              size=(0.7 * menu_button_w, 0.7 * menu_button_h))

        self._buttons = self._buttons_action + [self._button_save_train]

        self._button_overlap = None

        # Add selection Pane
        self._select_pane_track = SelectionPaneTrack()

        self._select_pane_model_train = SelectionPaneModelTrain()

        self._select_pane_model_raw = SelectionPaneModelRaw()

        # Generate Background which contains everything that do not move
        self._background = pygame.image.load(background_path).convert()
        self._img_logo = gen_logo_img(title_path)

        self._gen_menu_background()

        # Mouse infos
        self._is_ready_select = False  # Mouse's button has been pushed on menu's button, waiting for release

        self.actualize()

    def gen_background(self):
        pass

    def actualize(self, pos=None):
        self._clock.tick(self._fps_max)

        # Start by drawing background
        self._window.blit(self._background, (0, 0))

        # Watch if cursor is/is clicking on one button
        self._button_overlap = self.mouse_on_buttons(pos)

        # Change color of save_train button if selected
        if self._button_save_train.is_selected:
            self._button_save_train.draw_button_image(self._window)

        # Watch for SelectionPanes
        self._select_pane_track.actualize(self._window, pos, self._mouse_is_holding_left)
        self._select_pane_model_train.actualize(self._window, pos, self._mouse_is_holding_left)
        self._select_pane_model_raw.actualize(self._window, pos, self._mouse_is_holding_left)

        # Display
        pygame.display.flip()

    def _gen_menu_background(self):
        # Draw logo
        logo_x = (self._window_w - self._img_logo.get_width()) // 2
        self._background.blit(self._img_logo, (logo_x, offset_h))
        # Draw buttons
        for button in self._buttons:
            button.draw_button_image(self._background)

    # Check if mouse is on one button and if the case, return the button object
    def mouse_on_buttons(self, pos):
        if pos is None:
            return None
        mouse_x = pos[0]
        mouse_y = pos[1]
        for i, button in enumerate(self._buttons):
            ret = button.mouse_on_button(mouse_x, mouse_y)
            if not ret:
                continue
            button.draw_button_image(self._window, self._mouse_is_holding_left)
            return button
        return None

    def on_mouse_release(self, **kwargs):
        super(ScreenHome, self).on_mouse_release(**kwargs)
        self.run_action_selected()

    # Run action corresponding to its button
    def run_action_selected(self):
        if self._button_overlap is None:
            return
        # Check if the button is among those who run another window of the game
        if self._button_overlap in self._buttons_action:
            # Check if a trained model has been selected, else, use untrained model
            model_train_path = self._select_pane_model_train.get_chosen_item_path()
            if model_train_path is not None:
                model_path = model_train_path
            else:
                model_path = self._select_pane_model_raw.get_chosen_item_path()

            # generate **kwargs parameters to give config to others windows
            dict_parameters = {
                "track_path": self._select_pane_track.get_chosen_item_path(),
                "model_path": model_path,
                "save_train": self._button_save_train.is_selected
            }

            # Executing action
            self._button_overlap.on_press(**dict_parameters)

            # Resetting window
            self.reset_n_reload()

        else:  # Action do not need parameters (basically, On/Off Button)
            self._button_overlap.on_press()

    def reset_window_size(self):
        self._window = pygame.display.set_mode((self._window_w, self._window_h))

    def reset_n_reload(self):
        self.reset_window_size()
        # Regenerate Track List
        self._select_pane_track = SelectionPaneTrack()


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
