import numpy as np
import random
from .base_agent import BaseAgent
from .epsilon_agent_mixin import EpsilonAgentMixin

class BaseQLearningAgent(BaseAgent, EpsilonAgentMixin):
    """
    state = (self-last-action, opponent-last-action) and random choice for the first state
    """
    def __init__(self, config, pretrained=None):
        BaseAgent.__init__(self, config)
        EpsilonAgentMixin.__init__(self, config.epsilon, config.epsilon_decay, config.epsilon_min)
        self.name = "QLearningAgent"
        self.Q = pretrained if pretrained else {}
        self.alpha = config.alpha
        self.gamma = config.gamma

    def get_Q_value(self, state):
        if state not in self.Q:
            self.Q[state] = np.zeros(self.n_actions)
        return self.Q[state]

    def encode_state(self, raw_state):
        self_last = raw_state['self_last'] if raw_state['self_last'] is not None else random.choice(range(self.n_actions))
        oppo_last = raw_state['oppo_last'] if raw_state['oppo_last'] is not None else random.choice(range(self.n_actions))
        return (self_last, oppo_last)
    
    def select_action(self, state):
        state = self.encode_state(state)
        q_table = self.get_Q_value(state)
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        return np.random.choice(np.flatnonzero(q_table == q_table.max()))

    def update(self, state, action, reward, next_state):
        state = self.encode_state(state)
        next_state = self.encode_state(next_state)
        q_next = max(self.get_Q_value(next_state))
        q_now = self.get_Q_value(state)[action]
        self.Q[state][action] += self.alpha * (reward + self.gamma * q_next - q_now)
