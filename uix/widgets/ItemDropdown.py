import os
import pygame
from pygame_gui.elements import UIDropDownMenu, UILabel


class ItemDropdown:
    def __init__(self, rect, manager, folder, extension, text=None):
        self._folder = folder
        self._extension = extension

        self._dropdown = self.generate_dropdown(rect, manager)
        if text is not None:
            self.generate_label(manager, rect, text)

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

    @staticmethod
    def generate_label(manager, rect, text):
        x_center, y_center, w, h = rect
        corrected_w = int(0.7 * w)
        new_y_center = y_center - 3 * h // 2
        label_rect = (x_center - corrected_w // 2, new_y_center,
                         corrected_w, h)
        label_item = UILabel(relative_rect=pygame.Rect(*label_rect), text=text,
                             manager=manager)
        return label_item
