import pygame

from src.Games.GameSolo import GameSolo
from src.const import *


def run_play_human(**kwargs):
    # --- INIT Variables--- #
    stop = False
    if kwargs:
        track_path = kwargs["track_path"]
    else:
        track_path = list_track[0]

    # --- INIT GAME Window--- #

    game = GameSolo(track_path=track_path)

    # Boucle infinie
    while not stop:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                stop = True  # On arrête la boucle

        keys = pygame.key.get_pressed()
        if keys[pygame_const.K_DOWN]:  # If Down Arrow
            game.car.actualize_direction_or_gas(gas_BRAKE)
        elif keys[pygame_const.K_UP]:  # If Up Arrow
            game.car.actualize_direction_or_gas(gas_ON)
        else:  # If None of them
            game.car.actualize_direction_or_gas(gas_OFF)

        if keys[pygame_const.K_r]:  # If R
            # Reset car
            game.car.reset_car()

        if keys[pygame_const.K_LEFT]:  # If Left Arrow
            game.car.actualize_direction_or_gas(wheel_LEFT)
        elif keys[pygame_const.K_RIGHT]:  # If Right Arrow
            game.car.actualize_direction_or_gas(wheel_RIGHT)
        else:  # If None of them
            game.car.actualize_direction_or_gas(wheel_NONE)

        # Refresh
        game.actualize()


if __name__ == '__main__':
    run_play_human()

# --- NOTA BENNE --- #

# image.set_colorkey((255,255,255)) #Rend le blanc (valeur RGB : 255,255,255) de l'image transparent

# pygame.key.set_repeat(400, 30) # 400 ms avant répétition, 30 ms entre chaque rép
