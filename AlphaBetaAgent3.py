from state import state
from environment import puzzle
from constants import *
import numpy as np
from graphics import Graphics
class ABA3:
    
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
        player=[0]
        opponent=[0]
        i=2
        while i<=5:
            player.append(self.has_n_streak(gameState,i,self.player))
            opponent.append(self.has_n_streak(gameState,i,-self.player))
            i+=1
        
        for i in range(2,5):
            score+=i*(player[i]-opponent[i])*10
        for i in range(6):
            score+=np.sum(b[i])
            score+=np.sum(b[0:6,i])    
        
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
    
    def has_n_streak(self, sta: state, t: int,player:int):
        counter=0
        z=0
        for row in sta.Board:
            count = 1
            prev = row[0]
            for val in row[1:]:
                if val == prev and val!=0:
                    count += 1
                    if count == t:
                        counter+=1
                else:
                    count = 1
                    prev = val

        # Check columns
        for j in range(t):
            count = 1
            prev = sta.Board[0][j]
            for i in range(1, t):
                val = sta.Board[i][j]
                if val == prev and val!=0:
                    count += 1
                    if count == t:
                        counter+=1
                else:
                    count = 1
                    prev = val

        #check diagonals
        n = len(sta.Board)
        # check the diagonal from top-left to bottom-right
        for i in range(t - 4):
            for j in range(t - 4):
                if sta.Board[i][j]!=0 and sta.Board[i][j] == sta.Board[i+1][j+1] == sta.Board[i+2][j+2] == sta.Board[i+3][j+3] == sta.Board[i+4][j+4]  :
                    counter+=1

        # check the diagonal from bottom-left to top-right
        for i in range(t - 4):
            for j in range(4, t):
                if sta.Board[i][j]!=0 and sta.Board[i][j] == sta.Board[i+1][j-1] == sta.Board[i+2][j-2] == sta.Board[i+3][j-3] == sta.Board[i+4][j-4] :
                    counter+=1
        # No n-streak found
        return counter

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
