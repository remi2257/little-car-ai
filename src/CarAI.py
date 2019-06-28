from src.CarHuman import *
from src.NeuralNet import *


class CarAI(CarHuman):
    def __init__(self, neural_net_path, track, lidar_w, lidar_h, path_img="images/vehicles/Audi.png"):
        CarHuman.__init__(self, track, lidar_w, lidar_h, path_img)
        self.neural_net = NeuralNet(neural_net_path)
        self.fitness = 0

    def predict_next_move(self):
        inputs = np.append(self.speed, np.array(self.lidar_filtered).reshape((-1))
                           .astype(int)).astype(float)
        # print(inputs.shape,inputs)
        predictions = self.neural_net.model.predict(np.expand_dims(inputs, axis=0))

        return [np.argmax(predictions[0]), np.argmax(predictions[1]) + 3]

    def refresh_fitness(self):
        self.fitness += self.speed
