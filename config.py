from dataclasses import dataclass

@dataclass
class AgentConfig:
    n_actions: int = 5                # number of actions
    alpha: float = 0.05               # learning rate
    gamma: float = 0.9                # discount factor
    epsilon: float = 1.0              # exploring rate
    epsilon_decay: float = 0.99       # epsilon decay rate
    epsilon_min: float = 0.1          # lower bound for epsilon
    temperature: float = 2            # initial temperature
    temperature_decay: float = 0.995  # temperature decay rate
    temperature_min: float = 0.5      # lower bound for temperature


@dataclass
class TrainingConfig:
    episodes: int = 10000
    target_score: int = 50
    max_rounds: int = 500

@dataclass
class AgentConfigForBattle(AgentConfig):
    alpha: float = 0.1                # learning rate
    epsilon: float = 1.0              # exploring rate
    epsilon_decay: float = 0.9        # epsilon decay rate
    epsilon_min: float = 0.1          # lower bound for epsilon
    temperature: float = 2            # initial temperature
    temperature_decay: float = 0.9    # temperature decay rate
    temperature_min: float = 0.5      # lower bound for temperature