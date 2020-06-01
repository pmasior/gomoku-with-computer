#!/usr/bin/env python3

import pygame
import math
import random
import copy

from constants import *
from develop import *
from stone import *


class Player:
    def __init__(self, screen, tie, number, color):
        self.screen = screen
        self.tie = tie
        self.number = number
        self.color = color
        self.stone_sprites = pygame.sprite.Group()


    def check_if_field_is_empty(self, n, m, board):
        if board[n][m] is EMPTY:
            return True
        return False


    def write_move(self, n, m):
        self.tie.board[n][m] = self.number


    def draw_move(self, x, y):
        stone = Stone(self.color, x, y)
        self.tie.all_sprites.add(stone)
        self.stone_sprites.add(stone)



class Human(Player):
    def move(self, mouse_x, mouse_y):
        """ Sprawdza czy ruch jest dozwolony, jeśli jest to go wykonuje """
        for m in range(0, FIELDS):
            y = GRID_Y_BEGIN + m * GRID_TILESIZE
            for n in range(0, FIELDS):
                x = GRID_X_BEGIN + n * GRID_TILESIZE
                if (self.check_if_clicked_in_field(x, y, mouse_x, mouse_y) and 
                    self.check_if_field_is_empty(n, m, self.tie.board)):
                    self.write_move(n, m)
                    self.draw_move(x, y)
                    return n, m
        return None, None


    def check_if_clicked_in_field(self, x, y, mouse_x, mouse_y):
        if math.hypot(mouse_x - x, mouse_y - y) < STONE_RADIUS:
            return True
        return False



