import pygame

from src.objects.Track import Track
from src.const import FPS_MAX_init, background_path, roads_path, big_window_haut, big_window_larg
from .ScreenBase import ScreenBase


class ScreenBasePlay(ScreenBase):
    def __init__(self, track_path, fps_max=FPS_MAX_init, **kwargs):
        if "window_size" not in kwargs:
            kwargs["window_size"] = (big_window_haut, big_window_larg)
        super(ScreenBasePlay, self).__init__(fps_max=fps_max, **kwargs)

        # Generate track object
        self._track = Track(track_path)

    def actualize(self, pos=None):
        raise NotImplementedError

    def gen_background(self):
        self._background = pygame.image.load(background_path).convert()
        self._gen_track_background()  # Draw roads

    # Generate Track background by drawing roads
    def _gen_track_background(self):
        for i in range(self._track.grid_h):
            for j in range(self._track.grid_w):
                small_name = self._track.get_road_name(i, j)
                if "x" in small_name:  # If grass, background already good
                    continue

                im_name = roads_path + "road_{}.png".format(small_name)
                im = pygame.image.load(im_name).convert_alpha()
                im = pygame.transform.scale(im, (self._track.case_size, self._track.case_size))

                self._background.blit(im, (self._track.case_size * j, self._track.case_size * i))
