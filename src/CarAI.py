from src.CarHuman import *
from src.NeuralNet import *
import numpy as np


class CarAI(CarHuman):
    def __init__(self, neural_net_path, track, lidar_w, lidar_h):
        CarHuman.__init__(self, track, lidar_w, lidar_h, train=True)
        self.neural_net = NeuralNet(neural_net_path)

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
