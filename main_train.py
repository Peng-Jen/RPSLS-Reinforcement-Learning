import argparse
from env.rpsls_env import RPSLSEnv
from rewards_tables import CLASSIC_RPSLS, WEIGHTED_RPSLS, ONLY_SPOCK, mapping_dict
from agents import RandomAgent, TitForTatAgent, CycleAgent, OneTypeAgent, BaseQLearningAgent, SoftmaxAgent, AdaptiveAgent
from config import TrainingConfig, AgentConfig
from tools import tools
from training.against_pool import train_agent_against_pool


def parse_args():
    parser = argparse.ArgumentParser(description="Train RPSLS agent.")
    parser.add_argument("--table", type=str, choices=reward_table_map.keys(), default="CLASSIC_RPSLS",
                        help="Choose the reward table.")
    return parser.parse_args()

actions = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
agent_config = AgentConfig()
training_config = TrainingConfig()

reward_table_map = {
    "ONLY_SPOCK": ONLY_SPOCK,
    "WEIGHTED_RPSLS": WEIGHTED_RPSLS,
    "CLASSIC_RPSLS": CLASSIC_RPSLS
}

args = parse_args()
rewards = reward_table_map[args.table]
name = args.table

trained_q_agent, q_changes, actions_history = train_agent_against_pool(
    opponent_classes=[CycleAgent, OneTypeAgent, TitForTatAgent, RandomAgent],
    agent_class=BaseQLearningAgent,
    agent_config=AgentConfig(),
    training_config=TrainingConfig(),
    rewards_table=rewards,
    mapping=mapping_dict,
    proportions=[0.33, 0.33, 0.33, 0.01]
)

trained_softmax_agent, softmax_q_changes, softmax_actions_history = train_agent_against_pool(
    opponent_classes=[CycleAgent, OneTypeAgent, TitForTatAgent, RandomAgent],
    agent_class=SoftmaxAgent,
    agent_config=AgentConfig(),
    training_config=TrainingConfig(),
    rewards_table=rewards,
    mapping=mapping_dict,
    proportions=[0.33, 0.33, 0.33, 0.01]
)

tools.plot_q_convergence(q_changes, trained_q_agent)
tools.plot_q_convergence(softmax_q_changes, trained_softmax_agent)
tools.plot_strategy_distribution(actions_history, actions=actions, agent=trained_q_agent)
tools.plot_strategy_distribution(actions_history, actions=actions, agent=trained_softmax_agent)


agent_classes = {
    "Random": RandomAgent(AgentConfig()),
    "OneType": OneTypeAgent(AgentConfig()),
    "Cycle": CycleAgent(AgentConfig()),
    "TitForTat": TitForTatAgent(AgentConfig(), rewards, mapping_dict),
    "Adaptive": AdaptiveAgent(AgentConfig(), rewards, mapping_dict),
    "QLearning": trained_q_agent,
    "Softmax": trained_softmax_agent,
}
trained_q_agent.save_Q(name)
trained_softmax_agent.save_Q(name)
tools.plot_winrate_heatmap(env_class=RPSLSEnv, agent_classes=agent_classes, rewards_table=rewards, training_config=TrainingConfig(), episodes=100)

tools.summarize_agents_battle(trained_q_agent, trained_softmax_agent, rewards, training_config=TrainingConfig(episodes=100))