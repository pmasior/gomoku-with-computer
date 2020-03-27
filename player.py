#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import pygame
import math

from constants import *

class Player():
    def __init__(self, screen, tie, number, color):
        self.screen = screen
        self.tie = tie
        self.color = color
        self.number = number
        self.stone_sprites = pygame.sprite.Group()

    def update(self):
        pass

    def check_move(self, mouse_x, mouse_y):
        """ Sprawdza czy ruch jest dozwolony, jeśli jest to go wykonuje """
        for m in range(0, FIELDS):
            y = GRID_BEGIN + m * GRID_TILESIZE
            for n in range(0, FIELDS):
                x = GRID_BEGIN + n * GRID_TILESIZE
                if self.check_if_clicked_in_field(x, y, mouse_x, mouse_y) and \
                   self.check_if_field_is_empty(n, m):
                    self.write_move(n, m)
                    self.draw_move(x, y)
                    return True
        return False

    def check_if_clicked_in_field(self, x, y, mouse_x, mouse_y):
        if math.hypot(mouse_x - x, mouse_y - y) < STONE_RADIUS:
            return True
        return False

    def check_if_field_is_empty(self, n, m):
        if self.tie.board[n][m] == None:
            return True
        return False

    def write_move(self, n, m):
        self.tie.board[n][m] = self.number

    def draw_move(self, x, y):
        stone = Stone(self.color, x, y)
        self.tie.all_sprites.add(stone)
        self.stone_sprites.add(stone)


class Stone(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.set_image()

    def set_image(self):
        if self.color == WHITE:
            self.image = pygame.image.load(IMG_WHITE_STONE)
        elif self.color == BLACK:
            self.image = pygame.image.load(IMG_BLACK_STONE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


if __name__ == "__main__":
    print("You should run gomoku.py file")
