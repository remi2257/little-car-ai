from uix.screens.abstract.ScreenPlaySolo import ScreenPlaySolo
from src.cars.CarHuman import CarHuman
# import pygame.locals as pygame_const
from src.const import *


class ScreenPlayHuman(ScreenPlaySolo):

    def __init__(self, track_path="track/track1.tra"):
        super(ScreenPlayHuman, self).__init__(track_path=track_path)
        self._car = CarHuman(self._track, self._lidar_im_w, self._lidar_im_h)

        self.actualize()

    def _keys_pressed_handle(self, keys):
        if keys[pygame_const.K_DOWN]:  # If Down Arrow
            self._car.actualize_direction_or_gas(gas_BRAKE)
        elif keys[pygame_const.K_UP]:  # If Up Arrow
            self._car.actualize_direction_or_gas(gas_ON)
        else:  # If None of them
            self._car.actualize_direction_or_gas(gas_OFF)

        if keys[pygame_const.K_r]:  # If R
            # Reset car
            self._car.reset_car()

        if keys[pygame_const.K_LEFT]:  # If Left Arrow
            self._car.actualize_direction_or_gas(wheel_LEFT)
        elif keys[pygame_const.K_RIGHT]:  # If Right Arrow
            self._car.actualize_direction_or_gas(wheel_RIGHT)
        else:  # If None of them
            self._car.actualize_direction_or_gas(wheel_NONE)


def run_play_human(track_path):
    screen = ScreenPlayHuman(track_path=track_path)
    screen.run()


if __name__ == '__main__':
    run_play_human(
        track_path="tracks/race_tiny.tra"
    )
