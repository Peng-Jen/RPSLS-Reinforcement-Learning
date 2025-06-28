import numpy as np
import cvxpy as cp
import random
from .base_agent import BaseAgent


class AdaptiveAgent(BaseAgent):
    def __init__(self, config, rewards_table, mapping):
        super().__init__(config)
        self.name = "AdaptiveAgent"
        self.mode = "nash"
        self.payoff = self._build_payoff(rewards_table, mapping)
        self.nash_strategy = self._solve_nash()
        self.current_strategy = self.nash_strategy
        self.oppo_history = []
        self.threshold = 10  # rounds for observation
        self.total_steps = 0
        self.exploit_score = 0
        self.nash_score = 0

    def _build_payoff(self, table, mapping):
        payoff = np.zeros((self.n_actions, self.n_actions))
        for (i, j), (a_score, _) in table.items():
            payoff[mapping[i]][mapping[j]] = a_score
        return payoff
    
    def _solve_nash(self):
        pA = cp.Variable(self.n_actions)
        v = cp.Variable()

        constraints = [cp.sum(pA) == 1, pA >= 0]
        for j in range(self.n_actions):
            constraints.append(pA @ self.payoff[:, j] >= v)

        problem = cp.Problem(cp.Maximize(v), constraints)
        problem.solve()
        return pA.value

    def select_action(self, state):
        return np.random.choice(len(self.current_strategy), p=self.current_strategy)

    def update(self, state, action, reward, next_state):
        self.oppo_history.append(next_state["oppo_last"])
        self.total_steps += 1
        if self.mode == "nash":
            self.nash_score += reward
        elif self.mode == "exploit":
            self.exploit_score += reward

        if len(self.oppo_history) >= self.threshold:
            cycle = self._detect_cycle()
            if cycle is not None:
                self.mode = "cycle-exploit"
                self.current_strategy = self._exploit_cycle(cycle)
                return

            dist = self._estimate_oppo_dist()
            if self.mode == "nash" and self._should_exploit(dist):
                self.current_strategy = self._compute_best_response(dist)
                self.mode = "exploit"
            elif self.mode == "exploit" and self._should_revert_to_nash():
                self.current_strategy = self.nash_strategy
                self.mode = "nash"
    
    def _estimate_oppo_dist(self, window_size=20, decay=0.9):
        dist = np.zeros(self.n_actions)
        history = reversed(self.oppo_history[-20:])
        weight = 1
        for action in history:
            dist[action] += weight
            weight *= decay
        dist /= np.sum(dist)
        return dist
    
    def _should_exploit(self, oppo_dist):
        def entropy(dist):
            p = (p:= np.array(dist))[p > 0]
            return -np.sum(p * np.log2(p))
        return entropy(oppo_dist) < 1.5  # max entropy for 5 actions is about 2.3
    
    def _should_revert_to_nash(self):
        if self.total_steps < self.threshold:
            return False
        exploit_avg = self.exploit_score / max(1, self.total_steps)
        nash_avg = self.nash_score / max(1, self.total_steps)
        return exploit_avg < nash_avg    
    
    def _compute_best_response(self, oppo_dist):
        best_p = cp.Variable(self.n_actions)
        constraints = [cp.sum(best_p) == 1, best_p >= 0]
        expected = best_p @ (self.payoff @ oppo_dist)
        problem = cp.Problem(cp.Maximize(expected), constraints)
        problem.solve()
        return [round(x, 4) for x in best_p.value]

    def _detect_cycle(self, window_size=10, max_period=5):
        if len(self.oppo_history) < window_size:
            return None
        window = self.oppo_history[-window_size:]
        for period in range(1, max_period + 1):
            if all(window[i] == window[i % period] for i in range(len(window))):
                return period
        return None

    def _exploit_cycle(self, cycle_length):
        predicted = self.oppo_history[len(self.oppo_history) - cycle_length]
        counter = self._get_counter(predicted)
        strategy = np.zeros(self.n_actions)
        strategy[counter] = 1.0
        return strategy

    def _get_counter(self, action_id):
        win_actions = [(i, self.payoff[i][action_id]) for i in range(self.n_actions) if self.payoff[i][action_id] >= 0]
        if not win_actions:
            return random.randint(0, self.n_actions - 1)
        max_reward = max(score for _, score in win_actions)
        best_actions = [i for i, score in win_actions if score == max_reward]
        return random.choice(best_actions)

