from src.GameTrain import GameTrain
from src.const import *
import pygame

import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)


def run_train():
    # --- INIT Variable--- #

    stop = False

    # --- INIT PYGAME--- #

    game = GameTrain(
        # nn_file_path="models/nn1.net",
        nn_file_path="models/nn_tiny.net",
        # nn_file_path="results/first_tiny.h5",
        # nn_file_path="results/race1_6603.h5",

        track_path=list_track[0],

        save=True,
        # save=False,

        fps_max=240
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
