#!/usr/bin/env python3
# -*- coding: utf_8 -*-

from constants import *

# grep -n 'if' resgom.txt
# grep '.*Tie' -A 15 "resgom9.txt"
# grep -n '1 1 1 1 1' resgom.txt
# grep -n 'END' resgom.txt && grep -n 'LOSOWANIE' resgom.txt && grep -n -m 1 'ab.() .* v[^0]' resgom.txt
# python3 gomoku.py > resgom.txt

def init_debug_file():
    file = open("resgom.txt", "w")
    file.write(" ")
    file.close()

def print_board(board, tekst = "default"):
    if LOG_TO_FILE == 0:
        print("\n print_board()", tekst)
        for m in range(0, FIELDS):
            for n in range(0, FIELDS):
                if board[n][m] != None:
                    print(board[n][m], end=' ')
                else:
                    print("░", end=' ')
            print()
    elif LOG_TO_FILE == 1:
        file = open("resgom.txt", "a")
        file.write("\n print_board()" + tekst + "\n")
        for m in range(0, FIELDS):
            for n in range(0, FIELDS):
                if board[n][m] != None:
                    file.write(str(board[n][m]))
                    file.write(str(" "))
                else:
                    file.write("░")
                    file.write(str(" "))
            file.write("\n")
        file.close()

def draw_move(self, x, y):
    pygame.draw.circle(self.game.screen, self.color, (x, y), STONE_RADIUS)



if __name__ == "__main__":
    print("You should run gomoku.py file")
