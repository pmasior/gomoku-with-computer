from os import path

TITLE = "Gomoku"
WIDTH = 800
HEIGHT = 800
FPS = 30

LIGHT_GRAY = (221, 221, 221)
DARK_GRAY = (33, 37, 43)
BLUE = (30, 101, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SAND = (226, 192, 141)
SAND = (177, 153, 115)
DARK_SAND = (115, 104, 85)

PLAYER_1 = 1
PLAYER_2 = 2
PLAYER_DRAW = 3

FIELDS = 16
STONE_RADIUS = 23

GRID_MARGIN = 50
GRID_SIZE = 700
GRID_BEGIN = GRID_MARGIN
GRID_END = GRID_MARGIN + GRID_SIZE + 1
GRID_TILESIZE = GRID_SIZE // 14

LOCATION_IMG = path.join(path.dirname(__file__), 'img')
IMG_WHITE_STONE = path.join(LOCATION_IMG, 'pieceWhite_border11.png')
IMG_BLACK_STONE = path.join(LOCATION_IMG, 'pieceBlack_border11.png')

LOCATION_FONT = path.join(path.dirname(__file__), 'font')
FONT_ICEBERG = path.join(LOCATION_FONT, 'Iceberg-Regular.ttf')


if __name__ == "__main__":
    print("You should run gomoku.py file")
