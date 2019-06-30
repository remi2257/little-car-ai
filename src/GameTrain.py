from src.Game import *


class GameTrain(Game):
    def __init__(self, nn_file_path=None, track_path="track/track1.tra"):

        Game.__init__(self, track_path=track_path)

        self.carsAI = []
        self.best_actual_fitness = 0
        self.best_fitness_ever = 0
        self.mean_fitness = 0

        self.mutation_rate = 0.2

        self.gen_id = 1
        self.gen_duration = 0
        self.gen_duration_limit = 150

        for _ in range(nbr_AI_per_gen):
            self.carsAI.append(CarAI(nn_file_path, self.track, self.lidar_w, self.lidar_h))

        self.actualize()

    def actualize(self):
        pygame.time.Clock().tick(FPS_MAX)  # Fixe le nbr max de FPS
        self.gen_duration += 1

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
        self.best_fitness_ever = max(self.best_fitness_ever, self.best_actual_fitness)

        for carAI in self.carsAI:
            if carAI.fitness == self.best_actual_fitness:
                carAI.change_to_leader_img()
            # CAR PLAYER
            carAI.move_car_and_refresh_LIDAR()

            self.window.blit(carAI.actual_img, carAI.get_position_left_top())

        self.display_fitness()

        # BOTS CAR
        for car in self.cars_bot:
            car.move_car_bot(self.track)
            self.window.blit(car.actual_img, car.get_position_left_top())

        # REFRESH
        pygame.display.flip()

    def start_new_gen(self):
        self.gen_id += 1
        self.gen_duration = 0
        self.carsAI = sorted(self.carsAI, key=lambda x: x.fitness, reverse=True)

        for i in range(nbr_AI_per_gen):
            self.carsAI[i].reset_position()
            if i >= nbr_survivors:
                chosen_parent = random.randint(0, nbr_survivors)
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
