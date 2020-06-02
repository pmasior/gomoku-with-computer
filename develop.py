#!/usr/bin/env python3
"""Funkcje do zapisywania logów"""

# import pygame

import constants as c

# grep -n 'if' resgom.txt
# grep '.*Tie' -A 15 "resgom9.txt"
# grep -n '1 1 1 1 1' resgom.txt
# grep -n 'END' resgom.txt && grep -n 'LOSOWANIE' resgom.txt && grep -n -m 1 'ab.() .* v[^0]' resgom.txt
# python3 gomoku.py > resgom.txt

def init_debug_file():
    """Czyści plik używany do zapisywania logów."""
    file = open("resgom.txt", "w")
    file.write(" ")
    file.close()

def print_board(board, tekst="default"):
    """Wypisuje stan tablicy board[] do pliku."""
    if c.LOG_TO_FILE == 0:
        print("\n print_board()", tekst)
        for m in range(0, c.FIELDS): # pylint: disable=invalid-name
            for n in range(0, c.FIELDS): # pylint: disable=invalid-name
                if board[n][m] is not c.EMPTY:
                    print(board[n][m], end=' ')
                else:
                    print("░", end=' ')
            print()
    elif c.LOG_TO_FILE == 1:
        file = open("resgom.txt", "a")
        file.write(f"\n print_board() {tekst}\n")
        for m in range(0, c.FIELDS): # pylint: disable=invalid-name
            for n in range(0, c.FIELDS): # pylint: disable=invalid-name
                if board[n][m] is not c.EMPTY:
                    file.write(str(board[n][m]))
                    file.write(" ")
                else:
                    file.write("░")
                    file.write(" ")
            file.write("\n")
        file.close()



if __name__ == "__main__":
    print("You should run gomoku.py file")
