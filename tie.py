#!/usr/bin/env python3

import pygame

from constants import *
from player import *
from develop import *
from gui import *


class Tie(Gui):
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.next_player = 1
        self.board = [[EMPTY for n in range(FIELDS)] for m in range(FIELDS)]
        self.all_sprites = pygame.sprite.Group()
        self.winner = None
        self.last_move_n = None
        self.last_move_m = None
        self.create_players()
        self.draw_background(DARK_SAND)
        self.draw_grid()
        self.draw()
        self.show_actual_player()
        self.run()
        if LOG_TO_FILE == 1:
            init_debug_file()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FRAMES_PER_SECOND)
            self.events()
            self.update()
            self.draw()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.MOUSEBUTTONUP:
                if self.winner is not None:
                    self.playing = False
                if self.next_player == HUMAN:
                    self.move_human()
                if self.next_player == COMPUTER:
                    self.move_computer()
                # if event.button == 3:  # DEBUG:
                #     self.show_end_state_of_game()  # DEBUG:


    def update(self):
        self.all_sprites.update()


    def draw(self):
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


    def move_human(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        n, m = self.player1.move(mouse_x, mouse_y)
        if n is not None and m is not None:
            # if self.next_player == 1:  # DEBUG:
            #     print("if 1")  # DEBUG:
            if LOG_STATE_OF_BOARD > 0:
                print_board(self.board, "Tie")
            self.end_if_gameover(n, m, self.board)
            if self.winner is None:
                self.change_player()
                self.show_actual_player()
            self.last_move_n = n
            self.last_move_m = m
            self.draw()


    def move_computer(self):
        n, m = self.player2.move(self.last_move_n, self.last_move_m)
        if LOG_STATE_OF_BOARD > 0:
            print_board(self.board, "Tie")
        self.end_if_gameover(n, m, self.board)
        if self.winner is None:
            self.change_player()
            self.show_actual_player()


    def end_if_gameover(self, n, m, board):
        if self.check_winning(n, m, board, self.next_player):
            self.winner = board[n][m]
            self.show_end_state_of_game()
            self.events()
            self.next_player = None
        if self.check_draw(board):
            self.show_end_state_of_game()
            self.events()
            self.next_player = None


    def check_winning(self, n, m, board, player):
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
        if n is None or m is None:
            return False
        for out_extent in range(-2, 3):
            if (self.check_winning_horizontally(n, m, out_extent, board, player) or
                self.check_winning_vertically(n, m, out_extent, board, player) or
                self.check_winning_diagonally1(n, m, out_extent, board, player) or
                self.check_winning_diagonally2(n, m, out_extent, board, player)):
                return True


    def check_winning_horizontally(self, n, m, out_extent, board, player):
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
            if (board[left][m] == 
                board[left+1][m] == 
                board[left+2][m] == 
                board[left+3][m] == 
                board[right][m] == 
                player):
                return True
        return False


    def check_winning_vertically(self, n, m, out_extent, board, player):
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
            if (board[n][top] ==
                board[n][top + 1] ==
                board[n][top + 2] ==
                board[n][top + 3] ==
                board[n][down] ==
                player):
                # print("true")  # DEBUG:
                return True
        # print("f3")  # DEBUG:
        return False


    def check_winning_diagonally1(self, n, m, out_extent, board, player):
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
            if (board[left][top] == 
                board[left + 1][top + 1] == 
                board[left + 2][top + 2] == 
                board[left + 3][top + 3] == 
                board[right][down] == 
                player):
                return True
        return False


    def check_winning_diagonally2(self, n, m, out_extent, board, player):
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
            if (board[right][top] == 
                board[left + 3][top + 1] == 
                board[left + 2][top + 2] == 
                board[left + 1][top + 3] == 
                board[left][down] == 
                player):
                return True
        return False


    def check_draw(self, board):
        if sum([j.count(HUMAN) + j.count(COMPUTER) for j in board]) > (FIELDS-1)**2:
            self.winner = PLAYER_DRAW
            return True


    def change_player(self):
        if self.next_player == HUMAN:
            self.next_player = COMPUTER
        elif self.next_player == COMPUTER:
            self.next_player = HUMAN


    def create_players(self):
        self.player1 = Human(self.screen, self, HUMAN, BLACK)
        self.player2 = Computer(self.screen, self, COMPUTER, WHITE)



if __name__ == "__main__":
    print("You should run gomoku.py file")
