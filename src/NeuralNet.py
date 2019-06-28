from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Dropout, Flatten, Input


class NeuralNet:
    def __init__(self, nn_file_path="models/nn1.net"):
        self.input_dim = 36
        generate = nn_file_path.endswith(".net")
        if generate:
            self.model = self.gen_nn_model(nn_file_path)
        else:
            self.model = load_model(nn_file_path)

    def gen_nn_model(self, nn_file_path):
        model_struc = []
        softmax_classes = 3
        # input_dim = -1
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

        inp = Input((self.input_dim,), name='main_input')

        neurons, activ_func = model_struc.pop(0)
        model = Dense(neurons, activation=activ_func, name='dense_1')(inp)

        for i, layer in enumerate(model_struc):
            neurons, activ_func = layer
            model = Dense(neurons, activation=activ_func, name="dense_" + str(i + 2))(model)

        out1 = Dense(softmax_classes, activation="softmax", name='output_dir')(model)
        out2 = Dense(softmax_classes, activation="softmax", name='output_gas')(model)

        return Model(inputs=inp, outputs=[out1, out2])

        # neurons, activ_func = model_struc.pop(0)
        # self.model.add(Dense(neurons, input_dim=input_dim,
        #                      activation=activ_func))
        # for neurons, activ_func in model_struc:
        #     self.model.add(Dense(neurons, activation=activ_func))
        #
        # self.model.add(Dense(softmax_classes, activation="softmax"))


if __name__ == '__main__':
    from keras.utils.vis_utils import plot_model

    nn = NeuralNet()

    print(nn.model.summary())
    print(nn.model.get_weights())
    plot_model(nn.model, to_file='models/model_plot.png', show_shapes=True, show_layer_names=True)
