#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import pygame
import math
import random
import copy

from constants import *
from develop import *
from stone import *


class Player():
    def __init__(self, screen, tie, number, color):
        self.screen = screen
        self.tie = tie
        self.number = number
        self.color = color
        self.stone_sprites = pygame.sprite.Group()


    def check_if_field_is_empty(self, n, m, board):
        if board[n][m] == None:
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
                if self.check_if_clicked_in_field(x, y, mouse_x, mouse_y) and \
                   self.check_if_field_is_empty(n, m, self.tie.board):
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


    def new_get_empty_fields(self, board_copy, last_move_n = None, last_move_m = None, area = 1):
        """ Zwraca listę pustych pól

        Najpierw tworzy zbiór pustych pól wokół ostatniego ruchu człowieka,
        potem tworzy nowy zbiór pustych pól wokól wszystkich kamieni na planszy.
        Dzięki temu dostarcza funkcji alfa_beta() ...
        """
        empty_fields = list()
        near_empty_fields = set()
        rest_empty_fields = set()
        for i in range(FIELDS):
            for j in range(FIELDS):
                if board_copy[i][j] != None:
                    near_empty_fields |= self.empty_fields_around(board_copy, i, j, area)
                    # near_empty_fields.update(self.empty_fields_around(board_copy, i, j))
                # elif board_copy[i][j] == None:
                #     rest_empty_fields.add((i, j))

        if last_move_n != None or last_move_m != None:
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


    # def new_check_if_near_stones(self, board_copy, n, m, area = 1):
    #     small_board = [row[n-area, n+area+1] for row in board_copy[m-area, m+area+1]]
    #     amount_of_1 = sum(row.count(HUMAN) for row in small_board)
    #     amount_of_2 = sum(row.count(COMPUTER) for row in small_board)
    #     if amount_of_1 + amount_of_2 > 0:
    #         return True
    #     else:
    #         return False


    def score_in_alfa_beta(self, board_copy, n, m, depth, winner, draw):
        if depth % 2 == 0:
            earlier_player = HUMAN
        elif depth % 2 == 1:
            earlier_player = COMPUTER

        if earlier_player == HUMAN and winner == True:
            return depth - 100
        elif earlier_player == COMPUTER and winner == True:
            return 100 - depth

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
                human = tab[i:i+6].count(HUMAN)
                computer = tab[i:i+6].count(COMPUTER)
                none_s = tab[i:i+6].count(None)
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

                if me_s == 4 and (tab[i] == None or tab[-1] == None):
                    score = max(score, 80)
                elif me_s == 4 and none_s == 2:
                    score = max(score, 70)
                elif me_s == 4 and ((tab[i] == opponent_n) != (tab[-1] == opponent_n)) and none_s == 1:  # != xor
                    score = max(score, 70)
                elif me_s == 3 and (tab[i] == None and tab[-1] == None) and none_s == 3:
                    score = max(score, 60)
                elif me_s == 3 and ((tab[i] == opponent_n) != (tab[-1] == opponent_n)) and none_s == 2:
                    score = max(score, 50)
                elif me_s == 3 and ((tab[i] == None) != (tab[-1] == None)) and none_s == 3:
                    score = max(score, 50)
                elif me_s == 2 and none_s == 4 and tab[i] == tab[i+1] == tab[i+4] == tab[i+5] == None:
                    score = max(score, 40)
                elif me_s == 2 and none_s == 3 and ((tab[i] == opponent_n) != (tab[-1] == opponent_n)):
                    score = max(score, 30)
                elif me_s == 1 and none_s == 5:
                    score = max(score, 20)
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
        #     self.new_get_empty_fields(board_copy, last_move_n, last_move_m)
        empty_fields = self.new_get_empty_fields(board_copy, last_move_n, last_move_m, 1)
        # for empty_field in last_move_near_empty_fields:
        for empty_field in empty_fields:
            n, m = empty_field
            board_copy[n][m] = COMPUTER
            value = self.alfa_beta(board_copy, alfa, math.inf, n, m, 1)
            board_copy[n][m] = None
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

        winner = self.tie.check_winner(n, m, board_copy, earlier_player)
        draw = self.tie.check_draw(board_copy)
        # print("depth", depth)  # DEBUG:
        if winner == True or draw == True or depth == MAX_DEPTH:
            score = self.score_in_alfa_beta(board_copy, n, m, depth, winner, draw)
            # print("ab+() d", depth, " v", score, " n", n, " m", m, " p", player, "ep", earlier_player, sep='')  # DEBUG:
            return score

        if player == COMPUTER:
            value = -math.inf
            for empty_field in self.new_get_empty_fields(board_copy):
                n, m = empty_field
                board_copy[n][m] = player
                value = self.alfa_beta(board_copy, alfa, beta, n, m, depth + 1)
                # print("ab ()", " v", value, " n", n, " m", m, " p", player, " d", depth,  sep='')  # DEBUG:
                board_copy[n][m] = None
                if value > alfa:
                    alfa = value
                if alfa >= beta:
                    # print("ifβ", "*" * depth, beta)  # DEBUG:
                    return beta
                    # break
            # print("if ", "*" * depth, alfa)  # DEBUG:
            return alfa
        elif player == HUMAN:
            value = math.inf
            for empty_field in self.new_get_empty_fields(board_copy):
                n, m = empty_field
                board_copy[n][m] = player
                value = self.alfa_beta(board_copy, alfa, beta, n, m, depth + 1)
                # print("ab ()", " v", value, " n", n, " m", m, " p", player, " d", depth,  sep='')  # DEBUG:
                board_copy[n][m] = None
                if value < beta:
                    beta = value
                if alfa >= beta:
                    # print("ifα", "*" * depth, alfa)  # DEBUG:
                    return alfa
                    # break
            # print("if ", "*" * depth, beta)  # DEBUG:
            return beta



if __name__ == "__main__":
    print("You should run gomoku.py file")
