import os
from datetime import datetime

from src.const import FPS_MAX_max
from .ScreenBasePlay import *

# - Display Imports
import matplotlib
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
from matplotlib.ticker import MaxNLocator
import pygame.locals as pygame_const

matplotlib.use("Agg")

path_train_save = "results_training/"


class ScreenBaseTrain(ScreenBasePlay):

    def __init__(self, track_path, nn_file_path, save, **kwargs):
        ScreenBasePlay.__init__(self, track_path=track_path,
                                window_size=(big_window_larg, big_window_haut), **kwargs)

        self._save = save
        if self._save:
            self._save_folder_model = "".join([
                path_train_save,
                datetime.now().strftime("%d_%m__%H_%M_%S"),
                "_", nn_file_path.split("/")[1].split(".")[0],
                "_", track_path.split("/")[1].split(".")[0],
                "/",

            ])
            if not os.path.exists(self._save_folder_model):
                os.makedirs(self._save_folder_model)

        self._carsAI = []

        # Fitness Information #
        self._best_actual_fitness = 0
        self._mean_fitness = 0
        self._best_fitness_list = [0]
        self._best_fitness_ever = 0

        # Generation Infos
        self._gen_id = 1
        self._gen_duration = 0

        # Plot settings
        # 1 px = 0.010416666666819 inches
        l_fig = 2.0 * 0.010416666666819 * (self._window_w - self._track.im_w)
        self._fig = pylab.figure(figsize=[l_fig, l_fig],  # Inches
                                 dpi=50,
                                 )
        self._fig_ax = self._fig.gca()
        self._list_y_text = [self._track.im_h // 50 + i * self._font_h for i in range(20)]

        self.gen_background()

    def actualize_screen(self, pos=None):
        super(ScreenBaseTrain, self).actualize_screen(pos)

    def _key_press_handle(self, key):
        if key == pygame_const.K_KP_PLUS:
            self.increase_fps()
        elif key == pygame_const.K_KP_MINUS:
            self.decrease_fps()

    def start_new_gen(self):
        raise NotImplementedError

    # def display_infos_fitness_n_fps(self):
    #     raise NotImplementedError

    def refresh_fitness_plot(self):
        self._fig_ax.clear()
        self._fig_ax.plot(range(1, len(self._best_fitness_list) + 1), self._best_fitness_list, 'ro')
        self._fig_ax.plot(range(1, len(self._best_fitness_list) + 1), self._best_fitness_list)
        plt.ylim((0, self._best_fitness_ever + 10))
        self._fig_ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        canvas = agg.FigureCanvasAgg(self._fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        # self.window.blit(surf, (self.track.im_w - 50, 400))
        self._background.blit(surf, (self._track.im_w - 50, self._list_y_text[-1]))

    def save_gen_best_model(self):
        best_car = self._carsAI[0]
        new_model_name = self._save_folder_model + "Gen_{}_Fitness_{}.h5".format(self._gen_id,
                                                                                 int(best_car.fitness))

        best_car.save_neural_network(new_model_name)

    def update_duration_limit(self, ratio):
        raise NotImplementedError

    def increase_fps(self):
        self._fps_max = min(FPS_MAX_max, self._fps_max + 10)

    def decrease_fps(self):
        self._fps_max = max(FPS_MAX_init, self._fps_max - 10)
