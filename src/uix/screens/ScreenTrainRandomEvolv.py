import numpy as np
import math
import pygame

from src.const import *

from src.uix.screens.abstract.ScreenBaseTrain import ScreenBaseTrain

nbr_AI_per_gen = 25
rate_survivors = 0.2

nbr_survivors = int(nbr_AI_per_gen * rate_survivors)

weight_on_road = 10
lower_bound_fitness = -1000

boost_checkpoint = 250

max_mutation_rate = 1.0
decay_mutation_rate = 0.95

copy_mutation_rate = 0.08

generation_duration_max_sec = 20
generation_duration_max_frame = generation_duration_max_sec * FPS_MAX_init

generation_duration_init_sec = 1
generation_duration_init_frame = generation_duration_init_sec * FPS_MAX_init

gen_dur_incr_ratio_max = 1.2
generation_duration_incr_sec = 1
generation_duration_incr_frame = generation_duration_incr_sec * FPS_MAX_init


class ScreenTrainRandomEvolv(ScreenBaseTrain):
    def __init__(self, track_path, nn_file_path, save, **kwargs):
        # Import here so that Tensorflow is imported only if needed
        from src.cars.CarAI import CarAI
        from src.objects.NeuralNet import NeuralNet

        ScreenBaseTrain.__init__(self, track_path, nn_file_path, save, **kwargs)

        if nn_file_path.endswith(".net"):
            self._mutation_rate_best = max_mutation_rate
            self._gen_duration_limit_steps = generation_duration_init_frame
        elif nn_file_path.endswith(".h5"):
            self._mutation_rate_best = copy_mutation_rate
            self._gen_duration_limit_steps = round(generation_duration_max_frame * (1 - copy_mutation_rate) ** 2)
            print("Resuming training")
        else:
            raise TypeError("Model should be either .net or .h5")

        self._max_fitness_possible = self.get_max_possible_fitness()

        base_neural_net = NeuralNet.from_path(nn_file_path)
        self._carsAI.append(CarAI(self._track, base_neural_net))

        for i in range(nbr_AI_per_gen - 1):
            if nn_file_path.endswith(".net"):
                new_model = NeuralNet.copy_architecture(base_neural_net)
            else:
                new_model = NeuralNet.copy_architecture_n_weights(base_neural_net)
                new_model.mutate_model(self._mutation_rate_best)
            new_car = CarAI(self._track, new_model)
            self._carsAI.append(new_car)

    def actualize_screen(self, pos=None):
        super(ScreenTrainRandomEvolv, self).actualize_screen(pos)

        # Start new generation if limit of time is reached for the actual generation
        if self._gen_duration >= self._gen_duration_limit_steps:
            self.start_new_gen()
        self._gen_duration += 1

        # Make every cars' move
        for carAI in self._carsAI:
            if not carAI.is_alive:
                continue

            # Get Next Move
            carAI.actualize_direction_and_gas(carAI.predict_next_move())

            # Kill car that are bad
            if carAI.fitness < lower_bound_fitness:
                carAI.kill()

            # move_car
            carAI.move_car_and_refresh_lidar()

            # refresh fitness
            # carAI.refresh_fitness_v1()
            carAI.refresh_fitness_v2()

        # Get infos on fitness
        list_fitness = [c.fitness for c in self._carsAI]

        # Get mean & max
        self._mean_fitness = np.mean(list_fitness)
        self._best_actual_fitness = max(list_fitness)
        # Save Best fitness value
        self._best_fitness_list[-1] = self._best_actual_fitness
        # self.best_fitness_ever = max(self.best_fitness_ever, self.best_actual_fitness)

        # -- DISPLAY--#
        # AI's CARS
        for carAI in self._carsAI:
            if not carAI.is_alive:
                continue
            if carAI.fitness == self._best_actual_fitness:
                carAI.change_to_leader_img()
            elif carAI.is_survivor:
                carAI.change_to_survivor_img()

            self._window.blit(carAI.actual_img, carAI.get_position_left_top())

        # REFRESH
        self.display_infos_fitness_n_fps()

    def start_new_gen(self):
        # Sort cars by fitness
        self._carsAI = sorted(self._carsAI, key=lambda x: x.fitness, reverse=True)

        # Save the best model of this generation if the user put save on On
        if self._save:
            self.save_gen_best_model()

        # -- CALCULATE NEW MUTATION RATE --#
        best_car = self._carsAI[0]
        best_fitness = max(1, best_car.fitness - best_car.bonus_checkpoints)
        ratio_fitness = best_fitness / self._max_fitness_possible
        self._mutation_rate_best = self.get_mutation_rate(best_fitness)
        self.update_duration_limit(ratio_fitness)
        # self.mutation_rate *= decay_mutation_rate

        # Get fitness of survivors
        best_cars_fitness = [max(car.fitness, 1) for car in self._carsAI[0:nbr_survivors]]
        # Use square to increase the gap between lucky survivors & beasts
        best_fitness_square = np.array(best_cars_fitness) ** 2
        weight_best_fitness = best_fitness_square / np.sum(best_fitness_square)

        if best_car.fitness > self._best_fitness_ever:
            self._best_fitness_ever = best_car.fitness

        # -- APPLY MUTATION --#
        for i, car in enumerate(self._carsAI):
            car.reset_car_ai()
            if i < nbr_survivors or car.is_best_ever:
                car._is_survivor = True
            else:
                car._is_survivor = False
                chosen_parent = np.random.choice(nbr_survivors, p=weight_best_fitness)
                car.mutate_neural_network_from_parent(self._carsAI[chosen_parent],
                                                      self._mutation_rate_best)

        # Refresh plot which shows infos on best fitness
        self.refresh_fitness_plot()

        # Incr values
        self._max_fitness_possible = self.get_max_possible_fitness()

        self._best_fitness_list.append(0)
        self._gen_id += 1
        self._gen_duration = 0

    def display_infos_fitness_n_fps(self):
        x = self._track.im_w - round(0.7 * self._track.case_size)
        ind = 0
        text_fitness = self._font.render("Fitness - Gen {}".format(self._gen_id), True, COLOR_BLUE)
        self._window.blit(text_fitness, (x, self._list_y_text[ind]))
        ind += 2
        text_ever = self._font.render("Best Ever: {:.0f}".format(self._best_fitness_ever), True, COLOR_GREEN)
        self._window.blit(text_ever, (x, self._list_y_text[ind]))
        ind += 1

        text_best = self._font.render("Best Gen {:.0f}".format(self._best_actual_fitness), True,
                                      COLOR_GREEN)
        self._window.blit(text_best, (x, self._list_y_text[ind]))
        ind += 1

        text_mean = self._font.render("Mean Gen {:.0f}".format(self._mean_fitness), True,
                                      COLOR_GREEN)
        self._window.blit(text_mean, (x, self._list_y_text[ind]))
        ind += 1

        text_mutation = self._font.render("Mut. Rate {:.1f}%".format(self._mutation_rate_best * 100), True,
                                          COLOR_GREEN)
        self._window.blit(text_mutation, (x, self._list_y_text[ind]))
        ind += 1

        text_max_fitness = self._font.render("Up Bound Fit. {:.1f}".format(self._max_fitness_possible), True,
                                             COLOR_GREEN)
        self._window.blit(text_max_fitness, (x, self._list_y_text[ind]))
        ind += 1

        limit_frame = self._font.render("Lim. Frames: " + str(self._gen_duration_limit_steps), True,
                                        pygame.Color('white'))
        self._window.blit(limit_frame, (x, self._list_y_text[ind]))
        ind += 2

        fps = self._font.render("FPS (max): {} ({})".format(int(self._clock.get_fps()), self._fps_max), True,
                                pygame.Color('white'))
        self._window.blit(fps, (x, self._list_y_text[ind]))

    # New mutation rate which is directly link to the fitness
    def get_mutation_rate(self, fitness):
        fitness = max(fitness, 1)
        if fitness < 3000:
            return min(0.75, max(5.1844 * math.pow(fitness, -0.4584), 0.005))
        else:
            return min(0.75, max(-0.092 * math.log(fitness) + 0.834, 0.005))

    # Update duration limit according to fitness/fitness_PIED_AU_PLANCHER
    def update_duration_limit(self, ratio):
        if ratio < 0.15:
            self._gen_duration_limit_steps = max(int(self._gen_duration_limit_steps / gen_dur_incr_ratio_max),
                                                 generation_duration_init_frame)
        elif ratio > 0.35:
            self._gen_duration_limit_steps = min(int(self._gen_duration_limit_steps * gen_dur_incr_ratio_max),
                                                 generation_duration_max_frame)

    def get_max_possible_fitness(self):
        lost_fitness = 0
        max_fitness = self.get_forward_speed(max_n_speed) * weight_on_road / FPS_MAX_init

        for n in range(1, min(max_n_speed, self._gen_duration_limit_steps)):
            lost_fitness += max_fitness - self.get_forward_speed(n) / FPS_MAX_init * weight_on_road

        max_sum_fitness = self._gen_duration_limit_steps * max_fitness

        return max_sum_fitness - lost_fitness

    def get_forward_speed(self, n_speed):
        return self._track.speed_max * (1 - math.exp(-n_speed / n0_speed))

    def reset_best_ever(self):
        for carAI in self._carsAI:
            carAI._is_best_ever = False

        self._carsAI[0].is_best_ever = True


def run_train(track_path, nn_file_path, save_train, **kwargs):
    screen = ScreenTrainRandomEvolv(track_path=track_path,
                                    nn_file_path=nn_file_path,
                                    save=save_train,
                                    **kwargs)
    screen.run()


if __name__ == '__main__':
    run_train(
        track_path="tracks/tiny.tra",
        nn_file_path="models/raw/cnn_light.net",
        save_train=True,
    )
