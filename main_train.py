from src.GameTrain import GameTrain
from src.const import *
import pygame

import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)

# --- INIT Variable--- #

stop = False

# --- INIT PYGAME--- #

game = GameTrain(
    nn_file_path="models/nn1.net",
    track_path="track/track_race1.tra",
    save=True,

    # nn_file_path="results/tiny_track.h5",
    # track_path="track/track_race_izi.tra",
    # save=False,
)

# Boucle infinie
while not stop:
    for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
        if event.type == pygame_const.QUIT or (
                event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
            stop = True  # On arrête la boucle

    # Refresh
    game.actualize()
