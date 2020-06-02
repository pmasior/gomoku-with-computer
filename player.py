#!/usr/bin/env python3
"""Gracz w grze Gomoku"""

import math
import copy
import pygame

import constants as c
from develop import print_board
from stone import Stone


class Player:
    """Klasa reprezentująca gracza w grze."""
    def __init__(self, screen, tie, number, color):
        self.screen = screen
        self.tie = tie
        self.number = number
        self.color = color
        self.stone_sprites = pygame.sprite.Group()


    def check_if_field_is_empty(self, n, m, board): # pylint: disable=invalid-name
        """Sprawdza, czy pole w tabeli jest puste."""
        if board[n][m] is c.EMPTY: # pylint: disable=invalid-name
            return True
        return False


    def write_move(self, n, m): # pylint: disable=invalid-name
        """Zapisuje ruch na planszy."""
        self.tie.board[n][m] = self.number # pylint: disable=invalid-name


    def draw_move(self, x, y): # pylint: disable=invalid-name
        """Tworzy nowy kamień i pokazuje go na planszy."""
        stone = Stone(self.color, x, y)
        self.tie.all_sprites.add(stone)
        self.stone_sprites.add(stone)



class Human(Player):
    """Reprezentuje gracza, który jest człowiekim."""
    def move(self, mouse_x, mouse_y):
        """Sprawdza czy ruch jest dozwolony, jeśli jest to go wykonuje."""
        for m in range(0, c.FIELDS):  # pylint: disable=invalid-name
            y = c.GRID_Y_BEGIN + m * c.GRID_TILESIZE  # pylint: disable=invalid-name
            for n in range(0, c.FIELDS):  # pylint: disable=invalid-name
                x = c.GRID_X_BEGIN + n * c.GRID_TILESIZE  # pylint: disable=invalid-name
                if (self.check_if_clicked_in_field(x, y, mouse_x, mouse_y) and
                        self.check_if_field_is_empty(n, m, self.tie.board)):
                    self.write_move(n, m)
                    self.draw_move(x, y)
                    return n, m
        return None, None


    def check_if_clicked_in_field(self, x, y, mouse_x, mouse_y):  # pylint: disable=invalid-name
        """Sprawdza czy kliknięto w pole planszy."""
        if math.hypot(mouse_x - x, mouse_y - y) < c.STONE_RADIUS:
            return True
        return False



