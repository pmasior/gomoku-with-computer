#!/usr/bin/env python3
"""Moduł rysujący kamienie na planszy"""

__all__ = ["Stone"]

import pygame

import constants as c

class Stone(pygame.sprite.Sprite):  # pylint: disable=too-few-public-methods
    """Graficzna reprezentacja kamienia na planszy."""
    def __init__(self, color, x_position, y_position):
        pygame.sprite.Sprite.__init__(self)
        self.x_position = x_position
        self.y_position = y_position
        self.set_image(color)


    def set_image(self, color):
        """Narysowanie kamienia na planszy."""
        if color == c.COMPUTER_STONES_COLOR:
            self.image = pygame.image.load(c.IMG_COMPUTER_STONE)
        elif color == c.HUMAN_STONES_COLOR:
            self.image = pygame.image.load(c.IMG_HUMAN_STONE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_position, self.y_position)



if __name__ == "__main__":
    print("You should run gomoku.py file")
