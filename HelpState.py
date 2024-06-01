from state import state
import numpy as np

class HelpState:
    
    def __init__(self,state:state,act) -> None:
        self.state=state
        self.action=act
