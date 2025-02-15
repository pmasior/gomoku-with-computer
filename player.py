#!/usr/bin/env python3
"""Gracz w grze Gomoku"""

import copy
import math

import pygame

import constants as c
import develop
import stone


class Player:
    """Klasa reprezentująca gracza w grze."""
    def __init__(self, screen, tie, number, color):
        self.screen = screen
        self.actual_tie = tie
        self.number = number
        self.color = color
        self.stone_sprites = pygame.sprite.Group()


    def check_if_field_is_empty(self, move_i, move_j, board):
        """Sprawdza, czy pole w tabeli jest puste."""
        if board[move_i][move_j] is None:
            return True
        return False


    def write_move(self, move_i, move_j):
        """Zapisuje ruch na planszy."""
        self.actual_tie.board[move_i][move_j] = self.number


    def draw_move(self, x_position, y_position):
        """Tworzy nowy kamień i pokazuje go na planszy."""
        new_stone = stone.Stone(self.color, x_position, y_position)
        self.actual_tie.all_sprites.add(new_stone)
        self.stone_sprites.add(new_stone)



class Human(Player):
    """Reprezentuje gracza, który jest człowiekim."""
    def move(self, mouse_x, mouse_y):
        """Sprawdza czy ruch jest dozwolony, jeśli jest to go wykonuje."""
        for j in range(c.FIELDS):
            y_position = c.GRID_Y_BEGIN + j * c.GRID_TILESIZE
            for i in range(c.FIELDS):
                x_position = c.GRID_X_BEGIN + i * c.GRID_TILESIZE
                if (self.check_if_clicked_in_field(x_position, y_position,
                                                   mouse_x, mouse_y) and
                        self.check_if_field_is_empty(i, j, self.actual_tie.board)):
                    self.write_move(i, j)
                    self.draw_move(x_position, y_position)
                    return i, j
        return None, None


    def check_if_clicked_in_field(self, x_position, y_position, mouse_x, mouse_y):
        """Sprawdza czy kliknięto w pole planszy."""
        if math.hypot(mouse_x - x_position, mouse_y - y_position) < c.STONE_RADIUS:
            return True
        return False



