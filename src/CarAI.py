import numpy as np

from src.CarHuman import *
from src.NeuralNet import *


class CarAI(CarHuman):
    def __init__(self, neural_net_path, track, lidar_w, lidar_h):
        CarHuman.__init__(self, track, lidar_w, lidar_h)
        self.neural_net = NeuralNet(neural_net_path)
        self.is_alive = True
        self.is_survivor = False

        self.img_leader = pygame.transform.rotate(gen_car_img(track, path_viper), 270.0)
        self.img_survivor = pygame.transform.rotate(gen_car_img(track, path_car_survivor), 270.0)

    def get_inputs(self):
        return np.append(self.speed, np.array(self.lidar_filtered).reshape((-1))
                         .astype(int)).astype(float)

    def predict_next_move(self):
        inputs = self.get_inputs()
        # print(inputs.shape,inputs)
        predictions = self.neural_net.model.predict(np.expand_dims(inputs, axis=0))

        return [np.argmax(predictions[0]), np.argmax(predictions[1]) + 3]

    def change_to_leader_img(self):
        self.actual_img = pygame.transform.rotate(self.img_leader, self.theta)

    def change_to_survivor_img(self):
        self.actual_img = pygame.transform.rotate(self.img_survivor, self.theta)

    def reset_car_ai(self):
        self.reset_car()
        self.is_alive = True
