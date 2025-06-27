from .base_agent import BaseAgent
import random

class CycleAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.name = "CycleAgent"
        if config.default_action not in range(self.n_actions):
            self.last_action = random.choice(range(self.n_actions))
        else:
            self.last_action = config.default_action
        if config.shift not in range(self.n_actions):
            self.shift = random.choice(range(self.n_actions))
        else:
            self.shift = config.shift

    def select_action(self, state):
        action = (self.last_action + self.shift) % self.n_actions
        self.last_action = action
        return action
