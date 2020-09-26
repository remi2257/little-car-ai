from uix.screens.ScreenBaseTrain import *
from src.cars.CarAI import *

matplotlib.use("Agg")


class GameTrainRandomEvolv(ScreenBaseTrain):
    def __init__(self, nn_file_path="raw_models/nn1_dual_layers.net", track_path="track/track1.tra", save=True,
                 fps_max=FPS_MAX_init):

        ScreenBaseTrain.__init__(self, nn_file_path, track_path, save, fps_max)

        if nn_file_path.endswith(".net"):
            self.mutation_rate_best = max_mutation_rate
            self.gen_duration_limit_steps = generation_duration_init_frame
        elif nn_file_path.endswith(".h5"):
            self.mutation_rate_best = copy_mutation_rate
            self.gen_duration_limit_steps = round(generation_duration_max_frame * (1 - copy_mutation_rate) ** 2)
            print("Resuming training")
        else:
            print("NO MODEL")

        self.max_fitness_possible = self.get_max_possible_fitness()

        for i in range(nbr_AI_per_gen):
            self.carsAI.append(CarAI(nn_file_path, self._track, self.lidar_w, self.lidar_h))
            if nn_file_path.endswith(".h5") and i > 0:
                self.carsAI[-1].neural_net.mutate_model(self.mutation_rate_best)

        self.actualize()

    def actualize(self):
        self.clock.tick(self.FPS_MAX)  # Fixe le nbr max de FPS

        # Start new generation if limit of time is reached for the actual generation
        if self.gen_duration >= self.gen_duration_limit_steps:
            self.start_new_gen()
        self.gen_duration += 1

        # BACKGROUND
        self._window.blit(self._background, (0, 0))

        # Make every cars' move
        for carAI in self.carsAI:
            if not carAI.is_alive:
                continue

            # Get Next Move
            carAI.actualize_direction_and_gas(carAI.predict_next_move())

            # Kill car that are bad
            if carAI.fitness < lower_bound_fitness:
                carAI.is_alive = False

            # move_car
            carAI.move_car_and_refresh_LIDAR()

            # refresh fitness
            # carAI.refresh_fitness_v1()
            carAI.refresh_fitness_v2()

        """
        # Get infos on fitness
        list_fitness = [c.fitness for c in self.carsAI if c.is_alive]
        
        # If every cars died
        if not list_fitness: 
            self.gen_duration = self.gen_duration_limit_steps
        """
        # Get infos on fitness
        list_fitness = [c.fitness for c in self.carsAI]

        # Get mean & max
        self.mean_fitness = np.mean(list_fitness)
        self.best_actual_fitness = max(list_fitness)
        # Save Best fitness value
        self.best_fitness_list[-1] = self.best_actual_fitness
        # self.best_fitness_ever = max(self.best_fitness_ever, self.best_actual_fitness)

        # -- DISPLAY--#
        # AI's CARS
        for carAI in self.carsAI:
            if not carAI.is_alive:
                continue
            if carAI.fitness == self.best_actual_fitness:
                carAI.change_to_leader_img()
            elif carAI.is_survivor:
                carAI.change_to_survivor_img()

            self._window.blit(carAI.actual_img, carAI.get_position_left_top())

        # BOTS CAR
        for car in self.cars_bot:
            car.move_car_bot(self._track)
            self._window.blit(car.actual_img, car.get_position_left_top())

        # REFRESH
        self.display_infos_fitness_n_FPS()
        pygame.display.flip()

    def start_new_gen(self):
        # Refresh plot which shows infos on best fitness
        self.refresh_fitness_plot()

        # Sort cars by fitness
        self.carsAI = sorted(self.carsAI, key=lambda x: x.fitness, reverse=True)

        # Save the best model of this generation if the user put save on On
        if self.save:
            self.save_gen_best_model()

        # -- CALCULATE NEW MUTATION RATE --#
        best_fitness = max(1, self.carsAI[0].fitness - self.carsAI[0].bonus_checkpoints)
        ratio_fitness = best_fitness / self.max_fitness_possible
        self.mutation_rate_best = self.get_mutation_rate(best_fitness)
        self.update_duration_limit(ratio_fitness)
        # self.mutation_rate *= decay_mutation_rate

        # Get fitness of survivors
        best_cars_fitness = [max(car.fitness, 1) for car in self.carsAI[0:nbr_survivors]]
        # Use square to increase the gap between lucky survivors & beasts
        best_fitness_square = np.array(best_cars_fitness) ** 2
        weight_best_fitness = best_fitness_square / np.sum(best_fitness_square)

        if self.carsAI[0].fitness > self.best_fitness_ever:
            self.best_fitness_ever = self.carsAI[0].fitness

        # -- APPLY MUTATION --#
        for i, car in enumerate(self.carsAI):
            car.reset_car_ai()
            if i < nbr_survivors or car.is_best_ever:
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

    def display_infos_fitness_n_FPS(self):
        x = self._track.__im_w - round(0.7 * self._track.grid_size)
        ind = 0
        text_fitness = self.font.render("Fitness - Gen {}".format(self.gen_id), True, COLOR_BLUE)
        self._window.blit(text_fitness, (x, self.list_y_text[ind]))
        ind += 2
        text_ever = self.font.render("Best Ever: {:.0f}".format(self.best_fitness_ever), True, COLOR_GREEN)
        self._window.blit(text_ever, (x, self.list_y_text[ind]))
        ind += 1

        text_best = self.font.render("Best Gen {:.0f}".format(self.best_actual_fitness), True,
                                     COLOR_GREEN)
        self._window.blit(text_best, (x, self.list_y_text[ind]))
        ind += 1

        text_mean = self.font.render("Mean Gen {:.0f}".format(self.mean_fitness), True,
                                     COLOR_GREEN)
        self._window.blit(text_mean, (x, self.list_y_text[ind]))
        ind += 1

        text_mutation = self.font.render("Mut. Rate {:.1f}%".format(self.mutation_rate_best * 100), True,
                                         COLOR_GREEN)
        self._window.blit(text_mutation, (x, self.list_y_text[ind]))
        ind += 1

        text_max_fitness = self.font.render("Up Bound Fit. {:.1f}".format(self.max_fitness_possible), True,
                                            COLOR_GREEN)
        self._window.blit(text_max_fitness, (x, self.list_y_text[ind]))
        ind += 1

        limit_frame = self.font.render("Lim. Frames: " + str(self.gen_duration_limit_steps), True,
                                       pygame.Color('white'))
        self._window.blit(limit_frame, (x, self.list_y_text[ind]))
        ind += 2

        fps = self.font.render("FPS (max): {} ({})".format(int(self.clock.get_fps()), self.FPS_MAX), True,
                               pygame.Color('white'))
        self._window.blit(fps, (x, self.list_y_text[ind]))

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
            self.gen_duration_limit_steps = max(int(self.gen_duration_limit_steps / gen_dur_incr_ratio_max),
                                                generation_duration_init_frame)
        elif ratio > 0.35:
            self.gen_duration_limit_steps = min(int(self.gen_duration_limit_steps * gen_dur_incr_ratio_max),
                                                generation_duration_max_frame)

    def get_max_possible_fitness(self):
        lost_fitness = 0
        max_fitness = self.get_forward_speed(max_n_speed) * weight_on_road / FPS_MAX_init

        for n in range(1, min(max_n_speed, self.gen_duration_limit_steps)):
            lost_fitness += max_fitness - self.get_forward_speed(n) / FPS_MAX_init * weight_on_road

        max_sum_fitness = self.gen_duration_limit_steps * max_fitness

        return max_sum_fitness - lost_fitness

    def get_forward_speed(self, n_speed):
        return self._track.speed_max * (1 - math.exp(-n_speed / n0_speed))

    def reset_best_ever(self):
        for carAI in self.carsAI:
            carAI.is_best_ever = False

        self.carsAI[0].is_best_ever = True

def run_train(**kwargs):
    # --- INIT Variable--- #

    stop = False

    if "track_path" in kwargs:
        track_path = kwargs["track_path"]
    else:
        track_path = list_track[0]

    if "model_path" in kwargs:
        model_path = kwargs["model_path"]
    else:
        model_path = "raw_models/nn_tiny.net"

    if "save_train" in kwargs:
        save = kwargs["save_train"]
    else:
        save = True

    # --- INIT Game--- #

    game = GameTrainRandomEvolv(
        nn_file_path=model_path,

        track_path=track_path,

        save=save,

        fps_max=FPS_MAX_max,
    )

    # Boucle infinie
    while not stop:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                stop = True  # On arrête la boucle
            if event.type == pygame_const.KEYDOWN and event.key == pygame_const.K_DOWN:
                game.decrease_FPS()
            if event.type == pygame_const.KEYDOWN and event.key == pygame_const.K_UP:
                game.increase_FPS()

        # Refresh
        game.actualize()

if __name__ == '__main__':
    run_train()
