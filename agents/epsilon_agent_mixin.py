class EpsilonAgentMixin:
    def __init__(self, epsilon, epsilon_decay, epsilon_min):
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
