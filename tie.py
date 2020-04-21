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
        self.board = [[None for n in range(FIELDS)] for m in range(FIELDS)]
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
        if n != None and m != None:
            # print_board(self.board)
            self.end_if_gameover(n, m)
            self.change_player()

    def choose_player_and_move(self, mouse_x, mouse_y):
        if self.next_player == 1:
            n, m = self.player1.move(mouse_x, mouse_y)
        elif self.next_player == 2:
            n, m = self.player2.move(mouse_x, mouse_y)
        return n, m

    def end_if_gameover(self, n, m):
        if self.check_winner(n ,m) or self.check_draw():
            self.playing = False

    def check_winner(self, n, m):
        """ Sprawdza czy koniec gry (wygrana lub remis)

        Przyjmuje jako argument współrzędne ostatniego ruchu ostatniego gracza
        (różne niż None), następnie dla r równych -2, -1, 0, 1, 2 sprawdza czy
        wygrana wystąpiła w poziomie, pionie lub po któreś z przekątnych

        zmienna out_extent pozwala pokryć wszystkie możliwości skrajne i
        pośrednie przy sprawdzaniu wygranej np.: dla sprawdzania w poziomie:
        +++++____  _+++++___  __+++++__  ___+++++_  ____+++++
        gdzie + oznacza kamień jednego gracza,
        a _ puste miejsce lub kamień drugiego gracza
        """
        for out_extent in range(-2, 3):
            if self.check_winner_horizontally(n, m, out_extent) or \
               self.check_winner_vertically(n, m, out_extent) or \
               self.check_winner_diagonally1(n, m, out_extent) or \
               self.check_winner_diagonally2(n, m, out_extent):
                self.winner = self.board[n][m]
                return True

    def check_winner_horizontally(self, n, m, out_extent):
        """ Sprawdza czy wygrana w poziomie

        Przyjmuje jako argument współrzędne ostatniego ruchu ostatniego gracza.
        Pomija sprawdzanie pól, które są poza planszą (_ < 0 lub _ >= FIELDS).
        Sprawdza czy (w linii złożonej z 5 kamieni) poprzedni i następny kamień
        nie są tego samego gracza. Potem sprawdza czy w poziomie jest dokładnie
        5 takich samych kamieni.
        """
        left = n - 2 + out_extent
        right = n + 2 + out_extent
        if left - 1 >= 0:
            if self.board[left - 1][m] == self.next_player:
                return False
        if right + 1 < FIELDS:
            if self.board[right + 1][m] == self.next_player:
                return False
        if left >= 0 and right < FIELDS:
            if self.board[left][m] == \
               self.board[left+1][m] == \
               self.board[left+2][m] == \
               self.board[left+3][m] == \
               self.board[right][m] == \
               self.next_player:
                return True
        return False

    def check_winner_vertically(self, n, m, out_extent):
        """ Sprawdza czy wygrana w pionie """
        top = m - 2 + out_extent
        down = m + 2 + out_extent
        if top - 1 >= 0:
            if self.board[n][top - 1] == self.next_player:
                return False
        if down + 1 < FIELDS:
            if self.board[n][down + 1] == self.next_player:
                return False
        if top >= 0 and down < FIELDS:
            if self.board[n][top] == \
               self.board[n][top + 1] == \
               self.board[n][top + 2] == \
               self.board[n][top + 3] == \
               self.board[n][down] == \
               self.next_player:
                return True
        return False

    def check_winner_diagonally1(self, n, m, out_extent):
        """ Sprawdza czy wygrana po przekątnej \ """
        left = n - 2 + out_extent
        right = n + 2 + out_extent
        top = m - 2 + out_extent
        down = m + 2 + out_extent
        if left - 1 >= 0 and top - 1 >= 0:
            if self.board[left - 1][top - 1] == self.next_player:
                return False
        if right + 1 < FIELDS and down + 1 < FIELDS:
            if self.board[right + 1][down + 1] == self.next_player:
                return False
        if left >= 0 and right < FIELDS and top >= 0 and down < FIELDS:
            if self.board[left][top] == \
               self.board[left + 1][top + 1] == \
               self.board[left + 2][top + 2] == \
               self.board[left + 3][top + 3] == \
               self.board[right][down] == \
               self.next_player:
                return True
        return False

    def check_winner_diagonally2(self, n, m, out_extent):
        """ Sprawdza czy wygrana po przekątnej / """
        left = n - 2 + (-out_extent)
        right = n + 2 + (-out_extent)
        top = m - 2 + out_extent
        down = m + 2 + out_extent
        if right + 1 < FIELDS and top - 1 >= 0:
            if self.board[right + 1][top - 1] == self.next_player:
                return False
        if left - 1 >= 0 and down + 1 < FIELDS:
            if self.board[left - 1][down + 1] == self.next_player:
                return False
        if left >= 0 and right < FIELDS and top >= 0 and down < FIELDS:
            if self.board[right][top] == \
               self.board[left + 3][top + 1] == \
               self.board[left + 2][top + 2] == \
               self.board[left + 1][top + 3] == \
               self.board[left][down] == \
               self.next_player:
                return True
        return False

    def check_draw(self):
        if sum([j.count(PLAYER_1) + j.count(PLAYER_2) for j in self.board]) > (FIELDS-1)**2:
            self.winner = PLAYER_DRAW
            return True

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
            pygame.draw.line(self.screen, DARK_GRAY, (GRID_BEGIN, c), (GRID_END, c), 2)

    def create_players(self):
        self.player1 = Player(self.screen, self, 1, BLACK)
        self.player2 = Player(self.screen, self, 2, WHITE)


if __name__ == "__main__":
    print("You should run gomoku.py file")
