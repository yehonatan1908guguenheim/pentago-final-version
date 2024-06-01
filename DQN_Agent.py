import torch
import random
import math
from DQN import DQN
from constants import *
from state import state
from environment import puzzle
class DQN_Agent:
    def __init__(self, player = 1, parametes_path = None, train = True, env:puzzle= None):
        self.DQN = DQN()
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.player = player
        self.train = train
        self.setTrainMode()
        self.env=env
    def setTrainMode (self):
          if self.train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_Action (self, gameState:state, epoch = 0, events= None, train = True, graphics = None, black_state:state = None) -> tuple:
        actions = gameState.legal_actions()
        tensor_action=torch.tensor(actions)
        if self.train and train:
            epsilon = self.epsilon_greedy(epoch)
            rnd = random.random()
            if rnd < epsilon:
                return random.choice(actions)
        if self.player == 1:
            state_tensor = gameState.toTensor()
        elif not black_state:
            black_state = gameState.reverse()
            state_tensor = black_state.toTensor()
        else:
            state_tensor = black_state.toTensor()

        expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(tensor_action),1))
        
        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, tensor_action)
        max_index = torch.argmax(Q_values)
        return actions[max_index]

    def get_Actions (self, states_tensor: state, dones) -> torch.tensor:
        actions = []
        

        for i, board in enumerate(states_tensor):
            if dones[i].item():
                actions.append([0,0,0])
            else:
                actions.append(self.get_Action(state.tensorToState(states_tensor[i],player=self.player), train=False))
        return torch.tensor(actions)

    def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
        bol=epoch>decay
        if not bol:
            res = final + (start - final) * epoch/decay
            return res
        return final
    
    def loadModel (self, file):
        self.model = torch.load(file)
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def __call__(self, events= None, state=None):
        return self.get_Action(state)