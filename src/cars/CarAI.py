import pygame

from src.const import path_viper, path_car_survivor

from src.cars.Car import Car
from src.objects.NeuralNet import NeuralNet


class CarAI(Car):
    def __init__(self, track, neural_net: NeuralNet):
        super(CarAI, self).__init__(track)
        self._neural_net = neural_net

        # --Use during traning--#
        self._is_alive = True
        self._is_survivor = False
        self._is_best_ever = False

        self._img_leader = pygame.transform.rotate(self._gen_car_img(path_viper), 270.0)
        self._img_survivor = pygame.transform.rotate(self._gen_car_img(path_car_survivor), 270.0)

    def get_inputs(self):
        input_lidar = self._lidar.filtered_mat
        input_extra_params = [self._speed / self._speed_max]
        return input_lidar, input_extra_params

    def predict_next_move(self):
        inputs = self.get_inputs()

        predictions = self._neural_net.predict(inputs)

        return predictions

    def change_to_leader_img(self):
        self._actual_img = pygame.transform.rotate(self._img_leader, self._theta)

    def change_to_survivor_img(self):
        self._actual_img = pygame.transform.rotate(self._img_survivor, self._theta)

    def reset_car_ai(self):
        self.reset_car()
        self._is_alive = True

    def save_neural_network(self, filepath):
        self._neural_net.save(filepath)

    def mutate_neural_network(self, mutation_rate):
        self._neural_net.mutate_model(mutation_rate)

    def mutate_neural_network_from_parent(self, parent, mutation_rate):
        self._neural_net.mutate_model_from_query(target_nn=parent.neural_net,
                                                 mutation_rate=mutation_rate)

    @property
    def is_alive(self):
        return self._is_alive

    @is_alive.setter
    def is_alive(self, value):
        self._is_alive = value

    @property
    def is_best_ever(self):
        return self._is_best_ever

    @is_best_ever.setter
    def is_best_ever(self, value):
        self._is_best_ever = value

    @property
    def is_survivor(self):
        return self._is_survivor

    @is_survivor.setter
    def is_survivor(self, value):
        self._is_survivor = value

    @property
    def neural_net(self):
        return self._neural_net
