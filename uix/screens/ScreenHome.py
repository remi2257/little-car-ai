from uix.screens.ScreenDrawTrack import run_draw_map
from uix.screens.ScreenSolo  import run_play_ai
from uix.screens.ScreenSolo import run_play_human
from uix.screens.ScreenTrainEvolv import run_train

from uix.widgets.ButtonOnOff import *
from uix.widgets.ButtonPress import *
from uix.widgets.SelectionPaneModelRaw import *
from uix.widgets.SelectionPaneModelTrain import *
from uix.widgets.SelectionPaneTrack import *

# List functions which should be linked to buttons
actions = [run_play_human, run_play_ai, run_train, run_draw_map]


class ScreenHome:
    def __init__(self):
        pygame.init()

        # Set clock to limit FPS
        self.FPS_MAX = 30
        pygame.time.Clock().tick(self.FPS_MAX)  # Set max FPS
        self.clock = pygame.time.Clock()

        # Generate Main Window
        pygame.display.set_caption(game_name)
        self.window_w = big_window_haut
        self.window_h = big_window_haut
        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        # Add buttons
        self.buttons_mode = [ButtonPress(self.window_w // 2, buttons_y[i], actions[i],
                                         path_img_on=buttons_on_path[i], path_img_off=buttons_off_path[i],
                                         path_img_push=buttons_push_path[i])
                             for i in range(4)]

        self.button_save_train = ButtonOnOff(x=int(8 * self.window_w / 10), y=int(8 * self.window_h / 10),
                                             img_on=button_save_on,
                                             img_off=button_save_off)

        self.buttons = self.buttons_mode + [self.button_save_train]

        self.button_overlap = None

        # Add selection Pane
        self.select_pane_track = SelectionPaneTrack()

        self.select_pane_model_train = SelectionPaneModelTrain()

        self.select_pane_model_raw = SelectionPaneModelRaw()

        # Generate Background which contains everything that do not move
        self.background = pygame.image.load(background_path).convert()
        self.img_logo = gen_logo_img(title_path)

        self.gen_menu_background()

        # Mouse infos
        self.is_holding = False  # One mouse's button is pushed
        self.is_ready_select = False  # Mouse's button has been pushed on menu's button, waiting for release

        self.actualize()

    def actualize(self, pos=None):
        self.clock.tick(self.FPS_MAX)

        # Start by drawing background
        self.window.blit(self.background, (0, 0))

        # Watch if cursor is/is clicking on one button
        self.button_overlap = self.mouse_on_buttons(pos)
        # Highlight Menu buttons if mouse is on
        for button in self.buttons_mode:
            if button.mouse_on:
                button.draw_button_image(self.window, self.is_holding)
        # Change color of save_train button if selected
        if self.button_save_train.is_selected:
            self.button_save_train.draw_button_image(self.window, self.is_holding)

        # Watch for SelectionPanes
        self.select_pane_track.actualize(self.window, pos, self.is_holding)
        self.select_pane_model_train.actualize(self.window, pos, self.is_holding)
        self.select_pane_model_raw.actualize(self.window, pos, self.is_holding)

        # Display
        pygame.display.flip()

    def gen_menu_background(self):
        # Draw logo
        logo_x = (self.window_w - self.img_logo.get_width()) // 2
        self.background.blit(self.img_logo, (logo_x, offset_h))
        # Draw buttons
        for button in self.buttons:
            button.draw_button_image(self.background)

    # Check if mouse is on one button and if the case, return the button object
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

    # Run action corresponding to its button
    def run_action_selected(self):
        if self.button_overlap is not None:
            # Check if the button is among those who run another window of the game
            if self.button_overlap.__class__.__name__ == "ButtonPress":
                # Check if a trained model has been selected, else, use untrained model
                model_train_path = self.select_pane_model_train.get_item_path()
                if model_train_path is not None:
                    model_path = model_train_path
                else:
                    model_path = self.select_pane_model_raw.get_item_path()

                # generate **kwargs parameters to give config to others windows
                dict_parameters = {
                    "track_path": self.select_pane_track.get_item_path(),
                    "model_path": model_path,
                    "save_train": self.button_save_train.is_selected
                }

                # Executing action
                self.button_overlap.run_action(**dict_parameters)

                # Resetting window
                self.reset_window_size()
                # Regenerate Track List if GameDraw was the mode launched
                if self.button_overlap.action == run_draw_map:
                    self.select_pane_track = SelectionPaneTrack()

            else:  # Action do not need parameters (basically, On/Off Button)
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


def run_home_screen():
    # --- INIT Variable--- #

    should_stop = None

    # --- INIT Menu Window --- #

    game = ScreenHome()

    # Boucle infinie
    while not should_stop:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                should_stop = True  # On arrête la boucle
            if event.type == pygame_const.MOUSEBUTTONDOWN:  # If Push Mouse's button
                game.is_holding = True
            if event.type == pygame_const.MOUSEBUTTONUP:  # If release Mouse's button
                game.is_holding = False
                game.run_action_selected()  # This release mean a click, so we execute linked action
        pos = pygame.mouse.get_pos()

        game.actualize(pos)  # Actualize window

    # return stop


if __name__ == '__main__':
    run_home_screen()
