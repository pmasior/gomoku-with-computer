#!/usr/bin/env python3
"""Stałe w grze Gomoku"""

from os import path

TITLE = "Gomoku"
WIDTH = 800
HEIGHT = 850
FRAMES_PER_SECOND = 30

LOG_STATE_OF_BOARD = 0  # 0 - brak logów; 1 - logi z tie(); 2 - logi z alfa_beta()
    # !!! włączenie logów bardzo spowalnia działanie programu
LOG_TO_FILE = 0  # 0 - na konsolę; 1 - do pliku gomres.txt

COMPUTER_STONES_COLOR = (255, 255, 255)  # WHITE
GAME_BACKGROUND_COLOR = (115, 104, 85)  # DARK_SAND
GRID_COLOR = (177, 153, 115)  # SAND
HUMAN_STONES_COLOR = (33, 37, 43)  # DARK_GRAY
PROMPT_BACKGROUND_COLOR = (33, 37, 43)  # DARK_GRAY
PROMPT_TEXT_COLOR = (226, 192, 141)  # LIGHT_SAND

EMPTY = None
HUMAN = 1
COMPUTER = 2
PLAYER_DRAW = 3

FIELDS = 15
STONE_RADIUS = 23
MAX_DEPTH = 4  # zalecane: 4

GRID_MARGIN = 50
GRID_SIZE = 700
TOP_MARGIN = 50
GRID_X_BEGIN = GRID_MARGIN
GRID_X_END = GRID_MARGIN + GRID_SIZE + 1
GRID_Y_BEGIN = GRID_MARGIN + TOP_MARGIN
GRID_Y_END = GRID_MARGIN + GRID_SIZE + TOP_MARGIN + 1
GRID_TILESIZE = GRID_SIZE // (FIELDS - 1)

RANGE_OF_LINES_NEARBY_STONE = (-5, 6)
LINE_LENGTH_TO_CHECK = 6

LOCATION_IMG = path.join(path.dirname(__file__), 'img')
IMG_COMPUTER_STONE = path.join(LOCATION_IMG, 'pieceWhite_border11.png')
IMG_HUMAN_STONE = path.join(LOCATION_IMG, 'pieceBlack_border11.png')

LOCATION_FONT = path.join(path.dirname(__file__), 'font')
FONT_ICEBERG = path.join(LOCATION_FONT, 'Iceberg-Regular.ttf')



if __name__ == "__main__":
    print("You should run gomoku.py file")
