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
        if n != None and m != None:
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
        następnie dla r równych -2, -1, 0, 1, 2 sprawdza czy wygrana wystąpiła
        w poziomie, pionie lub po któreś z przekątnych

        r pozwala pokryć wszystkie możliwości skrajne i pośrednie przy
        sprawdzaniu wygranej np.: dla sprawdzania w poziomie:
        +++++____ _+++++___ __+++++__ ___+++++_ ____+++++
        gdzie + oznacza kamień jednego gracza,
        a _ puste miejsce lub kamień drugiego gracza
        """
        if n != None and m != None:
            for r in range(-2, 3):
                if self.check_winner_horizontally(n, m, r) or \
                   self.check_winner_vertically(n, m, r) or \
                   self.check_winner_diagonally1(n, m, r) or \
                   self.check_winner_diagonally2(n, m, r):
                    self.winner = self.board[n][m]
                    return self.board[n][m]

    def check_winner_horizontally(self, n, m, r):
        """ Sprawdza czy wygrana w poziomie

        Przyjmuje jako argument współrzędne ostatniego ruchu ostatniego gracza.
        Pomija sprawdzanie pól, które są poza planszą (_ < 0 lub _ > FIELDS).
        Potem sprawdza czy w poziomie jest dokładnie 5 takich samych kamieni,
        czyli sprawdza również czy poprzedni kamień i następny kamień nie są
        tego samego gracza.
        """
        left = n - 2 + r
        right = n + 2 + r
        more_left = left - 1
        more_right = right + 1
        if left >= 0 and right < FIELDS:
            s1 = self.board[left][m]
            s2 = self.board[left+1][m]
            s3 = self.board[left+2][m]
            s4 = self.board[left+3][m]
            s5 = self.board[right][m]
            print("h ", s1, s2, s3, s4, s5)
        else:
            return False
        if more_left >= 0:
            s0 = self.board[more_left][m]
        else:
            s0 = None
        if more_right < FIELDS:
            s6 = self.board[more_right][m]
        else:
            s6 = None

        if s1 == s2 == s3 == s4 == s5 == self.next_player and s0 != s1 and s5 != s6:
            return True

    def check_winner_vertically(self, n, m, r):
        """ Sprawdza czy wygrana w pionie """
        top = m - 2 + r
        down = m + 2 + r
        more_top = top - 1
        more_down = down + 1
        if top >= 0 and down < FIELDS:
            s1 = self.board[n][top]
            s2 = self.board[n][top + 1]
            s3 = self.board[n][top + 2]
            s4 = self.board[n][top + 3]
            s5 = self.board[n][down]
            print("v ", s1, s2, s3, s4, s5)
        else:
            return False
        if more_top >= 0:
            s0 = self.board[n][more_top]
        else:
            s0 = None
        if more_down < FIELDS:
            s6 = self.board[n][more_down]
        else:
            s6 = None

        if s1 == s2 == s3 == s4 == s5 == self.next_player and s0 != s1 and s5 != s6:
            return True

    def check_winner_diagonally1(self, n, m, r):
        """ Sprawdza czy wygrana po przekątnej  """
        left = n - 2 + r
        right = n + 2 + r
        more_left = left - 1
        more_right = right + 1
        top = m - 2 + r
        down = m + 2 + r
        more_top = top - 1
        more_down = down + 1
        if left >= 0 and right < FIELDS and top >= 0 and down < FIELDS:
            s1 = self.board[left][top]
            s2 = self.board[left + 1][top + 1]
            s3 = self.board[left + 2][top + 2]
            s4 = self.board[left + 3][top + 3]
            s5 = self.board[right][down]
        else:
            return False
        if more_left >= 0 and more_top >= 0:
            s0 = self.board[more_left][more_top]
        else:
            s0 = None
        if more_right < FIELDS and more_down < FIELDS:
            s6 = self.board[more_right][more_down]
        else:
            s6 = None

        if s1 == s2 == s3 == s4 == s5 == self.next_player and s0 != s1 and s5 != s6:
            return True

    def check_winner_diagonally2(self, n, m, r):
        """ Sprawdza czy wygrana po przekątnej / """
        s = -r
        left = n - 2 + s
        right = n + 2 + s
        more_left = left - 1
        more_right = right + 1
        top = m - 2 + r
        down = m + 2 + r
        more_top = top - 1
        more_down = down + 1
        # print("d2 n =", n, "m =", m, "n €", left, right, "m €", top, down)
        if left >= 0 and right < FIELDS and top >= 0 and down < FIELDS:
            s1 = self.board[right][top]
            s2 = self.board[left + 3][top + 1]
            s3 = self.board[left + 2][top + 2]
            s4 = self.board[left + 1][top + 3]
            s5 = self.board[left][down]
        else:
            return False
        if more_right < FIELDS and more_top >= 0:
            s0 = self.board[more_right][more_top]
        else:
            s0 = None
        if more_left >= 0 and more_down < FIELDS:
            s6 = self.board[more_left][more_down]
        else:
            s6 = None

        if s1 == s2 == s3 == s4 == s5 == self.next_player and s0 != s1 and s5 != s6:
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
            # pygame.gfxdraw.line(self.screen, c, GRID_BEGIN, c, GRID_END, DARK_GRAY)
            pygame.draw.line(self.screen, DARK_GRAY, (GRID_BEGIN, c), (GRID_END, c), 2)
            # pygame.gfxdraw.line(self.screen, GRID_BEGIN, c, GRID_END, c, DARK_GRAY)

    def create_players(self):
        self.player1 = Player(self.screen, self, 1, BLACK)
        self.player2 = Player(self.screen, self, 2, WHITE)


if __name__ == "__main__":
    print("You should run gomoku.py file")
