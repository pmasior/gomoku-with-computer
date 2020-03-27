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


if __name__ == "__main__":
    print("You should run gomoku.py file")
