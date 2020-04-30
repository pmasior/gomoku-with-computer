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
        if LOG_TO_FILE == 1:
            init_debug_file()

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
                if self.next_player == PLAYER_1:
                    self.move_human()

    def update(self):
        self.all_sprites.update()
        if self.next_player == PLAYER_2:
            self.move_computer()

    def draw(self):
        pygame.display.flip()
        self.all_sprites.draw(self.screen)

    def move_human(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        n, m = self.player1.move(mouse_x, mouse_y)
        if n != None and m != None:
            # if self.next_player == 1:  # DEBUG:
            #     print("if 1")  # DEBUG:
            self.draw()
            if LOG_STATE_OF_BOARD > 0:
                print_board(self.board, "Tie")
            self.draw()
            self.end_if_gameover(n, m, self.board)
            self.change_player()

    def move_computer(self):
        n, m = self.player2.move()
        if LOG_STATE_OF_BOARD > 0:
            print_board(self.board, "Tie")
        self.end_if_gameover(n, m, self.board)
        self.change_player()

    def end_if_gameover(self, n, m, board):
        if self.check_winner(n, m, board, self.next_player):
            self.winner = board[n][m]
            self.playing = False
        if self.check_draw(board):
            self.playing = False

    def check_winner(self, n, m, board, player):
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
        if n == None or m == None:
            return False
        for out_extent in range(-2, 3):
            if self.check_winner_horizontally(n, m, out_extent, board, player) or \
               self.check_winner_vertically(n, m, out_extent, board, player) or \
               self.check_winner_diagonally1(n, m, out_extent, board, player) or \
               self.check_winner_diagonally2(n, m, out_extent, board, player):
                return True

    def check_winner_horizontally(self, n, m, out_extent, board, player):
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
            if board[left - 1][m] == player:
                return False
        if right + 1 < FIELDS:
            if board[right + 1][m] == player:
                return False
        if left >= 0 and right < FIELDS:
            if board[left][m] == \
               board[left+1][m] == \
               board[left+2][m] == \
               board[left+3][m] == \
               board[right][m] == \
               player:
                return True
        return False

    def check_winner_vertically(self, n, m, out_extent, board, player):
        """ Sprawdza czy wygrana w pionie """
        top = m - 2 + out_extent
        down = m + 2 + out_extent
        if top - 1 >= 0:
            if board[n][top - 1] == player:
                # print("f1")  # DEBUG:
                return False
        if down + 1 < FIELDS:
            if board[n][down + 1] == player:
                # print("f2")  # DEBUG:
                return False
        if top >= 0 and down < FIELDS:
            if board[n][top] == \
               board[n][top + 1] == \
               board[n][top + 2] == \
               board[n][top + 3] == \
               board[n][down] == \
               player:
                # print("true")  # DEBUG:
                return True
        # print("f3")  # DEBUG:
        return False

    def check_winner_diagonally1(self, n, m, out_extent, board, player):
        """ Sprawdza czy wygrana po przekątnej \ """
        left = n - 2 + out_extent
        right = n + 2 + out_extent
        top = m - 2 + out_extent
        down = m + 2 + out_extent
        if left - 1 >= 0 and top - 1 >= 0:
            if board[left - 1][top - 1] == player:
                return False
        if right + 1 < FIELDS and down + 1 < FIELDS:
            if board[right + 1][down + 1] == player:
                return False
        if left >= 0 and right < FIELDS and top >= 0 and down < FIELDS:
            if board[left][top] == \
               board[left + 1][top + 1] == \
               board[left + 2][top + 2] == \
               board[left + 3][top + 3] == \
               board[right][down] == \
               player:
                return True
        return False

    def check_winner_diagonally2(self, n, m, out_extent, board, player):
        """ Sprawdza czy wygrana po przekątnej / """
        left = n - 2 + (-out_extent)
        right = n + 2 + (-out_extent)
        top = m - 2 + out_extent
        down = m + 2 + out_extent
        if right + 1 < FIELDS and top - 1 >= 0:
            if board[right + 1][top - 1] == player:
                return False
        if left - 1 >= 0 and down + 1 < FIELDS:
            if board[left - 1][down + 1] == player:
                return False
        if left >= 0 and right < FIELDS and top >= 0 and down < FIELDS:
            if board[right][top] == \
               board[left + 3][top + 1] == \
               board[left + 2][top + 2] == \
               board[left + 1][top + 3] == \
               board[left][down] == \
               player:
                return True
        return False

    def check_draw(self, board):
        if sum([j.count(PLAYER_1) + j.count(PLAYER_2) for j in board]) > (FIELDS-1)**2:
            self.winner = PLAYER_DRAW
            return True

    def change_player(self):
        if self.next_player == PLAYER_1:
            self.next_player = PLAYER_2
        elif self.next_player == PLAYER_2:
            self.next_player = PLAYER_1

    def draw_background(self):
        self.screen.fill(DARK_SAND)

    def draw_grid(self):
        """ Rysuje pionowe i poziome linie """
        for c in range(GRID_BEGIN, GRID_END, GRID_TILESIZE):
            pygame.draw.line(self.screen, SAND, (c, GRID_BEGIN), (c, GRID_END), 2)
            pygame.draw.line(self.screen, SAND, (GRID_BEGIN, c), (GRID_END, c), 2)

    def create_players(self):
        self.player1 = Human(self.screen, self, PLAYER_1, BLACK)
        self.player2 = Computer(self.screen, self, PLAYER_2, WHITE)



if __name__ == "__main__":
    print("You should run gomoku.py file")
