from src.Game import *

from datetime import datetime
import os

import matplotlib
from matplotlib.ticker import MaxNLocator
import matplotlib.backends.backend_agg as agg
import pylab
import matplotlib.pyplot as plt

matplotlib.use("Agg")


class GameTrain(Game):
    def __init__(self, nn_file_path=None, track_path="track/track1.tra"):

        self.save_folder_model = path_train_save + datetime.now().strftime("%d_%m__%H_%M_%S") + "/"
        if not os.path.exists(self.save_folder_model):
            os.makedirs(self.save_folder_model)

        Game.__init__(self, track_path=track_path)

        self.carsAI = []
        self.best_actual_fitness = 0
        self.mean_fitness = 0
        self.best_fitness_list = [0]
        self.best_fitness_ever = 0

        self.mutation_rate = init_mutation_rate

        self.gen_id = 1
        self.gen_duration = 0
        self.gen_duration_limit = generation_duration_in_sec * FPS_MAX

        for _ in range(nbr_AI_per_gen):
            self.carsAI.append(CarAI(nn_file_path, self.track, self.lidar_w, self.lidar_h))

        self.fig = pylab.figure(figsize=[4, 4],  # Inches
                                dpi=50,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                                )
        self.fig_ax = self.fig.gca()

        self.clock = pygame.time.Clock()

        self.actualize()

    def actualize(self):
        self.clock.tick(FPS_MAX)  # Fixe le nbr max de FPS
        self.gen_duration += 1
        # plt.xlim((1, self.gen_duration))

        if self.gen_duration >= self.gen_duration_limit:
            self.start_new_gen()

        # BACKGROUND
        self.window.blit(self.background, (0, 0))

        for carAI in self.carsAI:
            # Get Next Move
            carAI.actualize_direction_and_gas(carAI.predict_next_move())
            carAI.refresh_fitness()

        list_fitness = [c.fitness for c in self.carsAI]
        self.mean_fitness = np.mean(list_fitness)
        self.best_actual_fitness = max(list_fitness)
        if self.best_actual_fitness > self.best_fitness_list[-1]:
            self.best_fitness_list[-1] = self.best_actual_fitness
        self.best_fitness_ever = max(self.best_fitness_ever, self.best_actual_fitness)

        for carAI in self.carsAI:
            if carAI.fitness == self.best_actual_fitness:
                carAI.change_to_leader_img()
            # CAR PLAYER
            carAI.move_car_and_refresh_LIDAR()

            self.window.blit(carAI.actual_img, carAI.get_position_left_top())

        # BOTS CAR
        for car in self.cars_bot:
            car.move_car_bot(self.track)
            self.window.blit(car.actual_img, car.get_position_left_top())

        # REFRESH
        self.display_fitness()
        self.display_fps()
        pygame.display.flip()

    def start_new_gen(self):
        self.carsAI = sorted(self.carsAI, key=lambda x: x.fitness, reverse=True)
        self.save_best_model()

        best_fitness = np.array([car.fitness for car in self.carsAI[0:nbr_survivors]])
        weight_best_fitness = best_fitness / np.sum(best_fitness)

        self.best_fitness_list.append(0)

        self.gen_id += 1
        self.gen_duration = 0
        self.mutation_rate *= decay_mutation_rate
        self.gen_duration_limit += generation_duration_increase * FPS_MAX

        for i in range(nbr_AI_per_gen):
            self.carsAI[i].reset_position()
            if i >= nbr_survivors:
                chosen_parent = np.random.choice(nbr_survivors, p=weight_best_fitness)
                self.carsAI[i].neural_net.mutate_model(self.carsAI[chosen_parent].neural_net, self.mutation_rate)

    def gen_background(self):
        self.gen_track_background()

    def display_fitness(self):
        text_fitness = self.font.render("Fitness - Gen {}".format(self.gen_id), True, COLOR_BLUE)
        text_ever = self.font.render("Best Ever: {:.0f}".format(self.best_fitness_ever), True, COLOR_GREEN)
        text_best = self.font.render("Best Gen {:.0f}".format(self.best_actual_fitness), True,
                                     COLOR_GREEN)
        text_mean = self.font.render("Mean Gen {:.0f}".format(self.mean_fitness), True,
                                     COLOR_GREEN)

        self.window.blit(text_fitness, (self.track.im_w, 40))
        self.window.blit(text_ever, (self.track.im_w, 100))
        self.window.blit(text_best, (self.track.im_w, 160))
        self.window.blit(text_mean, (self.track.im_w, 220))

        # if self.best_fitness_list:
        self.refresh_fitness_plot()

    def display_fps(self):
        fps = self.font.render("FPS: " + str(int(self.clock.get_fps())), True, pygame.Color('white'))
        self.window.blit(fps, (self.track.im_w, 700))

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
        self.window.blit(surf, (self.track.im_w - 50, 400))

    def save_best_model(self):
        new_model_name = self.save_folder_model + "Gen_{}_Fitness_{}.h5".format(self.gen_id,
                                                                                int(self.carsAI[0].fitness))

        self.carsAI[0].neural_net.model.save(new_model_name)

    def save_game(self):
        import pickle

        pickle.dump(self, open(self.save_folder_model + '_game.p', "wb"))


def load_game(path_game):
    import pickle

    return pickle.load(open(path_game, "rb"))
