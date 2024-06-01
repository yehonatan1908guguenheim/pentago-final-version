
from environment import puzzle
from DQN_Agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
from RandomAgent import RA
from Fix_Agent import Fix_Agent
import torch
from Tester import Tester


File_Num = 12
path_load= None



def main ():
    
    env = puzzle()
    if torch.cuda.is_available():
        device=torch.device('cuda')
    else:
        device= torch.device('cpu')
    
    path_Save=f'data/run_{File_Num}/parameters_{File_Num}.pth'
    path_best = f'data/run_{File_Num}/best_parameters_{File_Num}.pth'
    buffer_path = f'data/run_{File_Num}/buffer_{File_Num}.pth'
    results_path=f'data/run_{File_Num}/results_{File_Num}.pth'
    random_results_path = f'data/run_{File_Num}/random_results_{File_Num}.pth'
    path_best_random = f'data/run_{File_Num}/best_random_parameters_{File_Num}.pth'
    
    ## parameters#####
    player1 = DQN_Agent(player=1, env=env,parametes_path=path_load)
    player2 = DQN_Agent(player=-1, env=env,parametes_path=None)
    player_hat = DQN_Agent(player=1, env=env,parametes_path=None) 
    Q = player1.DQN
    player2.DQN = Q
    Q_hat = Q.copy()
    Q_hat.train = False
    player_hat.DQN = Q_hat
    buffer = ReplayBuffer(path=None) # None
    epochs = 200000
    start_epoch = 0
    C = 100
    learning_rate = 0.01
    batch_size = 50
    MIN_Buffer = 4000

    
    
    
    

    #results_file = torch.load(results_path)
    results =[]  #results_file['results'] # []
    avgLosses = []
    avgLoss =  0
    loss = 0
    res = 0
    best_res = -200
    loss_count = 0
    tester1 = Tester(player1=player1, player2=RA(player=-1, env=env), env=env)
    tester2=Tester(player1=player2, player2=RA(player=1, env=env), env=env)
    tester_fix = Tester(player1=Fix_Agent(env=env,player=1, train=False), player2=player2, env=env)
    random_results =  []
    best_random = 0
        
    # init optimizer
    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optim,1000*20, gamma=0.95)
    # scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[30*50000, 30*100000, 30*250000, 30*500000], gamma=0.5)
    
    for epoch in range(start_epoch, epochs):
        print(f'epoch = {epoch}', end='\r')
        state_1 = env.get_init_state((6,6))
        state_2, action_2, after_state_2 = None, None, None
        state_2_R, after_state_2_R = None, None
        end_of_game_1 = False
        while not end_of_game_1:
        # Sample Environement
            # white
            action_1 = player1.get_Action(state_1, epoch=epoch)
            action_1_R = action_1
            after_state_1 = env.get_next_state(state=state_1, action=action_1)
            after_state_1_R = after_state_1.reverse()
            reward_1, end_of_game_1 = env.reward(after_state_1)
            reward_1_R, end_of_game_1_R = -reward_1, end_of_game_1 
            if state_2: # not the first action in a game
                    buffer.push(state_2_R, action_2_R, reward_1_R, after_state_1_R, end_of_game_1_R)    # for black
            if end_of_game_1:
                res += reward_1
                buffer.push(state_1, action_1, reward_1, after_state_1, True) # for white
                state_1 = after_state_1
            else:
                # Black
                state_2 = after_state_1
                state_2_R = after_state_1_R
                action_2 = player2.get_Action(gameState=state_2, epoch=epoch, black_state=state_2_R)
                action_2_R = action_2
                after_state_2 = env.get_next_state(state=state_2, action=action_2)
                after_state_2_R = after_state_2.reverse()
                reward_2, end_of_game_2 = env.reward(state=after_state_2)
                reward_2_R, end_of_game_2_R = -reward_2, end_of_game_2
                if end_of_game_2:
                    res += reward_2
                    buffer.push(state_2_R, action_2_R, reward_2_R, after_state_2_R, True) # for black
                buffer.push(state_1, action_1, reward_2, after_state_2, end_of_game_2)
                state_1 = after_state_2
                end_of_game_1 = end_of_game_2

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
            res = 0

        if (epoch+1) % 500 == 0:
            test = tester1(100)
            test_score = test[0]-test[1]
            test2=tester2(100)
            test_score_2=test2[0]-test2[1]
            if best_random < test_score:
                best_random = test_score
                player1.save_param(path_best_random)
            if best_random < test_score_2:
                best_random = test_score_2
                player2.save_param(path_best_random)
            print('test player 1',test, 'test player 2', test2,'best_random:', best_random)
            random_results.append(test_score)

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

