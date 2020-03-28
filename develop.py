#!/usr/bin/env python3
# -*- coding: utf_8 -*-

from constants import *

def print_board(board):
    print("\n print_board()")
    for m in range(0, FIELDS):
        for n in range(0, FIELDS):
            if board[n][m] != None:
                print(board[n][m], end=' ')
            else:
                print(" ", end=' ')
        print()

def draw_move(self, x, y):
    pygame.draw.circle(self.game.screen, self.color, (x, y), STONE_RADIUS)

def check_winner_diagonally2(self, n, m, r):
    print("d2", s1, s2, s3, s4, s5, "s06", s0, s6, "d2 n =", n, "m =", m, "n €", left, right, "m €", top, down)
    print("s1", "        ", right, top)
    print("s2", "      ", left + 3, top + 1)
    print("s3", "    ", left + 2, top + 2)
    print("s4", "  ", left + 1, top + 3)
    print("s5", "", left, down)


if __name__ == "__main__":
    print("You should run gomoku.py file")
