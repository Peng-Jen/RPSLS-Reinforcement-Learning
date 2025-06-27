from .base_agent import BaseAgent
import random

class OneTypeAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.name = "OneTypeAgent"
        if config.default_action not in range(self.n_actions):
            self.action = random.choice(range(self.n_actions))
        else:
            self.action = config.default_action
    
    def select_action(self, state):
        return self.action
