import numpy as np
from src.const import width_grid_LIDAR, height_grid_LIDAR


class LIDAR:
    def __init__(self):
        self.mat = np.zeros((height_grid_LIDAR, width_grid_LIDAR), dtype=object)
        self.filtered = np.zeros((height_grid_LIDAR, width_grid_LIDAR), dtype=bool)
        self.true_pos = np.zeros((height_grid_LIDAR, width_grid_LIDAR, 2), dtype=int)

    def is_practicable(self, i, j):
        return self.filtered[i, j]

    def get_true_pos(self, i, j):
        return tuple(self.true_pos[i, j])
