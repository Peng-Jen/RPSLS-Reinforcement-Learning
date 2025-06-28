from .base_agent import BaseAgent
import random
import numpy as np

class TitForTatAgent(BaseAgent):
    def __init__(self, config, rewards_table, mapping, default_action=None):
        super().__init__(config)
        self.name = "TitForTatAgent"
        self.payoff = self._build_payoff(rewards_table, mapping)
        if not default_action:
            default_action = random.choice(range(self.n_actions))
        self.last_opponent_action = default_action

    def encode_state(self, raw_state):
        oppo_last = raw_state['oppo_last']
        if oppo_last is None:
            return random.choice(range(self.n_actions))
        return oppo_last
    
    def select_action(self, state):
        return self._get_counter(self.encode_state(state))

    def update(self, state, action, reward, next_state):
        self.last_opponent_action = state['oppo_last']

    def _build_payoff(self, table, mapping):
        payoff = np.zeros((self.n_actions, self.n_actions))
        for (i, j), (a_score, _) in table.items():
            payoff[mapping[i]][mapping[j]] = a_score
        return payoff

    def _get_counter(self, action_id):
        win_actions = [(i, self.payoff[i][action_id]) for i in range(self.n_actions) if self.payoff[i][action_id] > 0]
        if not win_actions:
            return random.randint(0, self.n_actions - 1)
        max_reward = max(score for _, score in win_actions)
        best_actions = [i for i, score in win_actions if score == max_reward]
        return random.choice(best_actions)
