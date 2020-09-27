import numpy as np
import pygame

from src.const import path_viper, path_car_survivor

from src.cars.Car import Car
from src.objects.NeuralNet import NeuralNet


class CarAI(Car):
    def __init__(self, neural_net_path, track):
        super(CarAI, self).__init__(track)
        # Import neural net
        self._neural_net = NeuralNet(neural_net_path)
        if self._neural_net.is_cnn:
            self.get_inputs_function = self.get_inputs_cnn
        else:
            self.get_inputs_function = self.get_inputs_nn
            # self.get_inputs_function = self.get_inputs_v1

        # --Use during traning--#
        self._is_alive = True
        self._is_survivor = False
        self._is_best_ever = False

        self._img_leader = pygame.transform.rotate(self._gen_car_img(path_viper), 270.0)
        self._img_survivor = pygame.transform.rotate(self._gen_car_img(path_car_survivor), 270.0)

    def get_inputs_v1(self):
        # inputs = np.append(self.speed / self.speed_max,np.array(self.lidar_filtered).reshape((-1))
        inputs = np.append(self._speed, np.array(self._lidar.filtered_mat).reshape((-1))
                           .astype(int)).astype(float)
        return np.expand_dims(inputs, axis=0)

    def get_inputs_nn(self):
        inputs = np.append(np.array(self._lidar.filtered_mat).reshape((-1))
                           .astype(int), self._speed / self._speed_max).astype(float)
        return np.expand_dims(inputs, axis=0)

    def get_inputs_cnn(self):
        # return [np.expand_dims(np.array(self.lidar_filtered).astype(float), axis=0),
        #         np.array([self.speed / self.speed_max])]
        return [np.array([np.expand_dims(self._lidar.filtered_mat, axis=2)]).astype(float),
                np.array([self._speed / self._speed_max])]

    def predict_next_move(self):
        inputs = self.get_inputs_function()
        # print(inputs.shape,inputs)
        predictions = self._neural_net.predict(inputs)

        return [np.argmax(predictions[0]), np.argmax(predictions[1]) + 3]

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
        self._neural_net.mutate_model_from_query(target_nn=parent.neural_network,
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
