import numpy as np
import pygame

from src.const import path_viper, path_car_survivor

from src.cars.Car import Car
from src.objects.NeuralNet import NeuralNet


class CarAI(Car):
    def __init__(self, neural_net_path, track):
        super(CarAI, self).__init__(track)
        # Import neural net
        self.neural_net = NeuralNet(neural_net_path)
        if self.neural_net.is_cnn:
            self.get_inputs_function = self.get_inputs_cnn
        else:
            self.get_inputs_function = self.get_inputs_nn
            # self.get_inputs_function = self.get_inputs_v1

        # --Use during traning--#
        self.is_alive = True
        self.is_survivor = False
        self.is_best_ever = False

        self.img_leader = pygame.transform.rotate(self._gen_car_img(path_viper), 270.0)
        self.img_survivor = pygame.transform.rotate(self._gen_car_img(path_car_survivor), 270.0)

    def get_inputs_v1(self):
        # inputs = np.append(self.speed / self.speed_max,np.array(self.lidar_filtered).reshape((-1))
        inputs = np.append(self._speed, np.array(self.lidar_filtered).reshape((-1))
                           .astype(int)).astype(float)
        return np.expand_dims(inputs, axis=0)

    def get_inputs_nn(self):
        inputs = np.append(np.array(self.lidar_filtered).reshape((-1))
                           .astype(int), self._speed / self._speed_max).astype(float)
        return np.expand_dims(inputs, axis=0)

    def get_inputs_cnn(self):
        # return [np.expand_dims(np.array(self.lidar_filtered).astype(float), axis=0),
        #         np.array([self.speed / self.speed_max])]
        return [np.array([np.expand_dims(self.lidar_filtered, axis=2)]).astype(float),
                np.array([self._speed / self._speed_max])]

    def predict_next_move(self):
        inputs = self.get_inputs_function()
        # print(inputs.shape,inputs)
        predictions = self.neural_net.model.predict(inputs)

        return [np.argmax(predictions[0]), np.argmax(predictions[1]) + 3]

    def change_to_leader_img(self):
        self.actual_img = pygame.transform.rotate(self.img_leader, self._theta)

    def change_to_survivor_img(self):
        self.actual_img = pygame.transform.rotate(self.img_survivor, self._theta)

    def reset_car_ai(self):
        self.reset_car()
        self.is_alive = True
