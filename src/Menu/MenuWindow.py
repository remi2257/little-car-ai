from game_draw_map import run_draw_map
from game_play_ai import run_play_ai
from game_play_human import run_play_human
from game_train import run_train
from src.Menu.ButtonOnOff import *
from src.Menu.ButtonPress import *
from src.Menu.SelectionPaneModelRaw import *
from src.Menu.SelectionPaneModelTrain import *
from src.Menu.SelectionPaneTrack import *

actions = [run_play_human, run_play_ai, run_train, run_draw_map]


class MenuWindow:
    def __init__(self):
        pygame.init()

        self.FPS_MAX = 30
        pygame.time.Clock().tick(self.FPS_MAX)  # Fixe le nbr max de FPS

        pygame.display.set_caption(game_name)

        # Generate Window
        self.window_w = big_window_haut
        self.window_h = big_window_haut

        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        self.buttons_mode = [ButtonPress(self.window_w // 2, buttons_y[i], actions[i],
                                         path_img_on=buttons_on_path[i], path_img_off=buttons_off_path[i],
                                         path_img_push=buttons_push_path[i])
                             for i in range(4)]

        self.button_save = ButtonOnOff(x=int(8 * self.window_w / 10), y=int(8 * self.window_h / 10),
                                       img_on=button_save_on,
                                       img_off=button_save_off)

        self.buttons = self.buttons_mode + [self.button_save]

        self.button_overlap = None

        self.select_pane_track = SelectionPaneTrack()

        self.select_pane_model_train = SelectionPaneModelTrain()

        self.select_pane_model_raw = SelectionPaneModelRaw()

        # Generate Background
        self.background = pygame.image.load(background_path).convert()
        self.img_logo = gen_logo_img(title_path)

        self.gen_menu_background()

        # Mouse infos
        self.is_holding = False
        self.is_ready_select = False

        self.clock = pygame.time.Clock()

        self.actualize()

    def actualize(self, pos=None):
        self.clock.tick(self.FPS_MAX)

        self.window.blit(self.background, (0, 0))

        # Watch for Buttons
        self.button_overlap = self.mouse_on_buttons(pos)
        for button in self.buttons_mode:
            if button.mouse_on:
                button.draw_button_image(self.window, self.is_holding)
        if self.button_save.is_selected:
            self.button_save.draw_button_image(self.window, self.is_holding)

        # Watch for TrackBard*s
        self.select_pane_track.actualize(self.window, pos, self.is_holding)
        self.select_pane_model_train.actualize(self.window, pos, self.is_holding)
        self.select_pane_model_raw.actualize(self.window, pos, self.is_holding)

        pygame.display.flip()

    def gen_menu_background(self):
        logo_x = (self.window_w - self.img_logo.get_width()) // 2

        self.background.blit(self.img_logo, (logo_x, offset_h))
        for button in self.buttons:
            button.draw_button_image(self.background)

    def mouse_on_buttons(self, pos):
        if pos is None:
            return None
        mouse_x = pos[0]
        mouse_y = pos[1]
        for i, button in enumerate(self.buttons):
            ret = button.mouse_on_button(mouse_x, mouse_y)
            if ret:
                return button
        return None

    def run_action_selected(self):
        if self.button_overlap is not None:
            if self.button_overlap.__class__.__name__ == "ButtonPress":
                model_train_path = self.select_pane_model_train.get_item_path()
                if model_train_path is not None:
                    model_path = model_train_path
                else:
                    model_path = self.select_pane_model_raw.get_item_path()

                dict_parameters = {
                    "track_path": self.select_pane_track.get_item_path(),
                    "model_path": model_path,
                    "save": self.button_save.is_selected
                }

                # Executing
                self.button_overlap.run_action(**dict_parameters)

                # Reset
                self.reset_window_size()
                if self.button_overlap.action == run_draw_map:
                    self.select_pane_track = SelectionPaneTrack()

            else:
                self.button_overlap.run_action()

    def reset_window_size(self):
        self.window = pygame.display.set_mode((self.window_w, self.window_h))


def gen_logo_img(path_img):
    img = pygame.image.load(path_img).convert_alpha()
    width = img.get_width()
    height = img.get_height()

    ratio = float(width / height)

    new_height = int(menu_button_h * 1.0)
    new_width = int(new_height * ratio)

    img_resize = pygame.transform.scale(img, (new_width, new_height))
    return img_resize
