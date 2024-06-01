from environment import puzzle
from state import state
from constants import *
import numpy
import random
from graphics import Graphics
class RA:
    def __init__(self,player=1,env:puzzle=None)-> None:
        self.player = player
        self.env = env 
        self.graphics = env.graphics
        #self.mode = 1  # 1 - get row_col; 2 - get: turn k
        
    
    def get_Action(self,events=None,gameState:state=None,graphics:Graphics=None):
        legal_actions = self.env.get_legal_actions(state=gameState)
        action = random.choice(legal_actions)
        return action