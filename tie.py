#!/usr/bin/env python3
"""Plansza Gomoku"""

import pygame

import constants as c
import develop
import gui
import player

# Ignore false positive pygame errors
# pylint: disable=E1101

class Tie(gui.Gui):
    """Reprezentacja planszy w Gomoku."""
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.next_player = c.HUMAN
        self.board = [[None for n in range(c.FIELDS)] for m in range(c.FIELDS)]
        self.all_sprites = pygame.sprite.Group()
        self.winner = None
        self.last_move_n = None
        self.last_move_m = None
        self.playing = True
        self.human = None
        self.computer = None


    def start(self):
        """Przygotowanie rozgrywki."""
        self.create_players()
        self.draw_background(c.GAME_BACKGROUND_COLOR)
        self.draw_grid()
        self.draw()
        self.show_actual_player()
        self.run()
        if c.LOG_TO_FILE == 1:
            develop.init_debug_file()


    def run(self):
        """Główna pętla programu podczas trwania rozgrywki."""
        self.playing = True
        while self.playing:
            self.clock.tick(c.FRAMES_PER_SECOND)
            self.events()
            self.update()
            self.draw()


    def events(self):
        """Obsługiwane zdarzenia podczas każdej pętli w run()."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.MOUSEBUTTONUP:
                if self.winner is not None:
                    self.playing = False
                if self.next_player == c.HUMAN:
                    self.move_human()
                if self.next_player == c.COMPUTER:
                    self.move_computer()


    def update(self):
        """Aktualizacja obiektów podczas każdej pętli w run()."""
        self.all_sprites.update()


    def draw(self):
        """Rysowanie obiektów na ekranie podczas każdej pętli w run()."""
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


    def move_human(self):
        """Wywołanie ruchu wykonywanego przez człowieka."""
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        i, j = self.human.move(mouse_x, mouse_y)
        if i is not None and j is not None:
            if c.LOG_STATE_OF_BOARD > 0:
                develop.print_board(self.board, "Tie")
            self.end_if_gameover(i, j, self.board)
            if self.winner is None:
                self.change_player()
                self.show_actual_player()
            self.last_move_n = i
            self.last_move_m = j
            self.draw()


    def move_computer(self):
        """Wywołanie ruchu wykonywanego przez komputer."""
        i, j = self.computer.move(self.last_move_n, self.last_move_m)
        if c.LOG_STATE_OF_BOARD > 0:
            develop.print_board(self.board, "Tie")
        self.end_if_gameover(i, j, self.board)
        if self.winner is None:
            self.change_player()
            self.show_actual_player()


    def end_if_gameover(self, i, j, board):
        """Kończenie gry, jeśli wystąpił koniec gry."""
        if self.check_winning(i, j, board, self.next_player):
            self.winner = board[i][j]
            self.show_end_state_of_game()
            self.events()
            self.next_player = None
        if self.check_draw(board):
            self.show_end_state_of_game()
            self.events()
            self.next_player = None


    def check_winning(self, i, j, board, actual_player):
        """Sprawdza czy koniec gry (wygrana lub remis).

        Przyjmuje jako argument współrzędne ostatniego ruchu ostatniego gracza
        (różne niż None), następnie dla r równych -2, -1, 0, 1, 2 sprawdza czy
        wygrana wystąpiła w poziomie, pionie lub po któreś z przekątnych

        zmienna out_extent pozwala pokryć wszystkie możliwości skrajne i
        pośrednie przy sprawdzaniu wygranej np.: dla sprawdzania w poziomie:
        +++++____  _+++++___  __+++++__  ___+++++_  ____+++++
        gdzie + oznacza kamień jednego gracza,
        a _ puste miejsce lub kamień drugiego gracza
        """
        if i is None or j is None:
            return False
        for out_extent in range(-2, 3):
            if (self.check_winning_horizontally(i, j, out_extent, board,
                                                actual_player) or
                    self.check_winning_vertically(i, j, out_extent, board,
                                                  actual_player) or
                    self.check_winning_diagonally1(i, j, out_extent, board,
                                                   actual_player) or
                    self.check_winning_diagonally2(i, j, out_extent, board,
                                                   actual_player)):
                return True
        return None


    def check_winning_horizontally(self, i, j, out_extent, board, actual_player):
        """Sprawdza czy wygrana w poziomie.

        Przyjmuje jako argument współrzędne ostatniego ruchu ostatniego gracza.
        Pomija sprawdzanie pól, które są poza planszą (_ < 0 lub _ >= FIELDS).
        Sprawdza czy (w linii złożonej z 5 kamieni) poprzedni i następny kamień
        nie są tego samego gracza. Potem sprawdza czy w poziomie jest dokładnie
        5 takich samych kamieni.
        """
        left = i - 2 + out_extent
        right = i + 2 + out_extent
        if left - 1 >= 0:
            if board[left - 1][j] == actual_player:
                return False
        if right + 1 < c.FIELDS:
            if board[right + 1][j] == actual_player:
                return False
        if left >= 0 and right < c.FIELDS:
            if (board[left][j] ==
                    board[left+1][j] ==
                    board[left+2][j] ==
                    board[left+3][j] ==
                    board[right][j] ==
                    actual_player):
                return True
        return False


    def check_winning_vertically(self, i, j, out_extent, board, actual_player):
        """Sprawdza czy wygrana w pionie."""
        top = j - 2 + out_extent
        down = j + 2 + out_extent
        if top - 1 >= 0:
            if board[i][top - 1] == actual_player:
                return False
        if down + 1 < c.FIELDS:
            if board[i][down + 1] == actual_player:
                return False
        if top >= 0 and down < c.FIELDS:
            if (board[i][top] ==
                    board[i][top + 1] ==
                    board[i][top + 2] ==
                    board[i][top + 3] ==
                    board[i][down] ==
                    actual_player):
                return True
        return False


    def check_winning_diagonally1(self, i, j, out_extent, board, actual_player):
        """Sprawdza czy wygrana po przekątnej \ ."""  # pylint: disable=anomalous-backslash-in-string
        left = i - 2 + out_extent
        right = i + 2 + out_extent
        top = j - 2 + out_extent
        down = j + 2 + out_extent
        if left - 1 >= 0 and top - 1 >= 0:
            if board[left - 1][top - 1] == actual_player:
                return False
        if right + 1 < c.FIELDS and down + 1 < c.FIELDS:
            if board[right + 1][down + 1] == actual_player:
                return False
        if left >= 0 and right < c.FIELDS and top >= 0 and down < c.FIELDS:
            if (board[left][top] ==
                    board[left + 1][top + 1] ==
                    board[left + 2][top + 2] ==
                    board[left + 3][top + 3] ==
                    board[right][down] ==
                    actual_player):
                return True
        return False


    def check_winning_diagonally2(self, i, j, out_extent, board, actual_player):
        """Sprawdza czy wygrana po przekątnej / ."""
        left = i - 2 + (-out_extent)
        right = i + 2 + (-out_extent)
        top = j - 2 + out_extent
        down = j + 2 + out_extent
        if right + 1 < c.FIELDS and top - 1 >= 0:
            if board[right + 1][top - 1] == actual_player:
                return False
        if left - 1 >= 0 and down + 1 < c.FIELDS:
            if board[left - 1][down + 1] == actual_player:
                return False
        if left >= 0 and right < c.FIELDS and top >= 0 and down < c.FIELDS:
            if (board[right][top] ==
                    board[left + 3][top + 1] ==
                    board[left + 2][top + 2] ==
                    board[left + 1][top + 3] ==
                    board[left][down] ==
                    actual_player):
                return True
        return False


    def check_draw(self, board):
        """Sprawdzanie czy wystąpił remis."""
        if (sum([j.count(c.HUMAN) + j.count(c.COMPUTER) for j in board])
                > (c.FIELDS-1)**2):
            self.winner = c.PLAYER_DRAW
            return True
        return False


    def change_player(self):
        """Zmiana gracza."""
        if self.next_player == c.HUMAN:
            self.next_player = c.COMPUTER
        elif self.next_player == c.COMPUTER:
            self.next_player = c.HUMAN


    def create_players(self):
        """Stworzenie obiektów graczy."""
        self.human = player.Human(self.screen, self, c.HUMAN,
                                  c.HUMAN_STONES_COLOR)
        self.computer = player.Computer(self.screen, self, c.COMPUTER,
                                        c.COMPUTER_STONES_COLOR)



if __name__ == "__main__":
    print("You should run gomoku.py file")
