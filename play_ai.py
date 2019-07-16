from src.GameSolo import GameSolo
from src.const import *
import pygame

import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)


def run_play_ai():
    # --- INIT Variable--- #

    stop = False

    # --- INIT PYGAME--- #
    # model_path = "models/nn1.net"
    # model_path = "results/first_result_race.h5"
    model_path = "results/tiny_8144.h5"
    # model_path = "results/race1_6603.h5"
    game = GameSolo(nn_file_path=model_path,
                    track_path="track/track0.tra")

    # Boucle infinie
    while not stop:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                stop = True  # On arrête la boucle

            keys = pygame.key.get_pressed()
            if keys[pygame_const.K_r]:
                game.car.reset_car()

        # Refresh
        game.actualize()


if __name__ == '__main__':
    run_play_ai()

# --- NOTA BENNE --- #

# image.set_colorkey((255,255,255)) #Rend le blanc (valeur RGB : 255,255,255) de l'image transparent

# pygame.key.set_repeat(400, 30) # 400 ms avant répétition, 30 ms entre chaque rép
