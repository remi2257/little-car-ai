from .ScreenBase import ScreenBase

from src.objects.Track import *


class ScreenBasePlay(ScreenBase):
    def __init__(self, track_path, fps_max=FPS_MAX_init):
        super(ScreenBasePlay, self).__init__(fps_max=fps_max)

        # Generate track object
        self._track = Track(track_path)

        # Get infos on LIDAR's image size
        self._lidar_im_w, self._lidar_im_h = self.find_LIDAR_img_size(self._track.im_h)

        # Generate Window
        self._window_w = self._track.im_w + self._lidar_im_w + offset_LIDAR_grid_x
        self._window_h = self._track.im_h
        self._window = pygame.display.set_mode((self._window_w, self._window_h))

        # GEN ACTION IMGS (Direction & Pedals)
        self._actions_imgs = []
        # Actions are an enumeration which ends by wheel_NONE (which then, have the biggest value)
        for i in range(wheel_NONE + 1):
            img = pygame.image.load(img_pedals_arrows[i]).convert_alpha()
            width = img.get_width()
            height = img.get_height()
            ratio = float(width / height)
            img = pygame.transform.scale(img, (width_arrows_pedals, round(width_arrows_pedals / ratio)))

            self._actions_imgs.append(img)

        # Generate Background
        self._background = pygame.image.load(background_path).convert()

        self.gen_background()

    def actualize(self, pos=None):
        raise NotImplementedError

    def gen_background(self):
        raise NotImplementedError

    # Generate Track background by drawing roads
    def gen_track_background(self):
        for i in range(self._track.grid_h):
            for j in range(self._track.grid_w):
                small_name = self._track.get_road_name(i, j)
                if "x" in small_name:  # If grass, background already good
                    continue

                im_name = road_path + "road_{}.png".format(small_name)
                im = pygame.image.load(im_name).convert_alpha()
                im = pygame.transform.scale(im, (self._track.case_size, self._track.case_size))

                self._background.blit(im, (self._track.case_size * j, self._track.case_size * i))

    # read global variables to get the size of LIDAR's display
    def find_LIDAR_img_size(self, track_height):
        ratio = float(height_LIDAR) / width_LIDAR
        if ratio <= 1.0:
            return LIDAR_width_img, round(LIDAR_width_img * ratio)

        else:
            possible_height = ratio * LIDAR_width_img
            if possible_height + offset_LIDAR_grid_y > track_height:
                possible_height = track_height - offset_LIDAR_grid_y

            return round(possible_height / ratio), possible_height

    # Basically, a black rectangle :)
    def gen_LIDAR_background(self):
        # Generate LIDAR background
        rect_pos = tuple([self._track.im_w, offset_LIDAR_grid_y,
                          self._lidar_im_w, self._lidar_im_h])
        pygame.draw.rect(self._background, (0, 0, 0), rect_pos)
