from uix.screens.ScreenPlay import *
from src.cars.CarAI import *


class GameSolo(GamePlay):
    def __init__(self, nn_file_path=None, track_path="track/track1.tra"):
        # Use super class
        GamePlay.__init__(self, track_path=track_path)
        # Check if the player is Human by looking at the neural net file
        self.is_human = nn_file_path is None

        if self.is_human:
            # Construct Human Car
            self.car = CarHuman(self.track, self.lidar_w, self.lidar_h)
        else:
            # Construct AI Car
            self.car = CarAI(nn_file_path, self.track, self.lidar_w, self.lidar_h)

        # Actualize Window
        self.actualize()

    def actualize(self):
        pygame.time.Clock().tick(FPS_MAX_init)  # Fixe le nbr max de FPS

        # BACKGROUND
        self.window.blit(self.background, (0, 0))

        # Get Next Move for AI
        if not self.is_human:
            self.car.actualize_direction_and_gas(self.car.predict_next_move())
        # Make next move
        self.car.move_car_and_refresh_LIDAR(self.window)

        # Display Fitness
        self.car.refresh_fitness_v2()
        self.display_fitness()
        """"""
        # PEDALS & Direction Arrows
        self.refresh_arrow_pedal()

        # Display car on window
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
        self.gen_track_background()  # Draw roads
        self.gen_LIDAR_background()  # Draw LIDAR rect

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


def run_play_human(**kwargs):
    # --- INIT Variables--- #
    stop = False
    if kwargs:
        track_path = kwargs["track_path"]
    else:
        track_path = list_track[0]

    # --- INIT GAME Window--- #

    game = GameSolo(track_path=track_path)

    # Boucle infinie
    while not stop:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                stop = True  # On arrête la boucle

        keys = pygame.key.get_pressed()
        if keys[pygame_const.K_DOWN]:  # If Down Arrow
            game.car.actualize_direction_or_gas(gas_BRAKE)
        elif keys[pygame_const.K_UP]:  # If Up Arrow
            game.car.actualize_direction_or_gas(gas_ON)
        else:  # If None of them
            game.car.actualize_direction_or_gas(gas_OFF)

        if keys[pygame_const.K_r]:  # If R
            # Reset car
            game.car.reset_car()

        if keys[pygame_const.K_LEFT]:  # If Left Arrow
            game.car.actualize_direction_or_gas(wheel_LEFT)
        elif keys[pygame_const.K_RIGHT]:  # If Right Arrow
            game.car.actualize_direction_or_gas(wheel_RIGHT)
        else:  # If None of them
            game.car.actualize_direction_or_gas(wheel_NONE)

        # Refresh
        game.actualize()


def run_play_ai(**kwargs):
    # --- INIT Variables--- #
    stop = False

    if "track_path" in kwargs:
        track_path = kwargs["track_path"]
    else:
        track_path = list_track[0]

    if "model_path" in kwargs:
        model_path = kwargs["model_path"]
    else:
        # model_path = "raw_models/nn1_dual_layers.net"
        # model_path = "results_training/first_result_race.h5"
        model_path = "dev/results_training_dev/tiny_izi_8144.h5"

    # --- INIT Game--- #

    game = GameSolo(nn_file_path=model_path,
                    track_path=track_path)

    # Boucle infinie
    while not stop:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                stop = True  # On arrête la boucle

            keys = pygame.key.get_pressed()
            if keys[pygame_const.K_r]:  #  If R is pressed, then reset
                game.car.reset_car()

        # Refresh
        game.actualize()


if __name__ == '__main__':
    human = True
    if human:
        run_play_human()
    else:
        run_play_ai()

# --- NOTA BENNE --- #

# image.set_colorkey((255,255,255)) #Rend le blanc (valeur RGB : 255,255,255) de l'image transparent

# pygame.key.set_repeat(400, 30) # 400 ms avant répétition, 30 ms entre chaque rép
