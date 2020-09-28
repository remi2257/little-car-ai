import random
import yaml
import numpy as np

import tensorflow as tf
from tensorflow.keras.layers import Dense, Input, Conv2D, MaxPool2D, Flatten, Concatenate
from tensorflow.keras.models import Model, load_model

from src.cars.CarCommands import CommandDir, CommandGas
from src.const import height_grid_LIDAR, width_grid_LIDAR

extra_params_dim = 1


def interpret_layer(layer_type, *args):
    if layer_type == "conv":
        nb_filter, kernel_size, strides, padding = args
        return Conv2D(filters=nb_filter, kernel_size=kernel_size,
                      strides=strides, padding=padding,
                      activation='relu')
    elif layer_type == "max_pool":
        pool_size, strides, padding = args
        return MaxPool2D(pool_size=pool_size,
                         strides=strides, padding=padding)
    elif layer_type == "flatten":
        return Flatten()
    elif layer_type == "dense":
        size = args[0]
        return Dense(units=size, activation="relu")


def add_layers_to_model(model, model_architecture_layers):
    for layer_type, *args in model_architecture_layers:
        new_layer = interpret_layer(layer_type, *args)
        model = new_layer(model)
    return model


def model_parser(model_path):
    with open(model_path, "r") as input_file:
        yaml_file = yaml.safe_load(input_file)
    model_architectures = yaml_file["architectures"]
    model_lidar_architecture = model_architectures["lidar_layers"]

    use_conv = any("conv" in layer for layer in model_lidar_architecture)
    if use_conv:
        input_dim_lidar = tuple([height_grid_LIDAR, width_grid_LIDAR, 1])
    else:
        input_dim_lidar = (height_grid_LIDAR * width_grid_LIDAR,)

    lidar_model_input = Input(shape=input_dim_lidar, name='lidar_input')
    lidar_model_output = add_layers_to_model(lidar_model_input, model_lidar_architecture)
    lidar_model = Model(inputs=lidar_model_input, outputs=lidar_model_output)

    extra_params_model_input = Input((extra_params_dim,), name='extra_params_input')
    extra_params_model_output = add_layers_to_model(extra_params_model_input,
                                                    model_architectures["extra_params_layers"])
    extra_params_model = Model(inputs=extra_params_model_input, outputs=extra_params_model_output)

    concat_model_input = Concatenate(name="merge_input")([lidar_model.output, extra_params_model.output])
    concat_model = add_layers_to_model(concat_model_input, model_architectures["concat_layers"])

    output_dir = Dense(len(CommandDir), activation="softmax", name='output_dir')(concat_model)
    output_gas = Dense(len(CommandGas), activation="softmax", name='output_gas')(concat_model)

    model = Model(inputs=[lidar_model.input, extra_params_model.input], outputs=[output_dir, output_gas])

    tf.keras.utils.plot_model(
        model, to_file=model_path.replace('.net', '.png'),
        show_shapes=True, show_layer_names=True,
        rankdir='TB', expand_nested=True, dpi=96
    )
    return model


class NeuralNet:
    def __init__(self, nn_file_path):
        if nn_file_path.endswith(".net"):
            self._model = model_parser(nn_file_path)
        elif nn_file_path.endswith(".h5"):
            self._model = load_model(nn_file_path)

        self._is_cnn = any([isinstance(layer, Conv2D) for layer in self._model.layers])

    def mutate_model_from_query(self, target_nn, mutation_rate, fixed_mutation_rate=False):
        if not fixed_mutation_rate:
            mutation_rate = min(1.0, max(2 * random.random() * mutation_rate, 0.01))
        for j, layer in enumerate(target_nn.model.layers):
            new_weights_for_layer = []

            for weight_array in layer.get_weights():
                save_shape = weight_array.shape
                one_dim_weight = weight_array.reshape(-1)
                if layer.trainable:
                    for i, weight in enumerate(one_dim_weight):
                        if random.random() <= mutation_rate:
                            # one_dim_weight[i] = random.uniform(0, 2) - 1
                            one_dim_weight[i] = random.gauss(0, 0.4)

                new_weight_array = one_dim_weight.reshape(save_shape)
                new_weights_for_layer.append(new_weight_array)

            self._model.layers[j].set_weights(new_weights_for_layer)

    def mutate_model(self, mutation_rate):
        for j, layer in enumerate(self._model.layers):
            new_weights_for_layer = []

            for weight_array in layer.get_weights():
                save_shape = weight_array.shape
                one_dim_weight = weight_array.reshape(-1)

                for i, weight in enumerate(one_dim_weight):
                    if random.random() <= mutation_rate:
                        one_dim_weight[i] = random.uniform(0, 2) - 1

                new_weight_array = one_dim_weight.reshape(save_shape)
                new_weights_for_layer.append(new_weight_array)

            self._model.layers[j].set_weights(new_weights_for_layer)

    def save(self, filepath):
        self._model.save(filepath)

    @property
    def model(self):
        return self._model

    def predict(self, inputs):
        input_lidar, input_extra_params = inputs
        if not self._is_cnn:
            input_lidar_flatten = np.array(input_lidar).flatten()
            input_lidar_formatted = np.expand_dims(input_lidar_flatten, axis=0)
        else:
            input_lidar_3_channels = np.expand_dims(input_lidar, axis=2)
            input_lidar_formatted = np.expand_dims(input_lidar_3_channels, axis=0)

        input_extra_params_formatted = np.expand_dims(input_extra_params, axis=0)
        predictions = self._model.predict([input_lidar_formatted, input_extra_params_formatted])
        pred_dir, pred_gas = predictions
        chosen_dir = list(CommandDir)[np.argmax(pred_dir)]
        chosen_gas = list(CommandGas)[np.argmax(pred_gas)]
        return chosen_dir, chosen_gas

    def test_predict(self, inputs):
        # print(inputs.shape, inputs)
        return self._model.predict(inputs)


if __name__ == '__main__':
    print(list(CommandGas))
    # nn = NeuralNet("raw_models/nn_tiny.net")

    # input_1 = np.expand_dims([0., 1., 1., 0., 0., 0., 1., 1., 0., 0., 0., 1., 1., 0., 0., 0., 1.,
    #                           1., 0., 0., 0., 1., 1., 0., 0., 0., 1., 1., 0., 0., 0., 1., 1., 1., 1.], axis=0)
    # input_2 = np.expand_dims([0.], axis=0)
    # inputs_test = [input_1, input_2]
    # print(nn.test_predict(inputs_test))
    # nn.model.summary()
    #
    # nn2 = NeuralNet("raw_models/nn1_dual_layers.net")
    # nn2.model.summary()
    #
    # nn_cnn = NeuralNet("raw_models/cnn_standard.net")
    # nn_cnn.model.summary()
    # nn2 = NeuralNet("raw_models/nn_tiny.net")

    # nn2.mutate_model_from_query(nn, 0.9)
    # print(nn2.model.summary())
    # print(nn.model.get_weights())
    # print(nn2.model.get_weights())
