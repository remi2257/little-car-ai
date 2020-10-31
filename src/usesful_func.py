import pygame
import pygame.locals as pygame_const

from .const import game_name

list_break = [pygame_const.K_q, pygame_const.K_ESCAPE]


def start_pygame():
    pygame.init()
    pygame.display.set_caption(game_name)


def should_stop_pygame(event):
    if event.type == pygame_const.QUIT:
        return True
    if event.type == pygame_const.KEYDOWN and event.key in list_break:
        return True
    return False
