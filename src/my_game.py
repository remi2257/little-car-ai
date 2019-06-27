import pygame
from src.cars import *
from src.track import *

background_path = "images/background.jpg"


class Game:
    def __init__(self, track_path="track/track1.tra"):
        pygame.init()

        pygame.time.Clock().tick(FPS_MAX)  # Fixe le nbr max de FPS
        # pygame.key.set_repeat(30, 30)

        pygame.display.set_caption("My Game")
        self.track = Track(track_path)
        self.window = pygame.display.set_mode((self.track.grid_size * self.track.grid_w,
                                               self.track.grid_size * self.track.grid_h))
        self.background = pygame.image.load(background_path).convert()
        self.track.gen_background(self.background)
        # self.background = pygame.transform.scale(self.background, (size_larg, size_haut))

        # RESIZABLE
        self.car = Car(self.track)
        self.cars_bot = []
        for _ in range(nbr_bots):
            self.cars_bot.append(CarBot(self.track))

        # self.window.blit(self.background, (0, 0))
        # self.window.blit(self.car.actual_img, (self.car.x, self.car.y))
        # for car in self.cars_bot:
        #     car.move_car_bot(self.track)
        #     self.window.blit(car.actual_img, car.get_position_left_top())
        #
        # pygame.display.flip()
        self.actualize()

    def actualize(self):
        pygame.time.Clock().tick(FPS_MAX)  # Fixe le nbr max de FPS

        # BACKGROUND
        self.window.blit(self.background, (0, 0))

        # CAR PLAYER
        self.car.move_car(self.window)
        self.window.blit(self.car.actual_img, self.car.get_position_left_top())

        # BOTS CAR
        for car in self.cars_bot:
            car.move_car_bot(self.track)
            self.window.blit(car.actual_img, car.get_position_left_top())
            # pygame.draw.rect(self.window, (0, 0, 255), (
            # car.position_car.x, car.position_car.y,
            # car.position_car.w, car.position_car.h)
            #              , 3)


        # REFRESH
        pygame.display.flip()


    def predict_next_move(self):
        pass