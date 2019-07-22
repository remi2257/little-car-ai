import os

import pygame
import tensorflow as tf

from src.Games.GameTrainRandomEvolv import GameTrainRandomEvolv
from src.const import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)


def run_train(**kwargs):
    # --- INIT Variable--- #

    stop = False

    if "track_path" in kwargs:
        track_path = kwargs["track_path"]
    else:
        track_path = list_track[0]

    if "model_path" in kwargs:
        model_path = kwargs["model_path"]
    else:
        model_path = "raw_models/nn_tiny.net"

    if "save_train" in kwargs:
        save = kwargs["save_train"]
    else:
        save = True

    # --- INIT Game--- #

    game = GameTrainRandomEvolv(
        nn_file_path=model_path,

        track_path=track_path,

        save=save,

        fps_max=FPS_MAX_max,
    )

    # Boucle infinie
    while not stop:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                stop = True  # On arrête la boucle
            if event.type == pygame_const.KEYDOWN and event.key == pygame_const.K_DOWN:
                game.decrease_FPS()
            if event.type == pygame_const.KEYDOWN and event.key == pygame_const.K_UP:
                game.increase_FPS()

        # Refresh
        game.actualize()


if __name__ == '__main__':
    run_train()
