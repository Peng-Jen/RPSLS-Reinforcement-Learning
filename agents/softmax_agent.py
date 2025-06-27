import numpy as np
import random
from .base_agent import BaseAgent
from .epsilon_agent_mixin import EpsilonAgentMixin
from .temperature_agent_mixin import TemperatureAgentMixin

class SoftmaxAgent(BaseAgent, EpsilonAgentMixin, TemperatureAgentMixin):
    def __init__(self, config, pretrained=None):
        BaseAgent.__init__(self, config)
        EpsilonAgentMixin.__init__(self, config.epsilon, config.epsilon_decay, config.epsilon_min)
        TemperatureAgentMixin.__init__(self, config.temperature, config.temperature_decay, config.temperature_min)
        self.name = "SoftmaxAgent"
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
        q_vals = self.get_Q_value(state)
        exp_q = np.exp(q_vals / self.temperature)
        probs = exp_q / np.sum(exp_q)
        return np.random.choice(self.n_actions, p=probs)

    def update(self, state, action, reward, next_state):
        state = self.encode_state(state)
        next_state = self.encode_state(next_state)
        q_next = max(self.get_Q_value(next_state))
        q_now = self.get_Q_value(state)[action]
        self.Q[state][action] += self.alpha * (reward + self.gamma * q_next - q_now)
