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
        n, m = self.choose_player_and_move(mouse_x, mouse_y)
        print_board(self.board)
        if self.check_winner(n ,m):
            self.playing = False
            print("END")
        self.change_player()

    def choose_player_and_move(self, mouse_x, mouse_y):
        if self.next_player == 1:
            n, m = self.player1.check_move(mouse_x, mouse_y)
        elif self.next_player == 2:
            n, m = self.player2.check_move(mouse_x, mouse_y)
        if (n != None and m != None):
            return n, m
        return None, None

    def check_winner(self, n, m):
        """ Sprawdza czy wygrana

        Przyjmuje jako argument współrzędne ostatniego ruchu ostatniego gracza,
        następnie dla r równych -4, -3, -2, -1, 0 sprawdza czy wygrana wystąpiła
        w poziomie, pionie lub po któreś z przekątnych

        r pozwala pokryć wszystkie możliwości skrajne i pośrednie przy
        sprawdzaniu wygranej np.: dla sprawdzania w poziomie:
        +++++____ _+++++___ __+++++__ ___+++++_ ____+++++
        gdzie + oznacza kamień jednego gracza,
        a _ puste miejsce lub kamień drugiego gracza
        """
        if n != None and m != None:
            for r in range(-4, 1):
                if self.check_winner_horizontally(n, m, r) or \
                   self.check_winner_vertically(n, m, r) or \
                   self.check_winner_diagonally1(n, m, r) or \
                   self.check_winner_diagonally2(n, m, r):
                    self.winner = self.board[n][m]
                    return self.board[n][m]

    def check_winner_horizontally(self, n, m, r):
        """ Sprawdza czy wygrana w poziomie

        Przyjmuje jako argument współrzędne ostatniego ruchu ostatniego gracza.
        Pomija sprawdzanie pól, które są poza planszą (_ < 0 lub _ > FIELDS),
        potem sprawdza czy w poziomie jest po kolei 5 takich samych kamieni, a
        # jeśli jest więcej niż 5 takich samych kamieni pod rząd to zwraca Fałsz.
        """
        # TODO Zmienić, bo działa dla więcej niż 5 kamieni
        if (n+r) >= 0 and (n+r+4) < FIELDS:
            if self.board[n+r][m] == self.board[n+r+1][m] == \
               self.board[n+r+2][m] == self.board[n+r+3][m] == \
               self.board[n+r+4][m] != None:
                # if (n+r+5) < FIELDS:
                #     if self.board[n+r+5][m] == self.board[n+r][m]:
                #         return False
                return True
        return False

    def check_winner_vertically(self, n, m, r):
        """ Sprawdza czy wygrana w pionie """
        if (m+r) >= 0 and (m+r+4) < FIELDS:
            if self.board[n][m+r] == self.board[n][m+r+1] == \
               self.board[n][m+r+2] == self.board[n][m+r+3] == \
               self.board[n][m+r+4] != None:
                # if (m+r+5) < FIELDS:
                #     if self.board[n][m+r+5] == self.board[n][m+r]:
                #         return False
                return True
        return False

    def check_winner_diagonally1(self, n, m, r):
        """ Sprawdza czy wygrana po przekątnej \ """
        if (n+r) >= 0 and (m+r) >= 0 and (n+r+4) < FIELDS and (m+r+4) < FIELDS:
            if self.board[n+r][m+r] == self.board[n+r+1][m+r+1] == \
               self.board[n+r+2][m+r+2] == self.board[n+r+3][m+r+3] == \
               self.board[n+r+4][m+r+4] != None:
                # if (n+r+5) < FIELDS and (m+r+5) < FIELDS:
                #     if self.board[n+r+5][m+r+5] == self.board[n+r][m+r]:
                #         return False
                return True
        return False

    def check_winner_diagonally2(self, n, m, r):
        """ Sprawdza czy wygrana po przekątnej / """
        if (n-r) < FIELDS and (m+r) >= 0 and (n-(r+4)) >= 0 and (m+r+4) < FIELDS:
            if self.board[n-r][m+r] == self.board[n-(r+1)][m+r+1] == \
               self.board[n-(r+2)][m+r+2] == self.board[n-(r+3)][m+r+3] == \
               self.board[n-(r+4)][m+r+4] != None:
                # if (n-(r+5)) >= 0 and (m+r+5) < FIELDS:
                #     if self.board[n-(r+5)][m+r+5] == self.board[n-r][m+r]:
                #         return False
                return True
        return False

    def change_player(self):
        if self.next_player == 1:
            self.next_player = 2
        elif self.next_player == 2:
            self.next_player = 1

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
