import numpy as np
import torch
class state:
    def __init__(self , arr1:list,player=1)->None :
        self.Board=np.array(arr1.copy())
        self.player=player

    def __eq__(self, s) -> bool:
        b1=np.equal(self.Board,s.Board).all()
        b2= self.player==s.player
        return b1 and b2

    def get_opponent(self):
        return -self.player
    
    def copy(self):
        newBoard=np.copy(self.Board)
        return state(newBoard,self.player)

    def __hash__(self) -> int:
        return hash(repr(self.Board))
    
    def legal_actions(self):
        indices = np.where(self.Board == 0)
        indices = list(zip(indices[0], indices[1]))
        legal_actions=[]
        for i in indices:
            for k in range(4):
                legal_actions.append([i[0],i[1],k])
        return legal_actions
    
    def toTensor (self, device = torch.device('cpu')) -> tuple:
        board_np = self.Board.reshape(-1)
        board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
        return board_tensor
    
    [staticmethod]
    def tensorToState (state_tuple, player):
        board = state_tuple.reshape([6,6]).cpu().numpy()
        return state(arr1=board, player=player)
    def reverse (self):
        reversed = self.copy()
        reversed.Board= reversed.Board * -1
        reversed.player = reversed.player * -1
        return reversed