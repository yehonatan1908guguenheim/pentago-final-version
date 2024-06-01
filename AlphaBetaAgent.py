from state import state
from environment import puzzle
from constants import *
import numpy as np
from graphics import Graphics
class ABA:
    
    def __init__(self,depth:int=3,c:puzzle=None,player=1) -> None:
        self.player=player
        self.opponent=(-self.player)
        self.depth=depth
        self.environment=c.copy()
    
    def get_Action(self, events=None, gameState:state=None , graphics:Graphics=None):
        visited = dict()
        value, bestAction = self.minMax(gameState, visited)
        return bestAction
    
    def evaluate (self, gameState : state):
        b=gameState.copy()
        return 1000*((self.has_n_streak(gameState,3,gameState.player)-self.has_n_streak(gameState,3,-gameState.player))+(self.has_n_streak(gameState,4,gameState.player)-self.has_n_streak(gameState,4,-gameState.player)))
    
    def has_n_streak(self, sta: state, n: int,player:int):
        counter=0
        z=0
        board=sta.Board.copy()
        # Check rows
        while(z<6):
            for row in board:
                count = 1
                prev = row[0]
                for val in row[1:]:
                    if val == prev== player:
                        count += 1
                        if count == n:
                            counter+=1
                            z+=n
                    else:
                        z+=1
                        count = 1
                        prev = val

        # Check columns
        z=0
        while(z<6):
            for j in range(len(board)):
                count = 1
                prev = board[0][j]
                for i in range(1, len(board)):
                    val = board[i][j]
                    if val == prev== player:
                        count += 1
                        if count == n:
                            counter+=1
                    else:
                        z+=1
                        count = 1
                        prev = val

        # # Check diagonals

        board_size = len(board)
        # # Check the diagonal from top-left to bottom-right
        # z=0
        # while(z<6):
        #     for i in range(board_size - n + 1):
        #         count=1
        #         for j in range(board_size - n + 1):
        #             is_streak = True
        #             for k in range(n):
        #                 if board[i+k][j+k]==player==board[i + k + 1][j + k + 1]:
        #                     count+=1
        #                     if count==n:
        #                         z+=n
        #                         counter+=1
        #                     else:
        #                         z+=1

        # # Check the diagonal from bottom-left to top-right
        # z=0
        # while(z<6):
        #     for i in range(board_size - n + 1):
        #         for j in range(n - 1, board_size):
        #             is_streak = True
        #             for k in range(n):
        #                 if board[i + k][j - k] == board[i + k + 1][j - k - 1]==player:
        #                     count+=1
        #                     if count==n:
        #                         z+=n
        #                         counter+=1
        #                     else:
        #                         z+=1

        # No n-streak found
        return counter*n

    def minMax(self, state:state, visited:dict):
        depth = 0
        alpha = -MAXSCORE
        beta = MAXSCORE
        return self.max_value(state, visited, depth, alpha, beta)
    
    def max_value (self, state:state, visited:dict, depth, alpha, beta):
        
        value = -MAXSCORE

        # stop state
        if depth == self.depth or self.environment.is_winning_state(state):
            value = self.evaluate(state)
            return value, None
        
        # start recursion
        bestAction = None
        legal_actions = self.environment.get_legal_actions(state)
        for action in legal_actions:
            newState = self.environment.get_next_state(action, state)
            if newState not in visited:
                visited[newState]=value
                newValue, newAction = self.min_value(newState, visited,  depth + 1, alpha, beta)
                if newValue > value:
                    value = newValue
                    bestAction = action
                    alpha = max(alpha, value)
                if value >= beta:
                    return value, bestAction
                    

        return value, bestAction 

    def min_value (self, state:state, visited:dict, depth, alpha, beta):
        
        value = MAXSCORE

        # stop state
        if depth == self.depth or self.environment.is_winning_state(state):
            value = self.evaluate(state)
            return value, None
        
        # start recursion
        bestAction = None
        legal_actions = self.environment.get_legal_actions(state)
        for action in legal_actions:
            newState = self.environment.get_next_state(action, state)
            if newState not in visited:
                visited[newState]=value
                newValue, newAction = self.max_value(newState, visited,  depth + 1, alpha, beta)
                if newValue < value:
                    value = newValue
                    bestAction = action
                    beta = min(beta, value)
                if value <= alpha:
                    return value, bestAction

        return value, bestAction 
