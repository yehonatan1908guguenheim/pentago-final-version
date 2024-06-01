import numpy as np
from constants import *
from state import state
import numpy as np
import random
from graphics import Graphics
import torch
class puzzle:
    def __init__(self,g:Graphics=None) -> None:
        self.state=self.get_init_state((ROWS,COLS))
        self.graphics=g
        self.won=0
        self.score=0
    
    def get_init_state(self,Rows_Cols):
        rows, cols = Rows_Cols
        board = np.zeros([rows, cols],int)

        return state (board, 1)
     
    def square_num(self,num:int):#gets a square num and returns the (0,0) of the pivot for turning
        start_index=(0,0)
        if num==2:
            start_index=(0,3)
        elif num==3:
            start_index=(3,0)
        elif num==4:
            start_index=(3,3)
        return start_index
    
    def is_winning_state(self,state:state):#checks if a streak of five identical cirlces apears , if so return  true and stop the game
        a=self.has_five_streak(state)
        if a[1]==1:
            self.won= 1
        elif a[1]==-1:
            self.won= 2
        return a[0]
        
    def who_won(self):# returns which player won 1=white 2=black
        return self.won
        
    def has_five_streak(self,sta:state):#checks for a five streak , horizontaly diaganly and y: return (true/false,(1,2)/false)בהתאמה לתוצאות הבדיקה
        #Check rows
        for row in sta.Board:
            count = 1
            prev = row[0]
            for val in row[1:]:
                if val == prev and val!=0:
                    count += 1
                    if count == 5:
                        return (True,val)
                else:
                    count = 1
                    prev = val

        # Check columns
        for j in range(len(sta.Board[0])):
            count = 1
            prev = sta.Board[0][j]
            for i in range(1, len(sta.Board)):
                val = sta.Board[i][j]
                if val == prev and val!=0:
                    count += 1
                    if count == 5:
                        return (True,val)
                else:
                    count = 1
                    prev = val

        # #check diagonals
        # n = len(sta.Board)
        # # check the diagonal from top-left to bottom-right
        # for i in range(n - 4):
        #     for j in range(n - 4):
        #         if sta.Board[i][j]!=0 and sta.Board[i][j] == sta.Board[i+1][j+1] == sta.Board[i+2][j+2] == sta.Board[i+3][j+3] == sta.Board[i+4][j+4]  :
        #             return (True,sta.Board[i][j])

        # # check the diagonal from bottom-left to top-right
        # for i in range(n - 4):
        #     for j in range(4, n):
        #         if sta.Board[i][j]!=0 and sta.Board[i][j] == sta.Board[i+1][j-1] == sta.Board[i+2][j-2] == sta.Board[i+3][j-3] == sta.Board[i+4][j-4] :
        #             return (True,self.state.Board[i+4][j-4])
        # No five in a row or column found
        return (False,False)
    
    def insert(self,row_col,sta:state,player):#inserts the actual new circle and prints out the new board
        row,col=row_col
        if self.islegal(row_col,sta): 
            sta.Board[row][col]=player
            return True
        else:
            return False
    
    def init_legal(self):
        pos=tuple()
        legal_pos=[]
        for i in range(6):
            for j in range(6):
                pos=(i,j)
                legal_pos.append(pos)
                
        return legal_pos
    
    def islegal(self,row_col,sta:state):#checks if the cell in the board/array is empty (equals 0)
        x,y=row_col
        return (sta.Board[x,y]==0)
    
    def switch_player(self):#switches the current player -> switch_player(1)=-1 and switch_player(-1)=1 ,switch_player(n)=-n,for all n in the neturals
        self.state.player=(-self.state.player)
    
    def move(self,action,state:state,player):
        row,col,turn=action
        row_col=row,col
        #print(row_col)
        #print(turn)
        self.insert(row_col,state,player)
        self.turn_square(row_col,state,turn)
        #state.player = state.c()

    def turn_square(self,row_col,state:state=None,turn:int=1):#rotates a 3 by 3 part of the array 
        """
        Rotate a 2D matrix 90 degrees clockwise
        """


        pos=self.Pos_2_Num(row_col)
        if pos== 1:
                state.Board[0:3,0:3]=np.rot90(state.Board[0:3,0:3].copy(),k=-1*turn)
        if pos== 3:
                state.Board[0:3,3:]=np.rot90(state.Board[0:3,3:].copy(),k=-1*turn)
                
        if pos== 2:
                state.Board[3:,0:3]=np.rot90(state.Board[3:,0:3].copy(),k=-1*turn)
                
        if pos == 4:
                state.Board[3:,3:]=np.rot90(state.Board[3:,3:].copy(),k=-1*turn)
                
    def isEndState(self,state:state=None):
        if not state:
            return False
        if (len(np.where(state.Board==0)[0])==0 and len(np.where(state.Board==0)[1])==0) or self.is_winning_state(state=state):
            return True
        
    def get_next_state(self, action, state:state):#gets an action and a state and returns the board after the siad action is excuted
        next_state = state.copy()
        self.move(action=action,state=next_state,player=state.player)
        return next_state

    def copy(self):
        return puzzle(self.graphics)
    
    def get_legal_actions(self, state:state= None):

        indices = np.where(state.Board == 0)
        indices = list(zip(indices[0], indices[1]))
        legal_actions=[]
        for i in indices:
            for k in range(4):
                legal_actions.append([i[0],i[1],k])
        return legal_actions
    
    def Pos_2_Num(self,pos:tuple):
        # return the square num that the position stands on
        x,y=pos
        if 0<=x<=2 and 0<=y<=2:
            return 1
        elif 0<=x<=2 and 3<=y<=5:
            return 3
        elif 3<=x<=5 and 0<=y<=2:
            return 2
        elif 3<=x<=5 and 3<=y<=5:
            return 4
        return 1
    
    def toTensor (self, list_states, device = torch.device('cpu')) -> tuple:
        list_board_tensors = []
        list_legal_actions = []
        for state in list_states:
            board_tensor, legal_actions = state.toTensor(device) 
            list_board_tensors.append(board_tensor)
            list_legal_actions.append(torch.tensor(legal_actions))
        return torch.vstack(list_board_tensors), torch.vstack(list_legal_actions)
    
    def reward (self, state : state, action = None) -> tuple:
        # if action:
        #     next_state = self.get_next_state(action, state)
        # else:
            # next_state = state
        if(self.is_winning_state(state)):
            if(self.won==2):
                self.score=-1
                return -1,True
            self.score=1
            return 1,True
        self.score=0
        if (self.isEndState(state)):
            return 0,True
        return 0,False
    