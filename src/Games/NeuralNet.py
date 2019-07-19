import random

from keras.layers import Dense, Input
from keras.models import Model, load_model

from src.const import *


class NeuralNet:
    def __init__(self, nn_file_path=None):
        if nn_file_path is None:
            self.model = None
        elif nn_file_path.endswith(".net"):
            self.model = self.gen_nn_model(nn_file_path)
        elif nn_file_path.endswith(".h5"):
            self.model = load_model(nn_file_path)

    def gen_nn_model(self, nn_file_path):
        model_struc = []
        softmax_classes = 3
        input_dim = height_LIDAR * width_LIDAR + 1
        with open(nn_file_path) as f:
            lines_raw = f.readlines()
            lines = [line.strip() for line in lines_raw if line != "\n"]

        for line in lines:
            if line[0].startswith("#"):
                continue
            if line[0].startswith("["):
                continue

            line = line.split(" ")
            # if line[0] == "input_dim":
            #     input_dim = int(line[-1])
            if line[0] == "neurons":
                model_struc.append([int(line[-1])])
            if line[0] == "activation":
                model_struc[-1].append(line[-1].lower())
            if line[0] == "classes":
                softmax_classes = int(line[-1])

        inp = Input((input_dim,), name='main_input')

        neurons, activ_func = model_struc.pop(0)
        model = Dense(neurons, activation=activ_func, name='dense_1')(inp)

        for i, layer in enumerate(model_struc):
            neurons, activ_func = layer
            model = Dense(neurons, activation=activ_func, name="dense_" + str(i + 2))(model)

        out1 = Dense(softmax_classes, activation="softmax", name='output_dir')(model)
        out2 = Dense(softmax_classes, activation="softmax", name='output_gas')(model)

        return Model(inputs=inp, outputs=[out1, out2])

    def mutate_model_from_query(self, target_nn, mutate_rate, fixed_mutate_rate=False):
        if not fixed_mutate_rate:
            mutate_rate = min(1.0, max(2 * random.random() * mutate_rate, 0.01))
        for j, layer in enumerate(target_nn.model.layers):
            new_weights_for_layer = []

            for weight_array in layer.get_weights():
                save_shape = weight_array.shape
                one_dim_weight = weight_array.reshape(-1)

                for i, weight in enumerate(one_dim_weight):
                    if random.random() <= mutate_rate:
                        # one_dim_weight[i] = random.uniform(0, 2) - 1
                        one_dim_weight[i] = random.gauss(0, 0.4)

                new_weight_array = one_dim_weight.reshape(save_shape)
                new_weights_for_layer.append(new_weight_array)

            self.model.layers[j].set_weights(new_weights_for_layer)

    def mutate_model(self, mutate_rate):
        for j, layer in enumerate(self.model.layers):
            new_weights_for_layer = []

            for weight_array in layer.get_weights():
                save_shape = weight_array.shape
                one_dim_weight = weight_array.reshape(-1)

                for i, weight in enumerate(one_dim_weight):
                    if random.random() <= mutate_rate:
                        one_dim_weight[i] = random.uniform(0, 2) - 1

                new_weight_array = one_dim_weight.reshape(save_shape)
                new_weights_for_layer.append(new_weight_array)

            self.model.layers[j].set_weights(new_weights_for_layer)


if __name__ == '__main__':
    nn = NeuralNet("raw_models/nn_tiny.net")

    nn2 = NeuralNet("raw_models/nn_tiny.net")
    nn2.mutate_model_from_query(nn, 0.9)
    # print(nn.model.summary())
    print(nn.model.get_weights())
    print(nn2.model.get_weights())

    # plot_model(nn.model, to_file='raw_models/model_plot.png', show_shapes=True, show_layer_names=True)
