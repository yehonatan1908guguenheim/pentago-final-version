import pygame
import numpy as np
from graphics import Graphics
from state import state
from environment import puzzle
from constants import *
from MinMaxAgent import MMA
from HumanAgent import HumanAgent
import time
# from Trainer_White import 
import random
from AlphaBetaAgent import ABA
from RandomAgent import RA
from DQN_Agent import DQN_Agent
FPS=60
# set screen size
screen = pygame.display.set_mode((600, 600))



#set the actual graphics
graphics=Graphics()

#set the environment class(helper class)
env=puzzle(graphics)
env.state=env.get_init_state((6,6))
#set human and minmax agents

player1 = HumanAgent(player=1, env= env)
#player2=HumanAgent(player=-1, env= env)
#player1 = MMA(c=env,player=1)
#player2=MMA(c=env,player=-1) 
#player2= ABA(c=env,player=-1)
#player1=ABA(c=env,player=1)
#player1=RA(1,env)
#player1=DQN_Agent(player=1,parametes_path="data/run_10/parameters_10.pth",train=False,env=env)
player2=RA(-1,env)
#zeros=[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(5,0),(5,1),(5,2),(5,3),(5,4),(5,5)]


def Main():

    run = True
    clock = pygame.time.Clock()
    graphics.draw(env.state)
    player = player1
    
    while(run):
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
               run = False
               exit()
        #player.get_Action(events=events, gameState:env.state, epoch = 0, events= None, train = True, graphics = None, black_state:state = None)
        action = player.get_Action(events= events,gameState= env.state, graphics=graphics)

        if action:
            env.move(action,env.state,player.player)
            time.sleep(1)
            graphics.draw(env.state)
            if env.is_winning_state(env.state):
                run = False
                print(env.state.Board)
                print("Victory!")
                winning= "Player " +str(env.won)+" won"
                print(winning)
                return
            elif env.isEndState(env.state):
                run = False
                print("no one won")
            
            player=switchPlayers(player)
        else:
            if env.isEndState(env.state):
                run = False
                if env.won != 0:
                    winning= "Player " +str(env.won)+" won"
                    print(winning)
        pygame.display.update()
        
    
    # quit pygame
    time.sleep(100)
    pygame.quit()
    

def switchPlayers(player):
    if player == player1:
       return player2
    elif player==player2:
        return player1

if __name__ == '__main__':
    Main()



