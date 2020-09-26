from .ScreenBasePlay import *


class ScreenPlaySolo(ScreenBasePlay):
    def __init__(self, track_path):
        ScreenBasePlay.__init__(self, track_path=track_path)

        self._car = None

    def actualize(self, pos=None):
        self._tick_clock()
        # BACKGROUND
        self._window.blit(self._background, (0, 0))

        # Make next move
        self._car.move_car_and_refresh_LIDAR(self._window)
        # Display car on window
        self._window.blit(self._car.actual_img, self._car.get_position_left_top())
        # PEDALS & Direction Arrows
        self.refresh_arrow_pedal()

        # Compute Display Fitness
        self._car.refresh_fitness_v2()
        self.display_fitness()

        # REFRESH
        pygame.display.flip()

    def gen_background(self):
        self.gen_track_background()  # Draw roads
        self.gen_LIDAR_background()  # Draw LIDAR rect

    def refresh_arrow_pedal(self):
        self.gen_arrows_pedals(self._car.last_dir_cmd, self._car.last_gas_cmd)

    def gen_arrows_pedals(self, dir_cmd, gas_cmd):
        self.gen_arrow(dir_cmd)
        self.gen_pedals(gas_cmd)

    def gen_arrow(self, dir_cmd):
        self._window.blit(self._actions_imgs[dir_cmd], (self._window_w - width_arrows_pedals - offset_arrows_pedals,
                                                        self._lidar_im_h + 5 * offset_arrows_pedals))

    def gen_pedals(self, gas_cmd):
        self._window.blit(self._actions_imgs[gas_cmd], (self._window_w - width_arrows_pedals - offset_arrows_pedals,
                                                        self._lidar_im_h + 6 * offset_arrows_pedals))

    def display_fitness(self):
        text = self._font.render("Fitness: {:.0f}".format(self._car.fitness), True, COLOR_GREEN)

        self._window.blit(text, (self._window_w - 200,
                                 self._window_h - 100))
