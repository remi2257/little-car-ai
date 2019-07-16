from src.CarBot import *
from src.CarAI import *
from src.Track import *
from pygame.font import Font


class GamePlay:
    def __init__(self, track_path="track/track1.tra", fps_max=FPS_MAX_init):

        pygame.init()

        self.FPS_MAX = fps_max
        pygame.time.Clock().tick(self.FPS_MAX)  # Fixe le nbr max de FPS
        # pygame.key.set_repeat(30, 30)

        pygame.display.set_caption("Little Car AI")
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

        self.cars_bot = []
        for _ in range(nbr_bots):
            self.cars_bot.append(CarBot(self.track))

        # Font
        self.font = Font('freesansbold.ttf', font_size)

    def actualize(self):
        raise NotImplementedError

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
        raise NotImplementedError

    def gen_track_background(self):
        start_points = []
        # Generate Track
        for i in range(self.track.grid_h):
            for j in range(self.track.grid_w):
                im_name = track_part_1w[self.track.grid[i][j]]
                if im_name is None:
                    continue
                if self.track.grid[i][j].startswith("s"):
                    start_points.append(tuple([i, j]))
                self.track.start_spots_bot.append([i, j])
                self.track.grid_practicable[i][j] = True
                im = pygame.image.load(im_name).convert_alpha()
                im = pygame.transform.scale(im, (self.track.grid_size, self.track.grid_size))

                self.background.blit(im, (self.track.grid_size * j, self.track.grid_size * i))

        random.shuffle(self.track.start_spots_bot)
        if start_points:
            init_car_y_grid, init_car_x_grid = random.choice(start_points)
            self.track.init_car_y = self.track.grid_size * (init_car_y_grid + 2 / 5)
            self.track.init_car_x = self.track.grid_size * (init_car_x_grid + 2 / 5)

    def gen_LIDAR_background(self):
        # Generate LIDAR background
        rect_pos = tuple([self.track.im_w, offset_LIDAR_grid_y,
                          self.lidar_w, self.lidar_h])
        pygame.draw.rect(self.background, (0, 0, 0), rect_pos)