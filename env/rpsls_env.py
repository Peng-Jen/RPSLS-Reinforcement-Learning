import numpy as np
from typing import *

class RPSLSEnv:
    def __init__(self, rewards_table, target_score):
        self.actions = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
        self.n_actions = len(self.actions)
        self.rewards_table = rewards_table
        self.target_score = target_score
        self.reset()

    def get_state(self):
        raw_state = {
            'self_last': self.self_last,
            'oppo_last': self.oppo_last,
            'self_history': self.self_history.copy(),
            'oppo_history': self.oppo_history.copy(),
            'oppo_distribution': self._get_distribution(self.oppo_history, window_size=20),
            'self_score': self.self_score,
            'oppo_score': self.oppo_score,
            'self_reward': self.self_reward,
            'oppo_reward': self.oppo_reward
        }
        
        return raw_state
    
    def get_oppo_state(self):
        raw_state = {
            'self_last': self.oppo_last,
            'oppo_last': self.self_last,
            'self_history': self.oppo_history.copy(),
            'oppo_history': self.self_history.copy(),
            'oppo_distribution': self._get_distribution(self.self_history, window_size=20),
            'self_score': self.oppo_score,
            'oppo_score': self.self_score,
            'self_reward': self.oppo_reward,
            'oppo_reward': self.self_reward
        }
        
        return raw_state

    def step(self, self_action, oppo_action):
        self_action_type = self.actions[self_action]
        oppo_action_type = self.actions[oppo_action]
        self_reward, oppo_reward = self.rewards_table[(self_action_type, oppo_action_type)]
        
        self.self_last = self_action
        self.oppo_last = oppo_action
        self.self_history.append(self_action)
        self.oppo_history.append(oppo_action)
        self.self_reward = self_reward
        self.oppo_reward = oppo_reward
        self.self_score += self_reward
        self.oppo_score += oppo_reward

        return self_reward, oppo_reward
    
    def is_done(self):
        return self.self_score >= self.target_score or self.oppo_score >= self.target_score
    
    def reset(self):
        self.self_last = None
        self.oppo_last = None
        self.self_history = []
        self.oppo_history = []
        self.self_score = 0
        self.oppo_score = 0
        self.self_reward = 0
        self.oppo_reward = 0

    def _get_distribution(self, history, window_size=20):
        from collections import Counter
        records = min(len(history), window_size)
        count = Counter(history[-records:])
        return [count.get(i, 0) / records if records > 0 else 0.0 for i in range(self.n_actions)]