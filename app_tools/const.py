from agents import RandomAgent, TitForTatAgent, CycleAgent, OneTypeAgent, BaseQLearningAgent, SoftmaxAgent, AdaptiveAgent
from rewards_tables import CLASSIC_RPSLS, WEIGHTED_RPSLS, ONLY_SPOCK


actions = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
tables = ['CLASSIC_RPSLS', 'WEIGHTED_RPSLS', 'ONLY_SPOCK']
agents = ['QLearningAgent', 'SoftmaxAgent', 'RandomAgent', 'TitForTatAgent', 'AdaptiveAgent']
pretrained_agent = ['QLearningAgent', 'SoftmaxAgent']
emoji_map = {
    'Rock': '✊',
    'Paper': '🖐️',
    'Scissors': '✌️',
    'Lizard': '🤌',
    'Spock': '🖖'
}

agents_map = {
    'RandomAgent': RandomAgent,
    'OneTypeAgent': OneTypeAgent,
    'QLearningAgent': BaseQLearningAgent,
    'SoftmaxAgent': SoftmaxAgent,
    'TitForTatAgent': TitForTatAgent,
    'AdaptiveAgent': AdaptiveAgent
}

tables_map = {
    'CLASSIC_RPSLS': CLASSIC_RPSLS, 
    'WEIGHTED_RPSLS': WEIGHTED_RPSLS,
    'ONLY_SPOCK': ONLY_SPOCK
}
