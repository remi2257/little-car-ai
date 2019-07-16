from src.GamePlay import *

from datetime import datetime
import os

import matplotlib
from matplotlib.ticker import MaxNLocator
import matplotlib.backends.backend_agg as agg
import pylab
import matplotlib.pyplot as plt

matplotlib.use("Agg")


class GameTrain(GamePlay):
    def __init__(self, nn_file_path="models/nn1.net", track_path="track/track1.tra", save=True, fps_max=FPS_MAX_init):
        self.save = save
        if self.save:
            self.save_folder_model = path_train_save + datetime.now().strftime("%d_%m__%H_%M_%S") + "/"
            if not os.path.exists(self.save_folder_model):
                os.makedirs(self.save_folder_model)

        GamePlay.__init__(self, track_path=track_path, fps_max=fps_max)

        self.carsAI = []
        self.best_actual_fitness = 0
        self.mean_fitness = 0
        self.best_fitness_list = [0]
        self.best_fitness_ever = 0

        self.gen_id = 1
        self.gen_duration = 0

        if nn_file_path.endswith(".net"):
            self.mutation_rate_best = max_mutation_rate
            self.gen_duration_limit_frame = generation_duration_init_frame
        elif nn_file_path.endswith(".h5"):
            self.mutation_rate_best = copy_mutation_rate
            self.gen_duration_limit_frame = round(generation_duration_max_frame * (1 - copy_mutation_rate)**2)

        else:
            print("NO MODEL")

        self.max_fitness_possible = self.get_max_possible_fitness()

        for i in range(nbr_AI_per_gen):
            self.carsAI.append(CarAI(nn_file_path, self.track, self.lidar_w, self.lidar_h))
            if nn_file_path.endswith(".h5") and i > 0:
                self.carsAI[-1].neural_net.mutate_model(self.mutation_rate_best)

        self.fig = pylab.figure(figsize=[4, 4],  # Inches
                                dpi=50,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                                )
        self.fig_ax = self.fig.gca()

        self.clock = pygame.time.Clock()

        self.actualize()

    def actualize(self):
        self.clock.tick(self.FPS_MAX)  # Fixe le nbr max de FPS
        if self.gen_duration >= self.gen_duration_limit_frame:
            self.start_new_gen()
        self.gen_duration += 1

        # BACKGROUND
        self.window.blit(self.background, (0, 0))

        for carAI in self.carsAI:
            if not carAI.is_alive:
                continue

            # Get Next Move
            carAI.actualize_direction_and_gas(carAI.predict_next_move())
            if carAI.fitness < lower_bound_fitness:
                carAI.is_alive = False

            # move_car
            carAI.move_car_and_refresh_LIDAR()

            # refresh fitness
            carAI.refresh_fitness()

        list_fitness = [c.fitness for c in self.carsAI if c.is_alive]
        if not list_fitness:
            self.gen_duration = self.gen_duration_limit_frame

        self.mean_fitness = np.mean(list_fitness)
        self.best_actual_fitness = max(list_fitness)
        self.best_fitness_list[-1] = self.best_actual_fitness
        self.best_fitness_ever = max(self.best_fitness_ever, self.best_actual_fitness)

        # -- DISPLAY--#
        # CAR PLAYER
        for carAI in self.carsAI:
            if not carAI.is_alive:
                continue
            if carAI.fitness == self.best_actual_fitness:
                carAI.change_to_leader_img()
            elif carAI.is_survivor:
                carAI.change_to_survivor_img()

            self.window.blit(carAI.actual_img, carAI.get_position_left_top())

        # BOTS CAR
        for car in self.cars_bot:
            car.move_car_bot(self.track)
            self.window.blit(car.actual_img, car.get_position_left_top())

        # REFRESH
        self.display_fitness()
        self.display_infos_frame()
        pygame.display.flip()

    def start_new_gen(self):
        self.refresh_fitness_plot()

        self.carsAI = sorted(self.carsAI, key=lambda x: x.fitness, reverse=True)
        if self.save:
            self.save_best_model()

        best_cars_fitness = [max(car.fitness, 1) for car in self.carsAI[0:nbr_survivors]]
        best_fitness_square = np.array(best_cars_fitness) ** 2
        weight_best_fitness = best_fitness_square / np.sum(best_fitness_square)

        # self.mutation_rate *= decay_mutation_rate
        ratio_fitness = max(0, self.carsAI[0].fitness) / self.max_fitness_possible
        self.mutation_rate_best = self.get_mutation_rate(self.carsAI[0].fitness)
        self.update_duration_limit(ratio_fitness)

        for i, car in enumerate(self.carsAI):
            car.reset_car_ai()
            if i < nbr_survivors:
                car.is_survivor = True
            else:
                car.is_survivor = False
                chosen_parent = np.random.choice(nbr_survivors, p=weight_best_fitness)
                car.neural_net.mutate_model_from_query(self.carsAI[chosen_parent].neural_net,
                                                       self.mutation_rate_best)
        # Incr values

        self.max_fitness_possible = self.get_max_possible_fitness()

        self.best_fitness_list.append(0)
        self.gen_id += 1
        self.gen_duration = 0

    def gen_background(self):
        self.gen_track_background()

    def display_fitness(self):
        text_fitness = self.font.render("Fitness - Gen {}".format(self.gen_id), True, COLOR_BLUE)
        self.window.blit(text_fitness, (self.track.im_w - 50, 40))
        text_ever = self.font.render("Best Ever: {:.0f}".format(self.best_fitness_ever), True, COLOR_GREEN)
        self.window.blit(text_ever, (self.track.im_w - 50, 100))
        text_best = self.font.render("Best Gen {:.0f}".format(self.best_actual_fitness), True,
                                     COLOR_GREEN)
        self.window.blit(text_best, (self.track.im_w - 50, 160))
        text_mean = self.font.render("Mean Gen {:.0f}".format(self.mean_fitness), True,
                                     COLOR_GREEN)
        self.window.blit(text_mean, (self.track.im_w - 50, 220))
        text_mutation = self.font.render("Mut. Rate {:.1f}%".format(self.mutation_rate_best * 100), True,
                                         COLOR_GREEN)
        self.window.blit(text_mutation, (self.track.im_w - 50, 280))
        text_max_fitness = self.font.render("Up Bound Fit. {:.1f}".format(self.max_fitness_possible), True,
                                            COLOR_GREEN)
        self.window.blit(text_max_fitness, (self.track.im_w - 50, 340))

    def display_infos_frame(self):
        fps = self.font.render("FPS (max): {} ({})".format(int(self.clock.get_fps()), self.FPS_MAX), True,
                               pygame.Color('white'))
        self.window.blit(fps, (self.track.im_w - 50, 700))
        limit_frame = self.font.render("Lim. Frames: " + str(self.gen_duration_limit_frame), True,
                                       pygame.Color('white'))
        self.window.blit(limit_frame, (self.track.im_w - 50, 750))

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
        self.background.blit(surf, (self.track.im_w - 50, 400))

    def save_best_model(self):
        new_model_name = self.save_folder_model + "Gen_{}_Fitness_{}.h5".format(self.gen_id,
                                                                                int(self.carsAI[0].fitness))

        self.carsAI[0].neural_net.model.save(new_model_name)

    def save_game(self):
        import pickle

        pickle.dump(self, open(self.save_folder_model + '_game.p', "wb"))

    def get_mutation_rate(self, fitness):
        if fitness < 3000:
            return min(0.75, max(5.1844 * math.pow(fitness, -0.4584), 0.005))
        else:
            return min(0.75, max(-0.092 * math.log(fitness) + 0.834, 0.005))

    def update_duration_limit(self, ratio):
        if ratio < 0.2:
            self.gen_duration_limit_frame = max(int(self.gen_duration_limit_frame / gen_dur_incr_ratio_max),
                                                generation_duration_init_frame)
        elif ratio > 0.45:
            self.gen_duration_limit_frame = min(int(self.gen_duration_limit_frame * gen_dur_incr_ratio_max),
                                                generation_duration_max_frame)

    def get_max_possible_fitness(self):
        lost_fitness = 0
        max_fitness = get_forward_speed(max_n_speed) * weight_on_road / FPS_MAX_init

        for n in range(1, min(max_n_speed, self.gen_duration_limit_frame)):
            lost_fitness += max_fitness - get_forward_speed(n) / FPS_MAX_init * weight_on_road

        max_sum_fitness = self.gen_duration_limit_frame * max_fitness

        return max_sum_fitness - lost_fitness

    def increase_FPS(self):
        self.FPS_MAX += 10

    def decrease_FPS(self):
        self.FPS_MAX = max(FPS_MAX_init, self.FPS_MAX - 10)


def load_game(path_game):
    import pickle

    return pickle.load(open(path_game, "rb"))
