import os

import pygame

from src.Menu.SelectionPane import *


class SelectionPaneModelTrain(SelectionPane):
    def __init__(self):
        SelectionPane.__init__(self)

        self.x = 640
        self.y = 300
        self.title = "Trained Model ?"

        self.folder = trained_model_path
        self.extension = ".h5"

        self.list_nn = sorted([f for f in os.listdir(self.folder) if f.endswith(self.extension)])
        self.list_nn = [track.split(".")[0] for track in self.list_nn]

        self.list_nn.insert(0, "None")

        self.list_y_text = [self.y + i * self.font_h for i in range(len(self.list_nn))]

    def actualize(self, window, pos=None, is_clicking=False):
        self.mouse_on_id = self.mouse_on_texts(pos)
        if self.mouse_on_id is not None and is_clicking:
            self.chosen_id = self.mouse_on_id

        text = self.font.render(self.title, True, COLOR_BLUE)
        window.blit(text, (self.x, self.y - 1.5 * self.font_h))
        for i, item_name in enumerate(self.list_nn):
            if self.list_y_text[i] - self.y > self.h:
                break
            text = self.font.render(item_name, True, COLOR_BLUE if i != self.mouse_on_id else COLOR_BLUE_LIGHT)
            if i == self.chosen_id:
                rect_pos = tuple([self.x, self.list_y_text[i],
                                  self.font.size(item_name)[0], self.font_h])
                pygame.draw.rect(window, COLOR_ORANGE, rect_pos)

            window.blit(text, (self.x, self.list_y_text[i]))

    def mouse_on_texts(self, pos):
        if pos is None:
            return None
        mouse_x = pos[0]
        mouse_y = pos[1]
        for i, text in enumerate(self.list_nn):
            w = self.font.size(text)[0]
            if self.x <= mouse_x <= self.x + w and self.list_y_text[i] <= mouse_y <= self.list_y_text[i] + self.font_h:
                return i
        return None

    def get_item_path(self):
        if self.list_nn[self.chosen_id] == "None":
            return None
        return self.folder + self.list_nn[self.chosen_id] + self.extension