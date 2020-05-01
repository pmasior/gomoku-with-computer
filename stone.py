#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import pygame

from constants import *

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
    game = Gomoku()
