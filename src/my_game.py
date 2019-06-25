import pygame
from src.cars import *
from src.track import *

background_path = "images/background.jpg"


class Game:
    def __init__(self, track_path="track/track1.tra"):
        pygame.init()
        pygame.time.Clock().tick(30)

        pygame.display.set_caption("My Game")

        self.window = pygame.display.set_mode((size_larg, size_haut), )  # RESIZABLE
        self.background = pygame.image.load(background_path).convert()
        # self.background = pygame.transform.scale(self.background, (size_larg, size_haut))

        self.track = Track(track_path, self.background)

        self.car = Car()
        self.cars_bot = []
        for _ in range(nbr_bots):
            self.cars_bot.append(CarBot(self.track))

        self.window.blit(self.background, (0, 0))
        self.window.blit(self.car.actual_img, (self.car.x, self.car.y))

        pygame.display.flip()

    def actualize(self):
        pygame.time.Clock().tick(FPS_MAX)  # Fixe le nbr max de FPS

        # BACKGROUND
        self.window.blit(self.background, (0, 0))

        # CAR PLAYER
        self.car.move_car()
        self.window.blit(self.car.actual_img, (self.car.x, self.car.y))

        # BOTS CAR
        for car in self.cars_bot:
            car.move_car_bot(self.track)
            self.window.blit(car.actual_img, (car.x, car.y))

        # REFRESH
        pygame.display.flip()
