from src.objects.Track import Track

from src.usesful_func import start_pygame_headless

start_pygame_headless()
track = Track("tracks/tiny.tra")


def test_car_human():
    from src.cars.CarHuman import CarHuman


    car = CarHuman(track)
    assert car


def test_car_ai():
    from src.cars.CarAI import CarAI
    from src.objects.NeuralNet import NeuralNet

    nn = NeuralNet.from_path("models/raw/cnn_light.net")

    car = CarAI(track=track, neural_net=nn)
    assert car
