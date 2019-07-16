from src.GameMenu import *
from src.const import *
import pygame

import os


def run_menu():
    # --- INIT Variable--- #

    stop = None

    # --- INIT PYGAME--- #

    game = GameMenu()

    # Boucle infinie
    while stop is None:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                stop = 0  # On arrête la boucle
            if event.type == pygame_const.MOUSEBUTTONDOWN:
                game.is_holding = True
            if event.type == pygame_const.MOUSEBUTTONUP:
                game.is_holding = False
                stop = game.action_selected()
        pos = pygame.mouse.get_pos()

        game.actualize(pos)

    return stop


if __name__ == '__main__':
    run_menu()
