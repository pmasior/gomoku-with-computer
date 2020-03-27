#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import pygame

from constants import *
from player import *
from develop import *

class Tie():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.next_player = 1
        self.board = [[None for n in range(16)] for m in range(16)]
        self.all_sprites = pygame.sprite.Group()
        self.winner = None
        self.create_players()
        self.draw_background()
        self.draw_grid()
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.MOUSEBUTTONUP:
                self.events_after_mousebuttonup()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        pygame.display.flip()
        self.all_sprites.draw(self.screen)

    def events_after_mousebuttonup(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        self.choose_player_for_move(mouse_x, mouse_y)
        print_board(self.board)
        if self.check_winner():
            self.playing = False
            print("END")

    def choose_player_for_move(self, mouse_x, mouse_y):
        if self.next_player == 1:
            if self.player1.check_move(mouse_x, mouse_y):
                self.next_player = 2
        elif self.next_player == 2:
            if self.player2.check_move(mouse_x, mouse_y):
                self.next_player = 1

    def check_winner(self):
        for m in range(0, FIELDS - 4):
            for n in range(0, FIELDS - 4):
                if self.check_winner_horizontally(n, m) or \
                   self.check_winner_vertically(n, m) or \
                   self.check_winner_diagonally(n, m):
                    self.winner = self.board[n][m]
                    return self.board[n][m]

    def check_winner_horizontally(self, n, m):
        if self.board[n][m] == self.board[n+1][m] == self.board[n+2][m] == \
           self.board[n+3][m] == self.board[n+4][m] != None:
            return True
        return False

    def check_winner_vertically(self, n, m):
        if self.board[n][m] == self.board[n][m+1] == self.board[n][m+2] == \
           self.board[n][m+3] == self.board[n][m+4] != None:
            return True
        return False

    def check_winner_diagonally(self, n, m):
        if self.board[n][m] == self.board[n+1][m+1] == self.board[n+2][m+2] == \
           self.board[n+3][m+3] == self.board[n+4][m+4] != None:
            return True
        return False

    def draw_background(self):
        self.screen.fill(SAND)

    def draw_grid(self):
        """ Rysuje pionowe i poziome linie """
        for c in range(GRID_BEGIN, GRID_END, GRID_TILESIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (c, GRID_BEGIN), (c, GRID_END), 2)
            # pygame.gfxdraw.line(self.screen, c, GRID_BEGIN, c, GRID_END, DARK_GRAY)
            pygame.draw.line(self.screen, DARK_GRAY, (GRID_BEGIN, c), (GRID_END, c), 2)
            # pygame.gfxdraw.line(self.screen, GRID_BEGIN, c, GRID_END, c, DARK_GRAY)

    def create_players(self):
        self.player1 = Player(self.screen, self, 1, BLACK)
        self.player2 = Player(self.screen, self, 2, WHITE)


if __name__ == "__main__":
    print("You should run gomoku.py file")