class Computer(Player):
    """Reprezentuje komputer jako gracza."""
    def __init__(self, screen, tie, number, color):
        super().__init__(screen, tie, number, color)
        self.next_move_i = None
        self.next_move_j = None
        self.next_move_beta_i = None
        self.next_move_beta_j = None
        self.board_copy = copy.deepcopy(self.actual_tie.board)


    def move(self, last_move_i, last_move_j):
        """Wykonuje ruch komputera."""
        self.board_copy = copy.deepcopy(self.actual_tie.board)
        self.find_move(last_move_i, last_move_j)
        x_position = c.GRID_X_BEGIN + self.next_move_i * c.GRID_TILESIZE
        y_position = c.GRID_Y_BEGIN + self.next_move_j * c.GRID_TILESIZE
        self.write_move(self.next_move_i, self.next_move_j)
        self.draw_move(x_position, y_position)
        return self.next_move_i, self.next_move_j


    def empty_fields_around(self, move_i, move_j, area=1):
        """ Zwraca zbiór pustych pól wokól zadanych współrzędnych."""
        near_empty_fields = set()
        left, top, right, bottom = (
            self.improve_range_of_array(move_i - area, move_i + area,
                                        move_j - area, move_j + area))
        for i in range(left, right + 1):
            for j in range(top, bottom + 1):
                if self.check_if_field_is_empty(i, j, self.board_copy):
                    near_empty_fields.add((i, j))
        return near_empty_fields


    def get_empty_fields(self, area=1, move_i=None, move_j=None):
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
                if self.board_copy[i][j] is not None:
                    near_empty_fields |= self.empty_fields_around(i, j, area)

        if move_i is not None or move_j is not None:
            near_move_empty_fields = self.empty_fields_around(move_i, move_j)
            empty_fields.extend(list(near_move_empty_fields))
            near_empty_fields -= near_move_empty_fields

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


    def score_in_alfa_beta(self, move_i, move_j, depth, winning, draw):  # pylint: disable=too-many-arguments
        """Ocenia aktualny stan gry względem każdego gracza."""
        if depth % 2 == 0:
            earlier_player = c.HUMAN
        elif depth % 2 == 1:
            earlier_player = c.COMPUTER
        final_score = self.score_final_situation(earlier_player, depth,
                                                 winning, draw)
        nonfinal_score = self.score_nonfinal_situation(move_i, move_j,
                                                       earlier_player, depth)
        if final_score is not None:
            return final_score
        if nonfinal_score is not None:
            return nonfinal_score
        return 0

    def score_final_situation(self, earlier_player, depth, winning, draw):
        """Ocenia aktualny stan gry w przypadku wygranej lub remisu."""
        if winning and earlier_player == c.HUMAN:
            return depth - 100
        if winning and earlier_player == c.COMPUTER:
            return 100 - depth
        if draw:
            return 0
        return None


    def score_nonfinal_situation(self, move_i, move_j, earlier_player, depth):
        """Ocenia aktualny stan gry w przypadku, gdy gra nie kończy się."""
        horizontally = list()
        vertically = list()
        diagonally1 = list()
        diagonally2 = list()
        for i in range(*c.RANGE_OF_LINES_NEARBY_STONE):
            if move_i + i >= 0 and move_i + i < c.FIELDS:
                horizontally.append(self.board_copy[move_i + i][move_j])
            if move_j + i >= 0 and move_j + i < c.FIELDS:
                vertically.append(self.board_copy[move_i][move_j + i])
            if (move_i + i >= 0 and move_i + i < c.FIELDS and
                    move_j + i >= 0 and move_j + i < c.FIELDS):
                diagonally1.append(self.board_copy[move_i + i][move_j + i])
            if (move_i - i >= 0 and move_i - i < c.FIELDS and
                    move_j + i >= 0 and move_j + i < c.FIELDS):
                diagonally2.append(self.board_copy[move_i - i][move_j + i])

        score = 0
        for tab in horizontally, vertically, diagonally1, diagonally2:
            for i in range(c.LINE_LENGTH_TO_CHECK):
                line = tab[i:i+c.LINE_LENGTH_TO_CHECK]
                temp_score = self.score_nonfinal_situation_in_line(line,
                                                                   earlier_player)
                score = max(temp_score, score)
        if earlier_player == c.HUMAN:
            return depth - score
        if earlier_player == c.COMPUTER:
            return score - depth
        return None


    def score_nonfinal_situation_in_line(self, line, player):
        """Ocenia sytuację w jednej linii planszy przekazanej jako argument."""
        if len(line) == 6:
            none_stones = line.count(None)
            if player == c.HUMAN:
                me_stones = line.count(c.HUMAN)
                opponent = c.COMPUTER
            elif player == c.COMPUTER:
                me_stones = line.count(c.COMPUTER)
                opponent = c.HUMAN

            if me_stones == 4:
                for i in range(-2, 1):
                    if line[i] == line[i+1] == None:
                        return 80
                if none_stones == 2 and ((line[0] is None) != (line[-1] is None)):
                    return 70
                if none_stones == 1 and ((line[0] == opponent) != (line[-1] == opponent)):
                    return 70

            if none_stones == 3:
                for i in range(0, 4):
                    if line[i:i+3].count(player) == 3:
                        return 60
                if me_stones == 3 and line[0] == line[-1] is None:
                    return 50

            if none_stones == 2:
                if (line[0] == opponent) != (line[-1] == opponent):
                    for i in (1, 2):
                        if line[i:i+3].count(player) == 3:
                            return 50
                if line[0:3].count(player) == 3 and line[-1] == opponent:
                    return 50
                if line[3:6].count(player) == 3 and line[0] == opponent:
                    return 50
        return 0


    def find_move(self, last_move_i, last_move_j):
        """Wybiera następny ruch komputera.

        Wykorzystuje pętlę algorytmu minimax dla gracza MAX, żeby wyznaczyć
        następny ruch komputera, który zostaje zapisany jako atrybut klasy
        Computer.
        """
        alfa = -math.inf
        empty_fields = self.get_empty_fields(1, last_move_i, last_move_j)
        for i, j in empty_fields:
            self.board_copy[i][j] = c.COMPUTER
            value = self.alfa_beta(alfa, math.inf, i, j, 1)
            self.board_copy[i][j] = None
            if value > alfa:
                alfa = value
                self.next_move_i, self.next_move_j = i, j


    def alfa_beta(self, alfa, beta, move_i=None, move_j=None, depth=0):  # pylint: disable=too-many-arguments
        """Wybiera następny ruch komputera przy użyciu algorytmu alfa-beta.

        Argumenty:
        alfa -- największa wartość dla gracza MAX (komputera)
        beta -- najmniejsza wartość dla gracza MIN (człowiek)
        i -- współrzędna ostatniego ruchu (istotne przy sprawdzaniu wygranej)
        j -- współrzędna ostatniego ruchu (istotne przy sprawdzaniu wygranej)
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
            develop.print_board(self.board_copy, "alfa_beta()")
        if depth % 2 == 0:
            player = c.COMPUTER
            earlier_player = c.HUMAN
        elif depth % 2 == 1:
            player = c.HUMAN
            earlier_player = c.COMPUTER

        winning = self.actual_tie.check_winning(move_i, move_j, self.board_copy,
                                                earlier_player)
        draw = self.actual_tie.check_draw(self.board_copy)
        if winning or draw or depth == c.MAX_DEPTH:
            score = self.score_in_alfa_beta(move_i, move_j, depth, winning, draw)
            return score

        if player == c.COMPUTER:
            value = -math.inf
            for i, j in self.get_empty_fields(1, move_i, move_j):
                self.board_copy[i][j] = player
                value = self.alfa_beta(alfa, beta, i, j, depth + 1)
                self.board_copy[i][j] = None
                if value > alfa:
                    alfa = value
                if alfa >= beta:
                    return beta
            return alfa
        if player == c.HUMAN:
            value = math.inf
            for i, j in self.get_empty_fields(1, move_i, move_j):
                self.board_copy[i][j] = player
                value = self.alfa_beta(alfa, beta, i, j, depth + 1)
                self.board_copy[i][j] = None
                if value < beta:
                    beta = value
                if alfa >= beta:
                    return alfa
            return beta
        return None


if __name__ == "__main__":
    print("You should run gomoku.py file")
