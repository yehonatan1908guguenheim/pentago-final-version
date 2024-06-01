from state import state
import pygame
from constants import *
import numpy as np
pygame.init()

class Graphics:
    def __init__(self,initial_state:state = None):
        #main "board" array representation
        # self.Board=initial_state.Board
        # self.player=initial_state.player

        # initialize pygame
        pygame.init()
        pygame.display.set_caption('pentago :)')
        self.win=pygame.display.set_mode((WIDTH,HEIGHT))
    
    def draw(self,state: state):
        self.draw_grid()
        self.draw_all_pieces(state)
        # pygame.display.update()
    
    def draw_grid(self):
        
        self.win.fill(WHITE)
        self.grid_size=(COLS*100,ROWS*100)  
       # draw the background
        self.win.fill(RED)
         # Outer lines in black 
        pygame.draw.rect(self.win, WHITE, (0, 0, WIDTH, HEIGHT), 5)
        # Grid inner lines 
        for i in range(self.grid_size[0] + 1):
            x = i * SQUARE_SIZE
            pygame.draw.line(self.win, WHITE, (x, 0), (x, HEIGHT))

        for j in range(self.grid_size[1] + 1) :
            y = j * SQUARE_SIZE
            pygame.draw.line(self.win, WHITE, (0, y), (WIDTH, y))
        # update the screen
        pygame.display.update()
    

    def draw_all_pieces(self, state:state):
        copyarray= state.Board
        row=0
        col=0
        for i in copyarray:
            for j in i:
                col+=1
                self.draw_piece((row, col), j)
            col=0
            row+=1

    def draw_piece(self, row_col, player):
        center = self.calc_pos(row_col)
        radius = (SQUARE_SIZE) // 2 - PADDING
        color = self.calc_color(player)
        if color != RED:
            pygame.draw.circle(self.win, LIGHT_GRAY, center, radius*0.5 -2)
        pygame.draw.circle(self.win,color , center, radius*0.5)

    def calc_pos(self, row_col):
        row, col = row_col
        y = row * SQUARE_SIZE + SQUARE_SIZE//2
        x = col * SQUARE_SIZE + SQUARE_SIZE//2
        return x-100, y

    # def calc_base_pos(self, row_col):
    #     row, col = row_col
    #     y = row * SQUARE_SIZE
    #     x = col * SQUARE_SIZE
    #     return x, y

    def calc_row_col(self, pos):
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return row, col
    
    def calc_color(self, player):
        if player == 1:
            return WHITE
        elif player == -1:
            return BLACK
        else:
            return RED
    
    # def draw_square(self, row_col, color):
    #     pos = self.calc_base_pos(row_col)
    #     pygame.draw.rect(self.win, color, (*pos, SQUARE_SIZE, SQUARE_SIZE))

