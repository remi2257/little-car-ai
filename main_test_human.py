import pygame

from src.GameSolo import GameSolo
from src.const import *

# --- INIT Variable--- #

stop = False
# --- INIT PYGAME--- #

game = GameSolo(track_path="track/track_race_izi.tra")

# Boucle infinie
while not stop:
    for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
        if event.type == pygame_const.QUIT or (
                event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
            stop = True  # On arrête la boucle

    keys = pygame.key.get_pressed()
    if keys[pygame_const.K_DOWN]:  # Si "flèche bas"
        game.car.actualize_direction_or_gas(gas_BRAKE)
    elif keys[pygame_const.K_UP]:
        game.car.actualize_direction_or_gas(gas_ON)
    else:
        game.car.actualize_direction_or_gas(gas_OFF)

    if keys[pygame_const.K_r]:
        game.car.reset_car()

    if keys[pygame_const.K_LEFT]:
        game.car.actualize_direction_or_gas(dir_LEFT)
    elif keys[pygame_const.K_RIGHT]:
        game.car.actualize_direction_or_gas(dir_RIGHT)
    else:
        game.car.actualize_direction_or_gas(dir_NONE)

    # Refresh
    game.actualize()

# --- NOTA BENNE --- #

# image.set_colorkey((255,255,255)) #Rend le blanc (valeur RGB : 255,255,255) de l'image transparent

# pygame.key.set_repeat(400, 30) # 400 ms avant répétition, 30 ms entre chaque rép
