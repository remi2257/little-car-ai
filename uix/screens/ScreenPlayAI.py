from uix.screens.abstract.ScreenPlaySolo import ScreenPlaySolo
from src.cars.CarAI import CarAI
from src.objects.NeuralNet import NeuralNet


class ScreenPlayAI(ScreenPlaySolo):

    def __init__(self, nn_file_path, track_path, **kwargs):
        super(ScreenPlayAI, self).__init__(track_path=track_path, **kwargs)

        neural_net = NeuralNet.from_path(nn_file_path)
        self._car = CarAI(self._track, neural_net)

    def _keys_pressed_handle(self, keys):
        pass

    def actualize_screen(self, pos=None):
        super(ScreenPlayAI, self).actualize_screen(pos)
        self._car.actualize_direction_and_gas(self._car.predict_next_move())


def run_play_ai(track_path, nn_file_path, **kwargs):
    screen = ScreenPlayAI(nn_file_path=nn_file_path, track_path=track_path, **kwargs)
    screen.run()


if __name__ == '__main__':
    run_play_ai(
        nn_file_path="models/trained/tiny_player.h5",
        track_path="tracks/race_tiny.tra"
    )
