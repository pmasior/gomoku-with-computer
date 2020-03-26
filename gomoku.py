#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import sys
import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # ukrycie powitania pygame
import pygame
from player import *
from constants import *

class Gomoku:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.create_players_with_random_colors()
        self.draw_background()
        self.draw_grid()
        self.run()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                self.player1.check_move(x, y)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        pygame.display.flip()
        self.all_sprites.draw(self.screen)
        pass

    def create_players_with_random_colors(self):
        if random.randint(0, 1):
            color1 = WHITE
            color2 = BLACK
        else:
            color1 = BLACK
            color2 = WHITE
        self.player1 = Player(self, color1)
        self.player2 = Player(self, color2)

    def draw_background(self):
        self.screen.fill(GRAY)

    def draw_grid(self):
        """ Rysuje pionowe i poziome linie """
        for c in range(GRID_BEGIN, GRID_END, GRID_TILESIZE):
            pygame.draw.line(self.screen, BLUE, (c, GRID_BEGIN), (c, GRID_END))
            pygame.draw.line(self.screen, BLUE, (GRID_BEGIN, c), (GRID_END, c))

if __name__ == "__main__":
    game = Gomoku()
