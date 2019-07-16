from src.const import *
import pygame
import numpy as np


class GameMenu:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Little Car AI")

        # Generate Window
        self.window_w = size_haut
        self.window_h = size_haut

        self.x_rect = self.window_w // 2 - menu_rect_w // 2

        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        self.buttons_pos = [self.get_rect_menu_pos(i) for i in range(4)]

        self.button_overlap_ind = None

        # Generate Background
        self.background = pygame.image.load(background_path).convert()

        self.gen_menu_background()

        # Mouse infos
        self.is_holding = False
        self.is_ready_select = False

        self.actualize()

    def actualize(self, pos=None):
        self.window.blit(self.background, (0, 0))
        self.button_overlap_ind = self.mouse_on_button(pos)
        if self.button_overlap_ind is not None:
            if self.is_holding:
                self.is_ready_select = True
                pygame.draw.rect(self.window, COLORS_BRIGHT[self.button_overlap_ind],
                                 self.buttons_pos[self.button_overlap_ind])

            else:
                pygame.draw.rect(self.window, COLORS_LIGHT[self.button_overlap_ind],
                                 self.buttons_pos[self.button_overlap_ind])
            self.button_overlap_ind +=1
        else:
            self.is_ready_select = False

        pygame.display.flip()

    def gen_menu_background(self):
        pygame.draw.rect(self.background, COLOR_GREEN, self.buttons_pos[0])

        pygame.draw.rect(self.background, COLOR_RED, self.buttons_pos[1])

        pygame.draw.rect(self.background, COLOR_BLUE, self.buttons_pos[2])

        pygame.draw.rect(self.background, COLOR_GREEN, self.buttons_pos[3])

    def get_rect_menu_pos(self, rect_id):
        if rect_id == 0:
            y = first_rect_y
        elif rect_id == 1:
            y = second_rect_y
        elif rect_id == 2:
            y = third_rect_y
        else:
            y = forth_rect_y

        return tuple([self.x_rect, y,
                      menu_rect_w, menu_rect_h])

    def mouse_on_button(self, pos):
        if pos is None:
            return None
        mouse_x = pos[0]
        mouse_y = pos[1]
        for i, button_pos in enumerate(self.buttons_pos):
            x, y, w, h = button_pos
            if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                return i
        return None

    def action_selected(self):
        return self.button_overlap_ind
