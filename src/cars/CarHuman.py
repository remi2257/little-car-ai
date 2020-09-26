from src.cars.Car import Car


class CarHuman(Car):
    def __init__(self, track, lidar_w, lidar_h):
        super(CarHuman, self).__init__(track, lidar_w, lidar_h)
