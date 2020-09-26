import pygame
import pygame.locals as pygame_const

from src.const import font_size_global
from src.usesful_func import start_pygame, should_stop_pygame


class ScreenBase:
    def __init__(self, fps_max=60):
        start_pygame()

        self._fps_max = fps_max
        self._clock = pygame.time.Clock()

        self._mouse_is_holding_left = False

        # Font
        self._font = pygame.font.Font('freesansbold.ttf', int(font_size_global / 1.2))
        self._font_h = self._font.get_height()

    def _key_press_handle(self, key):
        pass

    def _keys_pressed_handle(self, keys):
        pass

    def actualize(self, pos=None):
        raise NotImplementedError

    def gen_background(self):
        raise NotImplementedError

    def run(self):
        stop = False
        while not stop:
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
            keys = pygame.key.get_pressed()
            self._keys_pressed_handle(keys)

            pos = pygame.mouse.get_pos()
            self.actualize(pos)

    def on_mouse_release(self, **kwargs):
        self._mouse_is_holding_left = False

    def on_mouse_press(self, **kwargs):
        self._mouse_is_holding_left = True

    def _tick_clock(self):
        self._clock.tick(self._fps_max)
