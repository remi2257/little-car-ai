from src.usesful_func import start_pygame, should_stop_pygame
import pygame
import pygame.locals as pygame_const


class ScreenBase:
    def __init__(self):
        start_pygame()
        self._mouse_is_holding_left = False

    def keydown_handle(self, key):
        pass

    def actualize(self, pos=None):
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
                # if pygame.mouse.get_pressed()[0]:  # See if the user has clicked or dragged their mouse
                elif event.type == pygame_const.KEYDOWN:
                    self.keydown_handle(event.key)
            pos = pygame.mouse.get_pos()

            self.actualize(pos)

    def on_mouse_release(self, **kwargs):
        self._mouse_is_holding_left = False

    def on_mouse_press(self, **kwargs):
        self._mouse_is_holding_left = True
