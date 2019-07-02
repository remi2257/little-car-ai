from src.Game import *


class GameSolo(Game):
    def __init__(self, nn_file_path=None, track_path="track/track1.tra"):

        Game.__init__(self, track_path=track_path)
        self.is_human = nn_file_path is None

        if self.is_human:
            self.car = CarHuman(self.track, self.lidar_w, self.lidar_h)
        else:
            self.car = CarAI(nn_file_path, self.track, self.lidar_w, self.lidar_h)

        self.actualize()

    def actualize(self):
        pygame.time.Clock().tick(FPS_MAX_init)  # Fixe le nbr max de FPS

        # BACKGROUND
        self.window.blit(self.background, (0, 0))

        # Get Next Move
        if not self.is_human:
            self.car.actualize_direction_and_gas(self.car.predict_next_move())

        self.car.move_car_and_refresh_LIDAR(self.window)
        self.car.refresh_fitness()
        self.display_fitness()
        # PEDALS
        self.refresh_arrow_pedal()

        self.window.blit(self.car.actual_img, self.car.get_position_left_top())

        # BOTS CAR
        for car in self.cars_bot:
            car.move_car_bot(self.track)
            self.window.blit(car.actual_img, car.get_position_left_top())
            # pygame.draw.rect(self.window, (0, 0, 255), (car.position_car.x, car.position_car.y,
            # car.position_car.w, car.position_car.h), 3)

        # REFRESH
        pygame.display.flip()

    def gen_background(self):
        self.gen_track_background()
        self.gen_LIDAR_background()

    def refresh_arrow_pedal(self):
        self.gen_arrows_pedals(self.car.last_dir_cmd, self.car.last_gas_cmd)

    def gen_arrows_pedals(self, dir_cmd, gas_cmd):
        self.gen_arrow(dir_cmd)
        self.gen_pedals(gas_cmd)

    def gen_arrow(self, dir_cmd):
        self.window.blit(self.actions_imgs[dir_cmd], (self.window_w - width_arrows_pedals - offset_arrows_pedals,
                                                      self.lidar_h + 5 * offset_arrows_pedals))

    def gen_pedals(self, gas_cmd):
        self.window.blit(self.actions_imgs[gas_cmd], (self.window_w - width_arrows_pedals - offset_arrows_pedals,
                                                      self.lidar_h + 6 * offset_arrows_pedals))

    def display_fitness(self):
        text = self.font.render("Fitness: {:.0f}".format(self.car.fitness), True, COLOR_GREEN)

        self.window.blit(text, (self.window_w - 200,
                                self.window_h - 100))
