from datetime import datetime

import matplotlib
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
from matplotlib.ticker import MaxNLocator

from .ScreenBasePlay import *

matplotlib.use("Agg")


class ScreenBaseTrain(ScreenBasePlay):
    def __init__(self, nn_file_path="raw_models/nn1_dual_layers.net", track_path="track/track1.tra", save=True,
                 fps_max=FPS_MAX_init):
        ScreenBasePlay.__init__(self, track_path=track_path, fps_max=fps_max)

        self.save = save
        if self.save:
            self.save_folder_model = "".join([
                path_train_save,
                datetime.now().strftime("%d_%m__%H_%M_%S"),
                "_", nn_file_path.split("/")[1].split(".")[0],
                "_", track_path.split("/")[1].split(".")[0],
                "/",

            ])
            if not os.path.exists(self.save_folder_model):
                os.makedirs(self.save_folder_model)

        self.carsAI = []

        # Fitness Information #
        self.best_actual_fitness = 0
        self.mean_fitness = 0
        self.best_fitness_list = [0]
        self.best_fitness_ever = 0

        # Generation Infos
        self.gen_id = 1
        self.gen_duration = 0

        # Plot settings
        # 1 px =	0.010416666666819 inches
        l_fig = 2.3 * 0.010416666666819 * (self._window_w - self._track.__im_w)
        self.fig = pylab.figure(figsize=[l_fig, l_fig],  # Inches
                                dpi=50,
                                )
        self.fig_ax = self.fig.gca()
        self.list_y_text = [self._track.im_h // 50 + i * self._font_h for i in range(20)]

    def actualize(self):
        raise NotImplementedError

    def start_new_gen(self):
        raise NotImplementedError

    def gen_background(self):
        self.gen_track_background()

    def display_infos_fitness_n_FPS(self):
        raise NotImplementedError

    def refresh_fitness_plot(self):
        self.fig_ax.clear()
        self.fig_ax.plot(range(1, len(self.best_fitness_list) + 1), self.best_fitness_list, 'ro')
        self.fig_ax.plot(range(1, len(self.best_fitness_list) + 1), self.best_fitness_list)
        plt.ylim((0, self.best_fitness_ever + 10))
        self.fig_ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        # self.window.blit(surf, (self.track.im_w - 50, 400))
        self._background.blit(surf, (self._track.__im_w - 50, 400))

    def save_gen_best_model(self):
        new_model_name = self.save_folder_model + "Gen_{}_Fitness_{}.h5".format(self.gen_id,
                                                                                int(self.carsAI[0].fitness))

        self.carsAI[0].neural_net.model.save(new_model_name)

    def save_game(self):
        import pickle

        pickle.dump(self, open(self.save_folder_model + '_game.p', "wb"))

    def update_duration_limit(self, ratio):
        raise NotImplementedError

    def increase_FPS(self):
        self.FPS_MAX += 10

    def decrease_FPS(self):
        self.FPS_MAX = max(FPS_MAX_init, self.FPS_MAX - 10)


def load_game(path_game):
    import pickle

    return pickle.load(open(path_game, "rb"))
