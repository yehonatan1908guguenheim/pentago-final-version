import numpy as np
import pygame as pg
from graphics import Graphics
import time
from constants import *
from state import state
 
from environment import puzzle 

class HumanAgent:
    def __init__(self, player: int, env : puzzle) -> None:
        self.player = player
        self.env = env
        self.graphics = env.graphics
        self.mode = 1  # 1 - get row_col; 2 - get: turn k
        self.row_col = None
        self.original_state = None

    def get_Action (self, events= None, gameState = None,graphics:Graphics=None)->list:
        
        for event in events:
            if self.mode == 1:
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    row_col = self.graphics.calc_row_col(pos)
                    if (self.env.islegal(row_col,self.env.state)):
                        self.original_state = self.env.state.copy()
                        self.env.insert(row_col,self.env.state,self.player)
                        self.env.graphics.draw(self.env.state)
                        self.mode = 2
                        self.row_col = row_col
                        
                    
            if self.mode==2:
                if event.type==pg.KEYDOWN:
                    
                    flag = False
                    turn = 0
                    match(event.key):
                        case pg.K_0:
                            flag = True
                            turn = 0
                        case pg.K_1:
                            flag = True
                            turn = 1
                        case pg.K_2:
                            flag=True
                            turn=2
                        case pg.K_3:
                            flag = True
                            turn = 3
                        
                    if flag:
                        self.mode = 1
                        self.env.state = self.original_state
                        return self.row_col[0],self.row_col[1], turn
                   
                    
        return None