import numpy as np

from src.objects.LIDAR import LIDAR
from src.objects.NeuralNet import NeuralNet
from src.objects.Track import Track


def test_LIDAR():
    lidar = LIDAR()
    i_test = 0
    j_test = 0
    assert not lidar.is_practicable(i=i_test, j=j_test)

    lidar.refresh_case(i=i_test, j=j_test, road_type="lr", is_practicable=True, true_pos=(40, 20))

    assert lidar.is_practicable(i=i_test, j=j_test)
    assert lidar.get_true_pos(i=i_test, j=j_test) == (40, 20)

    size_lidar = lidar.size
    assert size_lidar[0] * size_lidar[1] > 1

    new_filtered_map = np.random.choice(a=[False, True], size=size_lidar)
    for i in range(size_lidar[0]):
        for j in range(size_lidar[1]):
            lidar.refresh_case(i=i, j=j, road_type="xx", is_practicable=new_filtered_map[i][j], true_pos=(40, 20))

    assert (new_filtered_map == lidar.filtered_mat).all()


def test_NeuralNet():
    nn1 = NeuralNet.from_path("models/raw/cnn_light.net")
    assert nn1
    nn2 = NeuralNet.copy_architecture_n_weights(nn1)

    for weight_layer_1, weight_layer_2 in zip(nn1.get_weights(), nn2.get_weights()):
        comparison = weight_layer_1 == weight_layer_2
        equal_arrays = comparison.all()
        assert equal_arrays


def test_Track():
    track = Track("tracks/tiny.tra")
    assert track
