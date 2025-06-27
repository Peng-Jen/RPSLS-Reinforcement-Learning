import random
from .base_agent import BaseAgent

class RandomAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.name = "RandomAgent"
        
    def select_action(self, state):
        return random.choice(range(self.n_actions))
