from pygame.font import Font

from src.const import *


class SelectionPane:
    def __init__(self):
        # x: int
        # y: int
        # list_y_text: list
        # title: str
        # folder: str
        # extension: str

        self.w = menu_trackbar_w
        self.h = menu_trackbar_h

        self.chosen_id = 0
        self.mouse_on_id = None

        # Font
        self.font = Font('freesansbold.ttf', 28)
        self.font_h = self.font.get_height()
        self.space_between_line = 30

    def actualize(self, window, pos=None, is_clicking=False):
        raise NotImplementedError

    def mouse_on_texts(self, pos):
        raise NotImplementedError

    def get_item_path(self):
        raise NotImplementedError
