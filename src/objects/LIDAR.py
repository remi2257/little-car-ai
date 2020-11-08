import numpy as np
from src.const import width_grid_LIDAR, height_grid_LIDAR


class LIDAR:
    def __init__(self):
        self._road_mat = np.zeros((height_grid_LIDAR, width_grid_LIDAR), dtype=object)
        self._filtered_mat = np.zeros((height_grid_LIDAR, width_grid_LIDAR), dtype=bool)
        self._true_pos_mat = np.zeros((height_grid_LIDAR, width_grid_LIDAR, 2), dtype=int)

    # Todo : Refresh tout d'un coup pour éviter les appels multiples ?
    def refresh_case(self, i, j, road_type, is_practicable, true_pos):
        self._road_mat[i][j] = road_type
        self._filtered_mat[i][j] = is_practicable
        self._true_pos_mat[i][j] = true_pos

    def is_practicable(self, i, j):
        return self._filtered_mat[i, j]

    def get_true_pos(self, i, j):
        return tuple(self._true_pos_mat[i, j])

    @property
    def filtered_mat(self):
        return self._filtered_mat

    @property
    def size(self):
        return self._road_mat.shape
