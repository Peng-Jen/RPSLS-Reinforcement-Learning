from .base_agent import BaseAgent
import random

class TitForTatAgent(BaseAgent):
    def __init__(self, config, default_action=None):
        super().__init__(config)
        self.name = "TitForTatAgent"
        if not default_action:
            default_action = random.choice(range(self.n_actions))
        self.last_opponent_action = default_action

    def encode_state(self, raw_state):
        oppo_last = raw_state['oppo_last']
        if oppo_last is None:
            return random.choice(range(self.n_actions))
        return oppo_last
    
    def select_action(self, state):
        return self.encode_state(state)

    def update(self, state, action, reward, next_state):
        self.last_opponent_action = state['oppo_last']
