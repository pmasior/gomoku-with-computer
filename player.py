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


    def move(self):
        board_copy = copy.deepcopy(self.tie.board)
        self.find_move(board_copy)
        x = GRID_X_BEGIN + self.next_move_n * GRID_TILESIZE
        y = GRID_Y_BEGIN + self.next_move_m * GRID_TILESIZE
        self.write_move(self.next_move_n, self.next_move_m)
        self.draw_move(x, y)
        return self.next_move_n, self.next_move_m


    # def get_empty_fields(self, board_copy):
    #     """ Zwraca tablicę ze współrzędnymi pustych pól """
    #     return [(i, j) for i in range(FIELDS) for j in range(FIELDS) if self.check_if_field_is_empty(i, j, board_copy)]


    def get_empty_and_near_stones_fields(self, board_copy):
        """ Zwraca tablicę ze współrzędnymi pustych pól otorzonych kamieniami

        Funkcja pozwala na zmiejszenie liczby obliczeń podczas wyznaczania
        pól, które mogą być propozycjami kolejnych ruchów komputera.
        Zastępuje funkcję zwracającą tablicę ze współrzędnymi pustych pól
        """
        fields = set()
        for i in range(FIELDS):
            for j in range(FIELDS):
                if self.check_if_field_is_empty(i, j, board_copy) == False:
                    self.add_empty_fields_to_set(board_copy, i, j, fields)
        return fields


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


    def add_empty_fields_to_set(self, board_copy, n, m, fields, area = 1):  # area 1 lub 3 lub 4
        left, top, right, bottom = \
            self.improve_range_of_array(board_copy, n - area, n + area, m - area, m + area)
        for i in range(left, right + 1):
            for j in range(top, bottom + 1):
                if self.check_if_field_is_empty(i, j, board_copy):
                    # print("(", i, ", ", j, ")", sep = '', end = '')  # DEBUG:
                    fields.add((i, j))


    def score_in_alfa_beta(self, board_copy, depth, winner, draw):
        if depth % 2 == 0:
            earlier_player = HUMAN
        elif depth % 2 == 1:
            earlier_player = COMPUTER

        if earlier_player == HUMAN and winner == True:
            return depth - 100
        elif earlier_player == COMPUTER and winner == True:
            return 100 - depth
        else:
            return 0


    def find_move(self, board_copy):
        """ Wybiera następny ruch komputera

        Wykorzystuje pętlę algorytmu minimax dla gracza MAX, żeby wyznaczyć
        następny ruch komputera, który zostaje zapisany jako atrybut klasy
        Computer
        """
        alfa = -math.inf
        for empty_field in self.get_empty_and_near_stones_fields(board_copy):
            n, m = empty_field
            board_copy[n][m] = COMPUTER
            value = self.alfa_beta(board_copy, alfa, math.inf, n, m, 1)
            board_copy[n][m] = None
            if value > alfa:
                alfa = value
                self.next_move_n, self.next_move_m = n, m
        # if value == 0 or -math.inf or math.inf:
        #     print("LOSOWANIE wyłączone")  # DEBUG:
            # randoms = self.get_empty_and_near_stones_fields(board_copy)
            # print("find_move() randoms", randoms)  # DEBUG:
            # self.next_move_n, self.next_move_m = random.choice(tuple(randoms))


    def alfa_beta(self, board_copy, alfa, beta, n = None, m = None, depth = 0):
        """ Alfa-beta z heurystyką zabójcy

        Argumenty:
        board_copy -- tablica z aktualnymi ruchami graczy
        alfa -- największa wartość dla gracza MAX (komputera)
        beta -- najmniejsza wartość dla gracza MIN (człowiek)
        n -- współrzędne ostatniego ruchu (istotne w dalszych wywołaniach rek.)
        m -- współrzędne ostatniego ruchu (istotne w dalszych wywołaniach rek.)
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
        if winner == True or draw == True or depth == MAX_DEPTH:
            score = self.score_in_alfa_beta(board_copy, depth, winner, draw)
            # print("ab+() d", depth, " v", score, " n", n, " m", m, " p", player, "ep", earlier_player, sep='')  # DEBUG:
            return score

        if player == COMPUTER:
            for empty_field in self.get_empty_and_near_stones_fields(board_copy):
                if self.next_move_beta_n == None and self.next_move_beta_m == None:
                    n, m = empty_field
                if self.next_move_beta_n != None and self.next_move_beta_m != None:
                    n, m = self.next_move_beta_n, self.next_move_beta_m
                board_copy[n][m] = player
                value = self.alfa_beta(board_copy, alfa, beta, n, m, depth + 1)
                # print("ab ()", " v", value, " n", n, " m", m, " p", player, " d", depth,  sep='')  # DEBUG:
                board_copy[n][m] = None
                if self.next_move_beta_n != None and self.next_move_beta_m != None:
                    self.next_move_beta_n, self.next_move_beta_m = None, None
                if value > alfa:
                    alfa = value
                if alfa >= beta:
                    # print("ifβ", "*" * depth, beta)  # DEBUG:
                    self.next_move_beta_n = n
                    self.next_move_beta_m = m
                    return beta
            # print("if ", "*" * depth, alfa)  # DEBUG:
            return alfa
        elif player == HUMAN:
            for empty_field in self.get_empty_and_near_stones_fields(board_copy):
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
            # print("if ", "*" * depth, beta)  # DEBUG:
            return beta



if __name__ == "__main__":
    print("You should run gomoku.py file")
