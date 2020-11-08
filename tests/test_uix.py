from src.usesful_func import start_pygame_headless

from src.uix.screens.ScreenHome import ScreenHome
from src.uix.screens.ScreenPlayHuman import ScreenPlayHuman
from src.uix.screens.ScreenPlayAI import ScreenPlayAI
from src.uix.screens.ScreenTrainRandomEvolv import ScreenTrainRandomEvolv
from src.uix.screens.ScreenDrawTrack import ScreenDrawTrack

start_pygame_headless()
track_path = "tracks/tiny.tra"
neural_net_path = "models/raw/nn_tiny.net"


def test_screen_home():
    screen = ScreenHome()
    assert screen


def test_screen_play_human():
    screen = ScreenPlayHuman(track_path=track_path)
    assert screen


def test_screen_play_ai():
    screen = ScreenPlayAI(nn_file_path=neural_net_path,
                          track_path=track_path)
    assert screen


def test_screen_train():
    screen = ScreenTrainRandomEvolv(nn_file_path=neural_net_path,
                                    track_path=track_path,
                                    save=False)
    assert screen


def test_screen_draw():
    screen = ScreenDrawTrack()
    assert screen
