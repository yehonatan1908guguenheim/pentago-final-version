from DQN_Agent import DQN_Agent
from Tester import Tester
from graphics import Graphics
from environment import puzzle
graphics=Graphics()

#set the environment class(helper class)
env=puzzle(graphics)
env.state=env.get_init_state((6,6))
player1=DQN_Agent(1,)
testi= Tester(env,)