#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import pygame
import math
from constants import *

class Player():
    def __init__(self, game, color):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.color = color
        self.stone_sprites = pygame.sprite.Group()

    def update(self):
        pass

    def move(self, mouse_x, mouse_y):
        x, y = self.check_move(mouse_x, mouse_y)
        if (x != None and y != None):
            # print(x, y)
            self.create_stone(x, y)

    def check_move(self, mouse_x, mouse_y):
        """ Sprawdza czy kliknięto w miejsce, gdzie można ustawić kamień """
        for x in range(GRID_BEGIN, GRID_END, GRID_TILESIZE):
            for y in range(GRID_BEGIN, GRID_END, GRID_TILESIZE):
                if math.hypot(mouse_x - x, mouse_y - y) < STONE_RADIUS:
                    return (x, y)
        return (None, None)

    def create_stone(self, x, y):
        # pygame.draw.circle(self.game.screen, self.color, (x, y), STONE_RADIUS)
        stone = Stone(self.color, x, y)
        self.game.all_sprites.add(stone)
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
