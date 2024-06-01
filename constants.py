import pygame


ROWS, COLS = 6,6
HEIGHT, WIDTH  = 600, 600
FRAME = 4
SQUARE_SIZE = 100
LINE_WIDTH = 2
PADDING = 2
RADIUS=(SQUARE_SIZE) // 4 - PADDING-2
MAXSCORE=1000
#RGB
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)

# epsilon Greedy
epsilon_start = 1
epsilon_final = 0.01
epsiln_decay = 500
