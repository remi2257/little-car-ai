import os
import pygame
from pygame_gui.elements import UIButton, UIDropDownMenu


class ItemDropdown:
    def __init__(self, rect, manager, folder, extension):
        self._folder = folder
        self._extension = extension  # def get_chosen_item_path(self):
        self._dropdown = self.generate_dropdown(rect, manager)

    def generate_dropdown(self, rect, manager):
        x_center, y_center, w, h = rect
        centered_rect = (x_center - w // 2, y_center - h // 2, w, h)
        items = self.find_items()
        dropdown = UIDropDownMenu(items, items[0], relative_rect=pygame.Rect(*centered_rect),
                                  manager=manager, expansion_height_limit=200)
        return dropdown

    def find_items(self):
        items = sorted([f for f in os.listdir(self._folder) if f.endswith(self._extension)])
        return [track.split(".")[0] for track in items]

    def get_item(self):
        return os.path.join(self._folder, self.raw_item + self._extension)

    @property
    def raw_item(self):
        return self._dropdown.selected_option
