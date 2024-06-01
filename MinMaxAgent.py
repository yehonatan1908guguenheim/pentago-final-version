from environment import puzzle
from state import state
from constants import *
import numpy
from graphics import Graphics
class MMA:
    def __init__(self,depth:int=2,c:puzzle=None,player=1) -> None:
        self.player=player
        self.opponent=(-self.player)
        self.depth=depth
        self.environment=c.copy()

    def evaluate (self, gameState : state):
        score =  0
        b=gameState.Board.copy()
        player=[0]
        opponent=[0]
        i=2
        while i<=4:
            player.append(self.has_n_streak(gameState,i,self.player))
            opponent.append(self.has_n_streak(gameState,i,(-self.player)))
            i+=1
        for i in range(1,len(player)):
            score+=(i)*10*player[i]
            score-=i*10*player[i]
        #gives extra points if there is a player in the center
        for i in range(5):
            if b[1,i]==self.player:
                score +=10
                if b[4,i]==self.player:
                    score+=10
                elif b[4,i]==self.opponent:
                    score-=10
            elif b[1,i]==self.opponent:
                score-=10
                if b[4,i]==self.player:
                    score+=10
                elif b[4,i]==self.opponent:
                    score-=10
        for i in range(5):
            if b[i,1]==self.player:
                score +=10
                if b[i,4]==self.player:
                    score+=10
                elif b[i,4]==self.opponent:
                    score-=10
            elif b[i,1]==self.opponent:
                score-=10
                if b[i,4]==self.player:
                    score+=10
                elif b[i,4]==self.opponent:
                    score-=10
        return score
    def has_n_streak(self, sta: state, n: int,player:int):
        counter=0
        z=0
        # Check rows
        while(z<6):
            for row in sta.Board:
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
            for j in range(len(sta.Board[0])):
                count = 1
                prev = sta.Board[0][j]
                for i in range(1, len(sta.Board)):
                    val = sta.Board[i][j]
                    if val == prev== player:
                        count += 1
                        if count == n:
                            counter+=1
                    else:
                        z+=1
                        count = 1
                        prev = val

        # # Check diagonals

        # board_size = len(sta.Board)
        # # Check the diagonal from top-left to bottom-right
        # z=0
        # while(z<6):
        #     for i in range(board_size - n + 1):
        #         count=1
        #         for j in range(board_size - n + 1):
        #             is_streak = True
        #             for k in range(n):
        #                 if sta.Board[i+k][j+k]==player==sta.Board[i + k + 1][j + k + 1]:
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
        #                 if sta.Board[i + k][j - k] == sta.Board[i + k + 1][j - k - 1]==player:
        #                     count+=1
        #                     if count==n:
        #                         z+=n
        #                         counter+=1
        #                     else:
        #                         z+=1

        # No n-streak found
        return counter

    def get_Action(self, events=None, gameState:state=None , graphics:Graphics=None):
        reached = list()
        value, bestAction = self.minMax(gameState, reached, 0)
        return bestAction

    def minMax(self, gameState:state, reached:list, depth):
        if self.player == gameState.player:
            value = -MAXSCORE
        else:
            value = MAXSCORE

        # stop state
        if depth == self.depth or self.environment.is_winning_state(gameState):
            value = self.evaluate(gameState)
            return value, None
        
        # start recursion
        bestAction = None
        legal_actions = self.environment.get_legal_actions(gameState)
        for action in legal_actions:
            newGameState = self.environment.get_next_state(action, gameState)
            b=True
            for i in reached:
                if newGameState.__eq__(i):
                    b=False
                    
            if b:
                reached.append(newGameState)
                if self.player == gameState.player:         # maxNode - agent
                    newValue, newAction = self.minMax(newGameState, reached,  depth + 1)
                    if newValue > value:
                        value = newValue
                        bestAction = action
                else:                       # minNode - opponent
                    newValue, newAction = self.minMax(newGameState, reached,  depth + 1)
                    if newValue < value:
                        value = newValue
                        bestAction = action

        return value, bestAction 