class Computer(Player):
    """Reprezentuje komputer jako gracza."""
    def __init__(self, screen, tie, number, color):
        super().__init__(screen, tie, number, color)
        self.next_move_n = None
        self.next_move_m = None
        self.next_move_beta_n = None
        self.next_move_beta_m = None
        self.board_copy = copy.deepcopy(self.tie.board)


    def move(self, last_move_n, last_move_m):
        """Wykonuje ruch komputera."""
        self.board_copy = copy.deepcopy(self.tie.board)
        self.find_move(last_move_n, last_move_m)
        x = c.GRID_X_BEGIN + self.next_move_n * c.GRID_TILESIZE  # pylint: disable=invalid-name
        y = c.GRID_Y_BEGIN + self.next_move_m * c.GRID_TILESIZE  # pylint: disable=invalid-name
        self.write_move(self.next_move_n, self.next_move_m)
        self.draw_move(x, y)
        return self.next_move_n, self.next_move_m


    def empty_fields_around(self, n, m, area=1):  # pylint: disable=invalid-name
        """ Zwraca zbiór pustych pól wokól zadanych współrzędnych."""
        near_empty_fields = set()
        left, top, right, bottom = \
            self.improve_range_of_array(n - area, n + area, m - area, m + area)
        for i in range(left, right + 1):
            for j in range(top, bottom + 1):
                if self.check_if_field_is_empty(i, j, self.board_copy):
                    near_empty_fields.add((i, j))
        return near_empty_fields


    def get_empty_fields(self, area=1, last_move_n=None, last_move_m=None):
        """Zwraca listę pustych pól.

        Najpierw tworzy zbiór pustych pól wokół ostatniego ruchu człowieka,
        potem tworzy nowy zbiór pustych pól wokół wszystkich kamieni na planszy,
        ale niezawierający pól z wcześniejszego zbioru.
        Dzięki temu dostarcza funkcji alfa_beta() w pierwszej kolejności pola,
        które mogą mieć największe znaczenie dla wygranej w grze.
        """
        empty_fields = list()
        near_empty_fields = set()
        rest_empty_fields = set()
        for i in range(c.FIELDS):
            for j in range(c.FIELDS):
                if self.board_copy[i][j] is not c.EMPTY:
                    near_empty_fields |= self.empty_fields_around(i, j, area)

        if last_move_n is not None or last_move_m is not None:
            near_last_move_empty_fields = self.empty_fields_around(last_move_n,
                                                                   last_move_m)
            empty_fields.extend(list(near_last_move_empty_fields))
            near_empty_fields -= near_last_move_empty_fields

        empty_fields.extend(list(near_empty_fields))
        empty_fields.extend(list(rest_empty_fields))
        return empty_fields


    def improve_range_of_array(self, left, right, top, bottom):
        """Zapewnia, że współrzędne nie wychodzą poza zakres tablicy."""
        while left < 0:
            left += 1
        while top < 0:
            top += 1
        while right >= c.FIELDS:
            right -= 1
        while bottom >= c.FIELDS:
            bottom -= 1
        return left, top, right, bottom


    def score_in_alfa_beta(self, n, m, depth, winning, draw):  # pylint: disable=invalid-name, too-many-arguments
        """Ocenia aktualny stan gry względem każdego gracza."""
        if depth % 2 == 0:
            earlier_player = c.HUMAN
        elif depth % 2 == 1:
            earlier_player = c.COMPUTER
        final_score = self.score_final_situation(earlier_player, depth,
                                                 winning, draw)
        nonfinal_score = self.score_nonfinal_situation(n, m,
                                                       earlier_player, depth)
        if final_score is not None:
            return final_score
        if nonfinal_score is not None:
            return nonfinal_score
        return 0  #None

    def score_final_situation(self, earlier_player, depth, winning, draw):
        """Ocenia aktualny stan gry w przypadku wygranej lub remisu."""
        if winning and earlier_player == c.HUMAN:
            return depth - 100
        if winning and earlier_player == c.COMPUTER:
            return 100 - depth
        if draw:
            return 0
        return None


    def score_nonfinal_situation(self, n, m, earlier_player, depth):  # pylint: disable=invalid-name
        """Ocenia aktualny stan gry w przypadku, gdy gra nie kończy się."""
        horizontally = list()
        vertically = list()
        diagonally1 = list()
        diagonally2 = list()
        for i in range(-5, 5 + 1):
            if n + i >= 0 and n + i < c.FIELDS:
                horizontally.append(self.board_copy[n + i][m])
            if m + i >= 0 and m + i < c.FIELDS:
                vertically.append(self.board_copy[n][m + i])
            if n + i >= 0 and n + i < c.FIELDS and m + i >= 0 and m + i < c.FIELDS:
                diagonally1.append(self.board_copy[n + i][m + i])
            if n - i >= 0 and n - i < c.FIELDS and m + i >= 0 and m + i < c.FIELDS:
                diagonally2.append(self.board_copy[n - i][m + i])

        score = 0
        for tab in horizontally, vertically, diagonally1, diagonally2:
            for i in range(0, 5 + 1):
                line = tab[i:i+6]
                temp_score = self.score_nonfinal_situation_in_line(line,
                                                                   earlier_player)
                score = max(temp_score, score)
        if earlier_player == c.HUMAN:
            return depth - score
        if earlier_player == c.COMPUTER:
            return score - depth
        return None


    def score_nonfinal_situation_in_line(self, line, me):  # pylint: disable=invalid-name
        """Ocenia sytuację w jednej linii planszy przekazanej jako argument."""
        if len(line) == 6:
            none_s = line.count(c.EMPTY)
            if me == c.HUMAN:
                me_s = line.count(c.HUMAN)
                opponent = c.COMPUTER
            elif me == c.COMPUTER:
                me_s = line.count(c.COMPUTER)
                opponent = c.HUMAN

            if me_s == 4:
                for i in range(-2, 1):
                    if line[i] == line[i+1] == c.EMPTY:
                        return 80
                if none_s == 2 and ((line[0] is c.EMPTY) != (line[-1] is c.EMPTY)):
                    return 70
                if none_s == 1 and ((line[0] == opponent) != (line[-1] == opponent)):
                    return 70

            if none_s == 3:
                for i in range(0, 4):
                    if line[i:i+3].count(me) == 3:
                        return 60
                if me_s == 3 and line[0] == line[-1] is c.EMPTY:
                    return 50

            if none_s == 2:
                if (line[0] == opponent) != (line[-1] == opponent):
                    for i in (1, 2):
                        if line[i:i+3].count(me) == 3:
                            return 50
                if line[0:3].count(me) == 3 and line[-1] == opponent:
                    return 50
                if line[3:6].count(me) == 3 and line[0] == opponent:
                    return 50
        return 0


    def find_move(self, last_move_n, last_move_m):
        """Wybiera następny ruch komputera.

        Wykorzystuje pętlę algorytmu minimax dla gracza MAX, żeby wyznaczyć
        następny ruch komputera, który zostaje zapisany jako atrybut klasy
        Computer.
        """
        alfa = -math.inf
        empty_fields = self.get_empty_fields(1, last_move_n, last_move_m)
        for empty_field in empty_fields:
            n, m = empty_field  # pylint: disable=invalid-name
            self.board_copy[n][m] = c.COMPUTER
            value = self.alfa_beta(alfa, math.inf, n, m, 1)
            self.board_copy[n][m] = c.EMPTY
            if value > alfa:
                alfa = value
                self.next_move_n, self.next_move_m = n, m


    def alfa_beta(self, alfa, beta, n=None, m=None, depth=0):  # pylint: disable=invalid-name, too-many-arguments
        """Wybiera następny ruch komputera przy użyciu algorytmu alfa-beta.

        Argumenty:
        alfa -- największa wartość dla gracza MAX (komputera)
        beta -- najmniejsza wartość dla gracza MIN (człowiek)
        n -- współrzędna ostatniego ruchu (istotne w dalszych wywołaniach rek.)
        m -- współrzędna ostatniego ruchu (istotne w dalszych wywołaniach rek.)
        depth -- głębokość rekurencji
        Algorytm minimax to algorytm przeszukujący w głąb drzewo, które na
        kolejnych głębokościach,  zaczynając od najwyższego zawiera wszystkie
        możliwe ruchy graczy.
        Algorytm alfa-beta jest jego ulepszeniem. Zawiera on dodatkowo dwie
        wartości α i β. Początkowo α = -∞ i β = ∞. W miarę przechodzenia do
        kolejnych wywołań rekurencyjnych, α zwiększa się, a β zmiejsza się.
        Gdy α ≥ β, to oznacza to, że wybór tej opcji nie będzie lepszy od
        poprzednio zbadanych opcji, dlatego nie ma potrzeby dalszego
        przeszukiwania tej gałęzi.
        """
        if c.LOG_STATE_OF_BOARD > 1:
            print_board(self.board_copy, "alfa_beta()")
        if depth % 2 == 0:
            player = c.COMPUTER
            earlier_player = c.HUMAN
        elif depth % 2 == 1:
            player = c.HUMAN
            earlier_player = c.COMPUTER

        winning = self.tie.check_winning(n, m, self.board_copy, earlier_player)
        draw = self.tie.check_draw(self.board_copy)
        if winning or draw or depth == c.MAX_DEPTH:
            score = self.score_in_alfa_beta(n, m, depth, winning, draw)
            return score

        if player == c.COMPUTER:
            value = -math.inf
            for empty_field in self.get_empty_fields(1, n, m):
                n, m = empty_field
                self.board_copy[n][m] = player
                value = self.alfa_beta(alfa, beta, n, m, depth + 1)
                self.board_copy[n][m] = c.EMPTY
                if value > alfa:
                    alfa = value
                if alfa >= beta:
                    return beta
            return alfa
        if player == c.HUMAN:
            value = math.inf
            for empty_field in self.get_empty_fields(1):
                n, m = empty_field
                self.board_copy[n][m] = player
                value = self.alfa_beta(alfa, beta, n, m, depth + 1)
                self.board_copy[n][m] = c.EMPTY
                if value < beta:
                    beta = value
                if alfa >= beta:
                    return alfa
            return beta
        return None


if __name__ == "__main__":
    print("You should run gomoku.py file")
