#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import sys
import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # ukrycie powitania pygame
import pygame
from player import *
from constants import *

class Gomoku():
    def __init__(self):
        pygame.init()
        pygame.mixer.quit()  # avoid error when pygame CPU usage is 100%
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.draw_background()
        self.draw_grid()
        self.tie = Tie(self)
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
            if event.type == pygame.MOUSEBUTTONUP:
                self.events_after_mousebuttonup()

    def update(self):
        self.all_sprites.update()

    def events_after_mousebuttonup(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        self.tie.choose_player_for_move(mouse_x, mouse_y)
        self.tie.print_board()
        if self.tie.check_winner():
            self.show_gameover_screen()

    def show_gameover_screen(self):
        pass

    def draw(self):
        pygame.display.flip()
        self.all_sprites.draw(self.screen)

    def draw_background(self):
        self.screen.fill(SAND)

    def draw_grid(self):
        """ Rysuje pionowe i poziome linie """
        for c in range(GRID_BEGIN, GRID_END, GRID_TILESIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (c, GRID_BEGIN), (c, GRID_END), 2)
            pygame.draw.line(self.screen, DARK_GRAY, (GRID_BEGIN, c), (GRID_END, c), 2)


class Tie():
    def __init__(self, game):
        self.game = game
        self.next_player = 1
        self.board = [[None for n in range(16)] for m in range(16)]
        self.create_players()

    def choose_player_for_move(self, mouse_x, mouse_y):
        if self.next_player == 1:
            if self.player1.check_move(mouse_x, mouse_y):
                self.next_player = 2
        elif self.next_player == 2:
            if self.player2.check_move(mouse_x, mouse_y):
                self.next_player = 1

    def print_board(self):
        for m in range(0, FIELDS):
            for n in range(0, FIELDS):
                if self.board[n][m] != None:
                    print(self.board[n][m], end=' ')
                else:
                    print(" ", end=' ')
            print()

    def check_winner(self):
        for m in range(0, FIELDS - 4):
            for n in range(0, FIELDS - 4):
                if self.check_winner_horizontally(n, m) or \
                   self.check_winner_vertically(n, m) or \
                   self.check_winner_diagonally(n, m):
                    self.game.running = False

    def check_winner_horizontally(self, n, m):
        if self.board[n][m] == self.board[n+1][m] == self.board[n+2][m] == \
           self.board[n+3][m] == self.board[n+4][m] != None:
            return self.board[n][m]
        return False

    def check_winner_vertically(self, n, m):
        if self.board[n][m] == self.board[n][m+1] == self.board[n][m+2] == \
           self.board[n][m+3] == self.board[n][m+4] != None:
            return self.board[n][m]
        return False

    def check_winner_diagonally(self, n, m):
        if self.board[n][m] == self.board[n+1][m+1] == self.board[n+2][m+2] == \
           self.board[n+3][m+3] == self.board[n+4][m+4] != None:
            return self.board[n][m]
        return False

    def create_players(self):
        self.player1 = Player(self.game, self, 1, BLACK)
        self.player2 = Player(self.game, self, 2, WHITE)


if __name__ == "__main__":
    game = Gomoku()
