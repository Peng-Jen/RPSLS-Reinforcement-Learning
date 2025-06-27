import random
from env.rpsls_env import RPSLSEnv
import numpy as np
from copy import deepcopy
from tqdm import tqdm

def train_agent_against_pool(opponent_classes, agent_class, rewards_table, agent_config, training_config, proportions=None):
    """
    Trains a QLearningAgent against a pool of opponents with optional proportions.
    """
    if proportions is None:
        proportions = [1 / len(opponent_classes)] * len(opponent_classes)

    assert abs(sum(proportions) - 1.0) < 1e-6, "Proportions must sum to 1.0"


    agent = agent_class(agent_config)
    q_changes = []
    action_history = []

    for _ in tqdm(range(training_config.episodes)):
        opponent_cls = random.choices(opponent_classes, weights=proportions)[0]
        opponent = opponent_cls(agent_config)

        env = RPSLSEnv(rewards_table=rewards_table, target_score=training_config.target_score)
        env.reset()
        rounds = 0

        q_before = deepcopy(agent.Q)

        while not env.is_done() and rounds < training_config.max_rounds:
            state = env.get_state()
            a_agent = agent.select_action(state)
            a_oppo = opponent.select_action(state)
            r_agent, r_oppo = env.step(a_agent, a_oppo)

            agent.update(state, a_agent, r_agent, env.get_state())
            opponent.update(state, a_oppo, r_oppo, env.get_state())


            action_history.append(a_agent)
            rounds += 1

        if hasattr(agent, "decay_epsilon"):
            agent.decay_epsilon()
        if hasattr(opponent, "decay_epsilon"):
            opponent.decay_epsilon()
        if hasattr(agent, "decay_temperature"):
            agent.decay_temperature()
        if hasattr(opponent, "decay_temperature"):
            opponent.decay_temperature()
        
        q_after = agent.Q
        all_keys = set(q_before.keys()).union(q_after.keys())
        q_change = sum(
            np.sum(np.abs(np.array(q_after.get(k, 0)) - np.array(q_before.get(k, 0))))
            for k in all_keys
        )
        q_changes.append(q_change)

    return agent, q_changes, action_history
