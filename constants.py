from os import path

TITLE = "Gomoku"
WIDTH = 800
HEIGHT = 800
FPS = 30

LIGHT_GRAY = (221, 221, 221)
DARK_GRAY = (136, 136, 136)
BLUE = (30, 101, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND = (219, 201, 180)

FIELDS = 16

GRID_MARGIN = 50
GRID_SIZE = 700
GRID_BEGIN = GRID_MARGIN
GRID_END = GRID_MARGIN + GRID_SIZE + 1
GRID_TILESIZE = GRID_SIZE // 14

STONE_RADIUS = 23

location_img = path.join(path.dirname(__file__), 'img')
IMG_WHITE_STONE = path.join(location_img, 'pieceWhite_border11.png')
IMG_BLACK_STONE = path.join(location_img, 'pieceBlack_border11.png')
