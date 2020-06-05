#!/usr/bin/env python3
"""Funkcje do zapisywania logów"""

import constants as c


def init_debug_file():
    """Czyści plik używany do zapisywania logów."""
    file = open("resgom.txt", "w")
    file.write(" ")
    file.close()


def print_board(board, tekst="default"):
    """Wypisuje stan tablicy board[] do pliku."""
    if c.LOG_TO_FILE == 0:
        print("\n print_board()", tekst)
        for j in range(c.FIELDS):
            for i in range(c.FIELDS):
                if board[i][j] is not None:
                    print(board[i][j], end=' ')
                else:
                    print("░", end=' ')
            print()
    elif c.LOG_TO_FILE == 1:
        file = open("resgom.txt", "a")
        file.write(f"\n print_board() {tekst}\n")
        for j in range(c.FIELDS):
            for i in range(c.FIELDS):
                if board[i][j] is not None:
                    file.write(str(board[i][j]))
                    file.write(" ")
                else:
                    file.write("░")
                    file.write(" ")
            file.write("\n")
        file.close()



if __name__ == "__main__":
    print("You should run gomoku.py file")
