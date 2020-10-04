from src.cars.Car import CommandDir, CommandGas
from .ScreenBasePlay import *
from src.const import *
from math import ceil

img_pedals_arrows = {
    CommandGas.ON: im_others_path + "pedals_gas.png",
    CommandGas.BRAKE: im_others_path + "pedals_brake.png",
    CommandGas.OFF: im_others_path + "pedals_off.png",
    CommandDir.LEFT: im_others_path + "arrows_left.png",
    CommandDir.RIGHT: im_others_path + "arrows_right.png",
    CommandDir.NONE: im_others_path + "arrows_off.png",
}

LIDAR_width_img = ceil(big_window_haut / (20 * 8)) * 20
erode_LIDAR_grid = 1 + int(big_window_larg / 1500)
offset_LIDAR_grid_x = 20
offset_LIDAR_grid_y = 20
width_arrows_pedals = round(big_window_haut / 12)
offset_arrows_pedals = round(big_window_haut / 20)


class ScreenPlaySolo(ScreenBasePlay):
    def __init__(self, track_path, **kwargs):
        ScreenBasePlay.__init__(self, track_path=track_path, **kwargs)
        # Todo : Cacul de la taille de l'image un peu chelou
        self._car = None

        # Get infos on LIDAR's image size
        self._lidar_im_w, self._lidar_im_h = self.find_lidar_img_size()
        self._lidar_w_rect = self._lidar_im_w // width_grid_LIDAR
        self._lidar_h_rect = self._lidar_im_h // height_grid_LIDAR
        # Generate Window
        self._window_w = self._track.im_w + self._lidar_im_w + offset_LIDAR_grid_x
        self._window_h = self._track.im_h
        self._window = pygame.display.set_mode((self._window_w, self._window_h))

        # GEN ACTION IMGS (Direction & Pedals)
        self._actions_imgs = {}
        # Actions are an enumeration which ends by wheel_NONE (which then, have the biggest value)
        for command in img_pedals_arrows.keys():
            img = pygame.image.load(img_pedals_arrows[command]).convert_alpha()
            width = img.get_width()
            height = img.get_height()
            ratio = float(width / height)
            img = pygame.transform.scale(img, (width_arrows_pedals, round(width_arrows_pedals / ratio)))

            self._actions_imgs[command] = img

        self.gen_background()

    # -- INIT Functions -- #

    # read global variables to get the size of LIDAR's display
    def find_lidar_img_size(self):
        track_height = self._track.im_h
        ratio = float(height_grid_LIDAR) / width_grid_LIDAR
        if ratio <= 1.0:
            return LIDAR_width_img, round(LIDAR_width_img * ratio)

        else:
            possible_height = ratio * LIDAR_width_img
            if possible_height + offset_LIDAR_grid_y > track_height:
                possible_height = track_height - offset_LIDAR_grid_y

            return round(possible_height / ratio), possible_height

    # Basically, a black rectangle :)
    def gen_lidar_background(self):
        # Generate LIDAR background
        rect_pos = tuple([self._track.im_w, offset_LIDAR_grid_y,
                          self._lidar_im_w, self._lidar_im_h])
        pygame.draw.rect(self._background, (0, 0, 0), rect_pos)

    def gen_background(self):
        super(ScreenPlaySolo, self).gen_background()
        self.gen_lidar_background()  # Draw LIDAR rect

    # -- REFRESH -- #

    def actualize(self, pos=None):
        self._tick_clock()
        # BACKGROUND
        self._window.blit(self._background, (0, 0))

        # Make next move
        self._car.move_car_and_refresh_lidar()
        # Display car on window
        self._window.blit(self._car.actual_img, self._car.get_position_left_top())
        # Display Lidar
        self.refresh_lidar_display()

        # PEDALS & Direction Arrows
        self.refresh_arrow_pedal()

        # Compute Display Fitness
        self._car.refresh_fitness_v2()
        self.display_fitness()

        # REFRESH
        pygame.display.flip()

    def refresh_arrow_pedal(self):
        self.refresh_arrows_pedals(self._car.last_dir_cmd, self._car.last_gas_cmd)

    def refresh_arrows_pedals(self, dir_cmd, gas_cmd):
        self.refresh_arrow(dir_cmd)
        self.refresh_pedals(gas_cmd)

    def refresh_arrow(self, dir_cmd):
        self._window.blit(self._actions_imgs[dir_cmd], (self._window_w - width_arrows_pedals - offset_arrows_pedals,
                                                        self._lidar_im_h + 5 * offset_arrows_pedals))

    def refresh_pedals(self, gas_cmd):
        self._window.blit(self._actions_imgs[gas_cmd], (self._window_w - width_arrows_pedals - offset_arrows_pedals,
                                                        self._lidar_im_h + 6 * offset_arrows_pedals))

    def refresh_lidar_display(self):
        for i in range(height_grid_LIDAR):
            for j in range(width_grid_LIDAR):
                if self._car.lidar_is_practicable(i, j):
                    color = COLOR_GREEN
                else:
                    color = COLOR_RED

                # Print Point & Result
                point_pos = self._car.lidar_get_true_pos(i, j)
                pygame.draw.circle(self._window, color, point_pos, circle_size)

                # Draw rectangle
                rect_pos = tuple([self._track.im_w + j * self._lidar_w_rect + erode_LIDAR_grid,
                                  offset_LIDAR_grid_y + i * self._lidar_h_rect + erode_LIDAR_grid,
                                  self._lidar_w_rect - 2 * erode_LIDAR_grid,
                                  self._lidar_h_rect - 2 * erode_LIDAR_grid])

                pygame.draw.rect(self._window, color, rect_pos)

        point_pos = tuple([round(self._track.im_w + (self._car.lidar_grid_car_x + 0.5) * self._lidar_w_rect),
                           offset_LIDAR_grid_y + round((self._car.lidar_grid_car_y + 0.5) * self._lidar_h_rect)])

        pygame.draw.circle(self._window, COLOR_BLUE, point_pos, 4, 2)

    def display_fitness(self):
        text = self._font.render("Fitness: {:.0f}".format(self._car.fitness), True, COLOR_GREEN)

        self._window.blit(text, (self._window_w - 200,
                                 self._window_h - 100))
