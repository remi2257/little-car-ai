from src.CarBot import *
from src.CarAI import *
from src.track import *

background_path = "images/background.jpg"


class Game:
    def __init__(self, nn_file_path=None, track_path="track/track1.tra"):
        self.is_human = nn_file_path is None
        pygame.init()

        pygame.time.Clock().tick(FPS_MAX)  # Fixe le nbr max de FPS
        # pygame.key.set_repeat(30, 30)

        pygame.display.set_caption("My Game")
        self.track = Track(track_path)

        self.lidar_w, self.lidar_h = self.find_LIDAR_img_size(self.track.im_h)

        # Generate Window
        self.window_w = self.track.im_w + self.lidar_w + offset_LIDAR_grid_x
        self.window_h = self.track.im_h
        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        # GEN ACTION IMGS
        self.actions_imgs = []
        for i in range(dir_NONE + 1):
            img = pygame.image.load(img_pedals_arrows[i]).convert_alpha()
            width = img.get_width()
            height = img.get_height()
            ratio = float(width / height)
            img = pygame.transform.scale(img, (width_arrows_pedals, round(width_arrows_pedals / ratio)))

            self.actions_imgs.append(img)

        # Generate Background
        self.background = pygame.image.load(background_path).convert()

        self.gen_background()

        if self.is_human:
            self.car = CarHuman(self.track, self.lidar_w, self.lidar_h)
        else:
            self.car = CarAI(nn_file_path, self.track, self.lidar_w, self.lidar_h)

        self.cars_bot = []
        for _ in range(nbr_bots):
            self.cars_bot.append(CarBot(self.track))

        self.actualize()

    def actualize(self):
        pygame.time.Clock().tick(FPS_MAX)  # Fixe le nbr max de FPS

        # BACKGROUND
        self.window.blit(self.background, (0, 0))
        self.refresh_arrow_pedal()

        # CAR PLAYER
        self.car.move_car_and_refresh_window(self.window)

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
        return self.car.predict_next_move()

    def find_LIDAR_img_size(self, track_height):
        ratio = float(height_LIDAR) / width_LIDAR
        if ratio <= 1.0:
            return LIDAR_width_img, round(LIDAR_width_img * ratio)

        else:
            possible_height = ratio * LIDAR_width_img
            if possible_height + offset_LIDAR_grid_y > track_height:
                possible_height = track_height - offset_LIDAR_grid_y

            return round(possible_height / ratio), possible_height

    def gen_background(self):
        # Generate Track
        for i in range(self.track.grid_h):
            for j in range(self.track.grid_w):
                im_name = track_part_1w[self.track.grid[i][j]]
                if im_name is None:
                    continue
                self.track.start_spots.append([i, j])
                self.track.grid_practicable[i][j] = True
                im = pygame.image.load(im_name).convert_alpha()
                im = pygame.transform.scale(im, (self.track.grid_size, self.track.grid_size))

                self.background.blit(im, (self.track.grid_size * j, self.track.grid_size * i))

        random.shuffle(self.track.start_spots)

        # Generate LIDAR background
        rect_pos = tuple([self.track.im_w, offset_LIDAR_grid_y,
                          self.lidar_w, self.lidar_h])
        pygame.draw.rect(self.background, (0, 0, 0), rect_pos)

        # Generate Arrows & Pedals

        # self.gen_arrows_pedals(dir_NONE, gas_OFF)

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
