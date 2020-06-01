#!/usr/bin/env python3
"""Moduł rysujący kamienie na planszy"""

__all__ = ["Stone"]

import pygame

from constants import WHITE, BLACK, IMG_WHITE_STONE, IMG_BLACK_STONE

class Stone(pygame.sprite.Sprite):  # pylint: disable=too-few-public-methods
    """Graficzna reprezentacja kamienia na planszy"""
    def __init__(self, color, x, y):  # pylint: disable=invalid-name
        pygame.sprite.Sprite.__init__(self)
        self.x = x  # pylint: disable=invalid-name
        self.y = y  # pylint: disable=invalid-name
        self.color = color
        self.set_image()

    def set_image(self):
        """Narysowanie kamienia na planszy"""
        if self.color == WHITE:
            self.image = pygame.image.load(IMG_WHITE_STONE)
        elif self.color == BLACK:
            self.image = pygame.image.load(IMG_BLACK_STONE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)



if __name__ == "__main__":
    print("You should run gomoku.py file")
