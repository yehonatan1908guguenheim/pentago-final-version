from state import state
from environment import puzzle
from constants import *
import numpy as np
from graphics import Graphics
class ABA2:
    
    def __init__(self,depth:int=2,c:puzzle=None,player=1) -> None:
        self.player=player
        self.opponent=(-self.player)
        self.depth=depth
        self.environment=c.copy()
    
    def get_Action(self, events=None, state:state=None , graphics:Graphics=None):
        visited = set()
        value, bestAction = self.minMax(state, visited)
        return bestAction
    
    def evaluate (self, gameState : state):
        score =  0
        b=gameState.Board.copy()
        #gives extra points if there is a player in the center
        for i in range(5):
            if b[1,i]==self.player:
                score +=1
                if b[4,i]==self.player:
                    score+=1
                elif b[4,i]==self.opponent:
                    score-=1
            elif b[1,i]==self.opponent:
                score-=1
                if b[4,i]==self.player:
                    score+=1
                elif b[4,i]==self.opponent:
                    score-=1
            if b[i,1]==self.player:
                score +=1
                if b[i,4]==self.player:
                    score+=1
                elif b[i,4]==self.opponent:
                    score-=1
            elif b[i,1]==self.opponent:
                score-=10
                if b[i,4]==self.player:
                    score+=1
                elif b[i,4]==self.opponent:
                    score-=1
        return score
    def minMax(self, state:state, visited:set):
        depth = 0
        alpha = -MAXSCORE
        beta = MAXSCORE
        return self.max_value(state, visited, depth, alpha, beta)
    
    def max_value (self, state:state, visited:set, depth, alpha, beta):
        
        value = -MAXSCORE

        # stop state
        if depth == self.depth or self.environment.is_winning_state(state):
            value = self.evaluate(state )
            return value, None
        
        # start recursion
        bestAction = None
        legal_actions = self.environment.get_legal_actions(state)
        for action in legal_actions:
            newState = self.environment.get_next_state(action, state)
            if newState not in visited:
                visited.add(newState)
                newValue, newAction = self.min_value(newState, visited,  depth + 1, alpha, beta)
                if newValue > value:
                    value = newValue
                    bestAction = action
                    alpha = max(alpha, value)
                if value >= beta:
                    return value, bestAction
                    

        return value, bestAction 

    def min_value (self, state:state, visited:set, depth, alpha, beta):
        
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
                visited.add(newState)
                newValue, newAction = self.max_value(newState, visited,  depth + 1, alpha, beta)
                if newValue < value:
                    value = newValue
                    bestAction = action
                    beta = min(beta, value)
                if value <= alpha:
                    return value, bestAction

        return value, bestAction 
