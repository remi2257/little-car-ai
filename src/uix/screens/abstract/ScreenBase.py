import pygame
import pygame.locals as pygame_const
import pygame_gui

from src.const import font_size_global, background_path
from src.usesful_func import start_pygame, should_stop_pygame


class ScreenBase:
    def __init__(self, window_size, fps_max=30, **kwargs):
        start_pygame()

        # Generate Main Window
        self._window_size = window_size
        self._window_w, self._window_h = self._window_size
        self._window = pygame.display.set_mode((self._window_w, self._window_h))
        self._ui_manager = pygame_gui.UIManager(self._window_size)

        # Background
        self._background = None

        # Frame Rate
        self._fps_max = fps_max
        self._clock = pygame.time.Clock()
        self._time_delta = 0

        self._mouse_is_holding_left = False

        # Font
        self._font = pygame.font.Font('freesansbold.ttf', int(font_size_global / 1.2))
        self._font_h = self._font.get_height()

    def _key_press_handle(self, key):
        pass

    def _keys_pressed_handle(self, keys):
        pass

    def _button_pressed_handle(self, button):
        pass

    def actualize_screen(self, pos=None):
        # Start by drawing background
        self._draw_background()

        self._ui_manager.update(self._time_delta)
        self._ui_manager.draw_ui(self._window)

    def _gen_background(self):
        return pygame.image.load(background_path).convert()

    def _draw_background(self):
        self._window.blit(self._background, (0, 0))

    def run(self):
        stop = False
        while not stop:
            self._time_delta = self._clock.tick(self._fps_max) / 1000.0

            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                # Si un de ces événements est de type QUIT
                if should_stop_pygame(event):
                    stop = True  # On arrête la boucle
                elif event.type == pygame_const.MOUSEBUTTONDOWN:
                    self.on_mouse_press()
                elif event.type == pygame_const.MOUSEBUTTONUP:
                    self.on_mouse_release()
                elif event.type == pygame_const.KEYDOWN:
                    self._key_press_handle(event.key)
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        self._button_pressed_handle(event.ui_element)

                self._ui_manager.process_events(event)

            keys = pygame.key.get_pressed()
            self._keys_pressed_handle(keys)

            pos = pygame.mouse.get_pos()
            self.actualize_screen(pos)

            pygame.display.flip()

    def on_mouse_release(self, **kwargs):
        self._mouse_is_holding_left = False

    def on_mouse_press(self, **kwargs):
        self._mouse_is_holding_left = True

    def _tick_clock(self):
        return self._clock.tick(self._fps_max)