class Computer(Player):
    def __init__(self, screen, tie, number, color):
        super().__init__(screen, tie, number, color)
        self.next_move_n = None
        self.next_move_m = None
        self.next_move_beta_n = None
        self.next_move_beta_m = None


    def move(self, last_move_n, last_move_m):
        board_copy = copy.deepcopy(self.tie.board)
        self.find_move(board_copy, last_move_n, last_move_m)
        x = GRID_X_BEGIN + self.next_move_n * GRID_TILESIZE
        y = GRID_Y_BEGIN + self.next_move_m * GRID_TILESIZE
        self.write_move(self.next_move_n, self.next_move_m)
        self.draw_move(x, y)
        return self.next_move_n, self.next_move_m


    def get_empty_fields(self, board_copy, area = 1, last_move_n = None, last_move_m = None):
        """ Zwraca listę pustych pól

        Najpierw tworzy zbiór pustych pól wokół ostatniego ruchu człowieka,
        potem tworzy nowy zbiór pustych pól wokół wszystkich kamieni na planszy, 
        ale niezawierający pól z wcześniejszego zbioru.
        Dzięki temu dostarcza funkcji alfa_beta() w pierwszej kolejności pola,
        które mogą mieć największe znaczenie dla wygranej w grze.
        """
        empty_fields = list()
        near_empty_fields = set()
        rest_empty_fields = set()
        for i in range(FIELDS):
            for j in range(FIELDS):
                if board_copy[i][j] is not EMPTY:
                    near_empty_fields |= self.empty_fields_around(board_copy, i, j, area)
                # elif board_copy[i][j] is EMPTY:
                #     rest_empty_fields.add((i, j))

        if last_move_n is not None or last_move_m is not None:
            last_move_near_empty_fields = self.empty_fields_around(board_copy, last_move_n, last_move_m)
            empty_fields.extend(list(last_move_near_empty_fields))
            near_empty_fields -= last_move_near_empty_fields

        # rest_empty_fields -= near_empty_fields
        empty_fields.extend(list(near_empty_fields))
        empty_fields.extend(list(rest_empty_fields))
        # print("F", empty_fields)  # DEBUG:
        return empty_fields
        # return last_move_near_empty_fields, near_empty_fields, rest_empty_fields


    def empty_fields_around(self, board_copy, n, m, area = 1):  # area 1 lub 3 lub 4
        near_empty_fields = set()
        left, top, right, bottom = \
            self.improve_range_of_array(board_copy, n - area, n + area, m - area, m + area)
        for i in range(left, right + 1):
            for j in range(top, bottom + 1):
                if self.check_if_field_is_empty(i, j, board_copy):
                    # print("(", i, ", ", j, ")", sep = '', end = '')  # DEBUG:
                    near_empty_fields.add((i, j))
        return near_empty_fields


    def improve_range_of_array(self, board_copy, left, right, top, bottom):
        """ Zapewnia, że współrzędne nie wychodzą poza zakres tablicy """
        while left < 0:
            left += 1
        while top < 0:
            top += 1
        while right >= FIELDS:
            right -= 1
        while bottom >= FIELDS:
            bottom -= 1
        return left, top, right, bottom


    def score_in_alfa_beta(self, board_copy, n, m, depth, winning, draw):
        if depth % 2 == 0:
            earlier_player = HUMAN
        elif depth % 2 == 1:
            earlier_player = COMPUTER

        if winning and earlier_player == HUMAN:
            return depth - 100
        elif winning and earlier_player == COMPUTER:
            return 100 - depth
        # else:
        #     return 0

        horizontally = list()
        vertically = list()
        diagonally1 = list()
        diagonally2 = list()
        for i in range(-5, 5 + 1):
            if n + i >= 0 and n + i < FIELDS:
                horizontally.append(board_copy[n + i][m])
            if m + i >= 0 and m + i < FIELDS:
                vertically.append(board_copy[n][m + i])
            if n + i >= 0 and n + i < FIELDS and m + i >= 0 and m + i < FIELDS:
                diagonally1.append(board_copy[n + i][m + i])
            if n - i >= 0 and n - i < FIELDS and m + i >= 0 and m + i < FIELDS:
                diagonally2.append(board_copy[n - i][m + i])

        score = 0
        for tab in horizontally, vertically, diagonally1, diagonally2:
            for i in range(0, 5 + 1):
                line = tab[i:i+6]
                if len(line) == 6:
                    human = line.count(HUMAN)
                    computer = line.count(COMPUTER)
                    none_s = line.count(EMPTY)
                    if earlier_player == HUMAN:
                        me_s = human
                        opponent_s = computer
                        me_n = HUMAN
                        opponent_n = COMPUTER
                    elif earlier_player == COMPUTER:
                        me_s = computer
                        opponent_s = human
                        me_n = COMPUTER
                        opponent_n = HUMAN

                    if me_s == 4 and line[-2] == line[-1] is EMPTY:
                        score = max(score, 80)
                    elif me_s == 4 and line[0] == line[-1] is EMPTY:
                        score = max(score, 80)
                    elif me_s == 4 and line[0] == line[1] is EMPTY:
                        score = max(score, 80)
                    elif me_s == 4 and none_s == 2 and ((line[0] is EMPTY) != (line[-1] is EMPTY)):
                        score = max(score, 70)
                    elif me_s == 4 and none_s == 1 and ((line[0] == opponent_n) != (line[-1] == opponent_n)):
                        score = max(score, 70)
                    # elif line[0:3].count(me_n) == 3 and none_s == 3:
                    #     score = max(score, 60)
                    # elif line[1:4].count(me_n) == 3 and none_s == 3:
                    #     score = max(score, 60)
                    # elif line[2:5].count(me_n) == 3 and none_s == 3:
                    #     score = max(score, 60)
                    # elif line[3:6].count(me_n) == 3 and none_s == 3:
                    #     score = max(score, 60)
                    # elif me_s == 3 and none_s == 3 and line[0] == line[-1] is EMPTY:
                    #     score = max(score, 50)
                    # elif line[0:3].count(me_n) == 3 and none_s == 2 and line[0] == opponent_n:
                    #     score = max(score, 50)
                    # elif line[1:4].count(me_n) == 3 and none_s == 2 and ((line[0] == opponent_n) != (line[-1] == opponent_n)):
                    #     score = max(score, 50)
                    # elif line[2:5].count(me_n) == 3 and none_s == 2 and ((line[0] == opponent_n) != (line[-1] == opponent_n)):
                    #     score = max(score, 50)
                    # elif line[3:6].count(me_n) == 3 and none_s == 2 and line[-1] == opponent_n:
                    #     score = max(score, 50)
                    else:
                        score = max(score, 0)
                else:
                    score = max(score, 0)
        if earlier_player == HUMAN:
            return depth - score
        elif earlier_player == COMPUTER:
            return score - depth


    def find_move(self, board_copy, last_move_n, last_move_m):
        """ Wybiera następny ruch komputera

        Wykorzystuje pętlę algorytmu minimax dla gracza MAX, żeby wyznaczyć
        następny ruch komputera, który zostaje zapisany jako atrybut klasy
        Computer
        """
        alfa = -math.inf
        # last_move_near_empty_fields, near_empty_fields, rest_empty_fields = \
        #     self.get_empty_fields(board_copy, last_move_n, last_move_m)
        empty_fields = self.get_empty_fields(board_copy, 1, last_move_n, last_move_m)
        for empty_field in empty_fields:
            n, m = empty_field
            board_copy[n][m] = COMPUTER
            value = self.alfa_beta(board_copy, alfa, math.inf, n, m, 1)
            board_copy[n][m] = EMPTY
            if value > alfa:
                alfa = value
                self.next_move_n, self.next_move_m = n, m


    def alfa_beta(self, board_copy, alfa, beta, n = None, m = None, depth = 0):
        """ Alfa-beta z heurystyką zabójcy

        Argumenty:
        board_copy -- tablica z aktualnymi ruchami graczy
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
        Heurystyka zabójcy (ang. killer heuristic) polega na zapamiętywaniu
        ostatniego ruchu, który spowodował odcięcie gałęzi na określonej
        głębokości, a następnie sprawdzenie tego ruchu w pierwszej kolejności
        w kolejnych wywołaniach dla tej samej głębokości.
        """
        if LOG_STATE_OF_BOARD > 1:
            print_board(board_copy, "alfa_beta()")
        if depth % 2 == 0:
            player = COMPUTER
            earlier_player = HUMAN
        elif depth % 2 == 1:
            player = HUMAN
            earlier_player = COMPUTER

        winning = self.tie.check_winning(n, m, board_copy, earlier_player)
        draw = self.tie.check_draw(board_copy)
        # print("depth", depth)  # DEBUG:
        if winning or draw or depth == MAX_DEPTH:
            score = self.score_in_alfa_beta(board_copy, n, m, depth, winning, draw)
            # print("ab+() d", depth, " v", score, " n", n, " m", m, " p", player, "ep", earlier_player, sep='')  # DEBUG:
            return score

        if player == COMPUTER:
            value = -math.inf
            for empty_field in self.get_empty_fields(board_copy, 1):
                n, m = empty_field
                # if self.next_move_beta_n is not None and self.next_move_beta_m is not None:
                #     n, m = self.next_move_beta_n, self.next_move_beta_m
                board_copy[n][m] = player
                value = self.alfa_beta(board_copy, alfa, beta, n, m, depth + 1)
                # print("ab ()", " v", value, " n", n, " m", m, " p", player, " d", depth,  sep='')  # DEBUG:
                board_copy[n][m] = EMPTY
                if value > alfa:
                    alfa = value
                if alfa >= beta:
                    # print("ifβ", "*" * depth, beta)  # DEBUG:
                    # if value == 97:
                    #     self.next_move_beta_n, self.next_move_beta_m = n, m
                    # elif self.next_move_beta_n is not None and self.next_move_beta_m is not None:
                    #     self.next_move_beta_n, self.next_move_beta_m = None, None
                    return beta
                    # break
            # print("if ", "*" * depth, alfa)  # DEBUG:
            return alfa
        elif player == HUMAN:
            value = math.inf
            for empty_field in self.get_empty_fields(board_copy, 1):
                n, m = empty_field
                # if self.next_move_beta_n is not None and self.next_move_beta_m is not None:
                #     n, m = self.next_move_beta_n, self.next_move_beta_m
                board_copy[n][m] = player
                value = self.alfa_beta(board_copy, alfa, beta, n, m, depth + 1)
                # print("ab ()", " v", value, " n", n, " m", m, " p", player, " d", depth,  sep='')  # DEBUG:
                board_copy[n][m] = EMPTY
                if value < beta:
                    beta = value
                if alfa >= beta:
                    # print("ifα", "*" * depth, alfa)  # DEBUG:
                    # if value == -98:
                    #     self.next_move_beta_n, self.next_move_beta_m = n, m
                    # elif self.next_move_beta_n is not None and self.next_move_beta_m is not None:
                    #     self.next_move_beta_n, self.next_move_beta_m = None, None
                    return alfa
                    # break
            # print("if ", "*" * depth, beta)  # DEBUG:
            return beta



if __name__ == "__main__":
    print("You should run gomoku.py file")
