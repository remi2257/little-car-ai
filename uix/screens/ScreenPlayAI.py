from uix.screens.abstract.ScreenPlaySolo import ScreenPlaySolo
from src.cars.CarAI import CarAI


class ScreenPlayAI(ScreenPlaySolo):

    def __init__(self, model_path, track_path):
        super(ScreenPlayAI, self).__init__(track_path=track_path)
        self._car = CarAI(model_path, self._track)

        self.actualize()

    def _keys_pressed_handle(self, keys):
        pass

    def actualize(self, pos=None):
        super(ScreenPlayAI, self).actualize(pos)
        self._car.actualize_direction_and_gas(self._car.predict_next_move())


def run_play_ai(track_path, model_path):
    screen = ScreenPlayAI(model_path=model_path, track_path=track_path)
    screen.run()


if __name__ == '__main__':
    run_play_ai(
        model_path="results_training/good_tiny_cp.h5",
        track_path="tracks/race_tiny.tra"
    )
