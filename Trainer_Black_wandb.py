from environment import puzzle
from DQN_Agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
from RandomAgent import RA
import torch
from Tester import Tester
import wandb
import pygame
from graphics import Graphics as graphics
from constants import *
import os

def main ():

    #graphic=graphics()

    env = puzzle()

    best_score = 0
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    ####### parameters #######
    player1 = DQN_Agent(player=-1, env=env,parametes_path=None)
    player_hat = DQN_Agent(player=1, env=env, train=True)
    Q = player1.DQN
    Q_hat = Q.copy()
    Q_hat.train = False
    player_hat.DQN = Q_hat
    batch_size=50
    player2 = RA(player=1, env=env) 
    buffer = ReplayBuffer(path=None)

    learning_rate = 0.01
    epochs = 250000
    start_epoch = 0
    C = 100
    # init optimizer
    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)
    #scheduler = torch.optim.lr_scheduler.StepLR(optim,30000, gamma=0.90)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[500*10, 1000*10, 1500*10, 2000*10, 2500*10, 3000*10], gamma=0.9)
    MIN_Buffer = 4000

    File_Num = 3
    path_load= None
    path_Save=f'data/run_{File_Num}/parameters_{File_Num}.pth'
    path_best = f'data/run_{File_Num}/best_parameters_{File_Num}.pth'
    buffer_path = f'data/run_{File_Num}/buffer_{File_Num}.pth'
    results_path=f'data/run_{File_Num}/results_{File_Num}.pth'
    random_results_path = f'data/run_{File_Num}/random_results_{File_Num}.pth'
    path_best_random = f'data/run_{File_Num}/best_random_parameters_{File_Num}.pth'
    Q_hat.train = False
    player_hat.DQN = Q_hat
    
    player2 = RA(player=-1,env=env)
    
    #בריצות הבאות, אשר ידרשו שימוש בפרמטרים שנצברו והותאמו לפי הריצה הזאת(ההתחלתית) נבצע את הפעולות הבאות במקומות הבאים
    #results_file=torch.load(results_path)
    results = []#results_file['results']
    avgLosses = []#results_file['avglosses']
    avgLoss = 0
    loss = 0
    res = 0
    best_res = -200
    loss_count = 0
    tester = Tester(player1=RA(player=1, env=env), player2=player1, env=env)
    tester_fix = Tester(player1=player2, player2=player1, env=env)
    random_results = []#torch.load(random_results_path)
    best_random =0#max(random_results)
    scores, losses, avg_score = [], [], []
    ########load checkpoint ###########
    

    





    ####### w and b initiator######
    wandb.init(
        #set current project
        project="pentago",
        resume=False,
        id=f' pentago {3}',
        config={
            "name":f' pentago {3}',
            "checkpoint": None,
            "learning_rate": learning_rate,
            "Schedule": f'{str(scheduler.milestones)} gama={str(scheduler.gamma)}',
            "epochs":epochs,
            "start_epoch":start_epoch,
            "decay":epsiln_decay,
            "gamma": 0.9,
            "batch_size":batch_size,
            "C":C,
            "Model":str(player1.DQN),
            "device":str(device)
        }

    )

    for epoch in range(start_epoch, epochs):
        state = env.get_init_state((6,6))
        action = player2.get_Action(gameState=state)
        state_1 = env.get_next_state(state=state, action=action)
        state_1_R = state_1.reverse()
        while not env.isEndState(state_1_R):
            # Sample Environement
            action_1_R = player1.get_Action(state_1_R, epoch=epoch, black_state=state_1_R) # fix add param
            after_state_1_R = env.get_next_state(state=state_1_R, action=action_1_R)
            reward_1_R, end_of_game_1_R = env.reward(after_state_1_R)
            if end_of_game_1_R:
                res += reward_1_R
                buffer.push(state_1_R, action_1_R, reward_1_R, after_state_1_R, True)
                break
            state_2 = after_state_1_R.reverse()
            action_2 = player2.get_Action(gameState=state_2)
            after_state_2 = env.get_next_state(state=state_2, action=action_2)
            after_state_2_R = after_state_2.reverse() 
            reward_2_R, end_of_game_2 = env.reward(state=after_state_2_R)
            if end_of_game_2:
                res += reward_2_R
            buffer.push(state_1_R, action_1_R, reward_2_R, after_state_2_R, end_of_game_2)
            state_1_R = after_state_2_R

            if len(buffer) < MIN_Buffer:
                continue
            
            # Train NN
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = Q(states, actions)
            next_actions = player_hat.get_Actions(next_states, dones) 
            with torch.no_grad():
                Q_hat_Values = Q_hat(next_states, next_actions)

            loss = Q.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            
            scheduler.step()
            if loss_count <= 1000:
                avgLoss = (avgLoss * loss_count + loss.item()) / (loss_count + 1)
                loss_count += 1
            else:
                avgLoss += (loss.item()-avgLoss)* 0.00001 
            
        if epoch % C == 0:
                Q_hat.load_state_dict(Q.state_dict())

        if (epoch+1) % 100 == 0:
            print(f'\nres= {res}')
            avgLosses.append(avgLoss)
            results.append(res)
            if best_res < res:      
                best_res = res
                # if best_res > 75 and tester_fix(1) == (0,1):
                #     player1.save_param(path_best)
            res = 0

        # if (epoch+1) % 1000 == 0:
        #     test = tester(100)
        #     test_score = test[0]-test[1]
        #     if best_random < test_score and tester_fix(1) == (0,1):
        #         best_random = test_score
        #         player1.save_param(path_best_random)
        #     print(test)
        #     random_results.append(test_score)

        if (epoch+1) % 5000 == 0:
            torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
            torch.save(buffer, buffer_path)
            player1.save_param(path_Save)
            torch.save(random_results, random_results_path)

        print (f'epoch={epoch} loss={loss:.5f}  avgloss={avgLoss:.5f}', end=" ")
        print (f'learning rate={scheduler.get_last_lr()[0]} path={path_Save} res= {res} best_res = {best_res}')

    

    torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
    torch.save(buffer, buffer_path)
    torch.save(random_results, random_results_path)

if __name__ == '__main__':

    main()

