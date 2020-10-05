import pygame.locals as pygame_const

from uix.screens.abstract.ScreenPlaySolo import ScreenPlaySolo
from src.cars.CarHuman import CarHuman
from src.cars.Car import CommandGas, CommandDir


class ScreenPlayHuman(ScreenPlaySolo):

    def __init__(self, track_path, **kwargs):
        super(ScreenPlayHuman, self).__init__(track_path=track_path, **kwargs)
        self._car = CarHuman(self._track)

    def _keys_pressed_handle(self, keys):
        if keys[pygame_const.K_r]:  # If R
            # Reset car
            self._car.reset_car()
            return

        if keys[pygame_const.K_DOWN]:  # If Down Arrow
            self._car.actualize_direction_or_gas(CommandGas.BRAKE)
        elif keys[pygame_const.K_UP]:  # If Up Arrow
            self._car.actualize_direction_or_gas(CommandGas.ON)
        else:  # If None of them
            self._car.actualize_direction_or_gas(CommandGas.OFF)

        if keys[pygame_const.K_LEFT]:  # If Left Arrow
            self._car.actualize_direction_or_gas(CommandDir.LEFT)
        elif keys[pygame_const.K_RIGHT]:  # If Right Arrow
            self._car.actualize_direction_or_gas(CommandDir.RIGHT)
        else:  # If None of them
            self._car.actualize_direction_or_gas(CommandDir.NONE)


def run_play_human(track_path, **kwargs):
    screen = ScreenPlayHuman(track_path=track_path, **kwargs)
    screen.run()


if __name__ == '__main__':
    run_play_human(
        track_path="tracks/race_tiny.tra"
    )
