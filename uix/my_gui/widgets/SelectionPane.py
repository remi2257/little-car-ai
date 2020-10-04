import pygame
from pygame.font import Font

from src.const import *
from uix.my_gui.widgets import Widget

"""
List on which you can click to select one element
"""


class SelectionPane(Widget):
    def __init__(self, x, y, title, folder, extension):
        super(SelectionPane, self).__init__()
        self._x = x
        self._y = y
        self._w = menu_selection_w
        self._h = menu_selection_h

        self._title = title

        self._folder = folder
        self._extension = extension

        # Font
        self._font = Font('freesansbold.ttf', int(font_size_global * 1.3))
        self._font_h = self._font.get_height()

        # Items
        self._items = self.find_items()
        self._list_y_text = self.generate_list_y_text()

        self._chosen_id = 0
        self._mouse_on_id = None

    def actualize(self, window, pos=None, is_clicking=False):
        self._mouse_on_id = self.mouse_on_text(pos)
        if self._mouse_on_id is not None and is_clicking:
            self._chosen_id = self._mouse_on_id

        text = self._font.render(self._title, True, COLOR_BLUE)
        window.blit(text, (self._x, self._y - 1.5 * self._font_h))
        for i, item_name in enumerate(self._items):
            if self._list_y_text[i] - self._y > self._h:
                break
            text = self._font.render(item_name, True, COLOR_BLUE if i != self._mouse_on_id else COLOR_BLUE_LIGHT)
            if i == self._chosen_id:
                rect_pos = tuple([self._x, self._list_y_text[i],
                                  self._font.size(item_name)[0], self._font_h])
                pygame.draw.rect(window, COLOR_ORANGE, rect_pos)

            window.blit(text, (self._x, self._list_y_text[i]))

    def mouse_on_text(self, pos):
        if pos is None:
            return None
        mouse_x = pos[0]
        mouse_y = pos[1]
        for i, text in enumerate(self._items):
            w = self._font.size(text)[0]
            if self._x <= mouse_x <= self._x + w and \
                    self._list_y_text[i] <= mouse_y <= self._list_y_text[i] + self._font_h:
                return i
        return None

    def get_chosen_item_path(self):
        return os.path.join(self._folder, self._items[self._chosen_id] + self._extension)

    def find_items(self):
        items = sorted([f for f in os.listdir(self._folder) if f.endswith(self._extension)])
        return [track.split(".")[0] for track in items]

    def add_item(self, new_item):
        self._items.append(new_item)
        self._list_y_text = self.generate_list_y_text()

    def generate_list_y_text(self):
        return [self._y + i * self._font_h for i in range(len(self._items))]
