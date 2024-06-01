from RandomAgent import RA
from environment import puzzle
from constants import *
from AlphaBetaAgent import ABA
from MinMaxAgent import MMA
from DQN_Agent import DQN_Agent
class Tester:
    def __init__(self, env:puzzle, player1, player2) -> None:
        self.env = env
        self.player1 = player1
        self.player2 = player2

    def test (self, games_num):
        env = self.env
        player = self.player1
        player1_win = 0
        player2_win = 0
        games = 0
        while games < games_num:
            action = player.get_Action(gameState=env.state)
            env.move(action, env.state,player.player)
            player = self.switchPlayers(player)
            if env.isEndState(env.state):
                score = self.env.is_winning_state(env.state)
                if score >0:
                    player1_win += 1
                elif score <0:
                    player2_win += 1
                env.state = env.get_init_state((ROWS,COLS))
                games += 1
                player = self.player1
        return player1_win, player2_win        

    def switchPlayers(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def __call__(self, games_num):
        return self.test(games_num)

if __name__ == '__main__':
    env = puzzle()
    # player1 = RA(env=env,player=1)
    # player2 = RA(env=env, player=-1)
    # test = Tester(env,player1, player2)
    # print(test.test(100))
    # player1 = ABA(env=env, player=1)
    # player2 = ABA(env=env, player=-1)
    # test = Tester(env,player1, player2)
    # print(test.test(100))
    player1 = MMA(c=env, player=1,depth=2)
    # player2 = MMA(env=env, player=-1)
    # test = Tester(env,player1, player2)
    # print(test.test(100))
    # player1 = DQN_Agent(player=1, parametes_path="data/run_10/parameters_10.pth", train=False, env=env)
    player2 = RA(env=env, player=-1)
    test = Tester(env,player1, player2)
    score=[]
    for i in range(15):
        test1=test.test(10)
        print(test1) 
        score.append(test1[0]-test1[1])
        test = Tester(env,player1, player2)
    print("min max vs ra"+score)