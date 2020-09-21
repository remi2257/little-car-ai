import pygame

from src.Menu.MenuWindow import MenuWindow
from src.const import *


def run_main_menu():
    # --- INIT Variable--- #

    should_stop = None

    # --- INIT Menu Window --- #

    game = MenuWindow()

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
    run_main_menu()
