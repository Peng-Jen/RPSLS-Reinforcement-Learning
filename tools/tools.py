import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import os
from tqdm import tqdm

def plot_q_convergence(q_changes, agent, filename="Q-value_convergence"):
    plt.figure(figsize=(10, 6))
    plt.plot(q_changes, label=agent.name)
    plt.title("Q-Table Convergence")
    plt.xlabel("Episodes")
    plt.ylabel("Total Q Change")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(os.path.join(save_path, f'{filename}_{agent.name}.png'))


def plot_strategy_distribution(history, actions, agent, filename="strategy_distribution"):
    counts = Counter(history)
    total = sum(counts.values())
    frequencies = [counts.get(i, 0) / total for i in range(len(actions))]

    plt.figure(figsize=(6, 4))
    plt.bar(actions, frequencies, color='skyblue')
    plt.title(f"{agent.name} Strategy Distribution")
    plt.xlabel("Actions")
    plt.ylabel("Frequency")
    plt.ylim(0, 1)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(os.path.join(save_path, f'{filename}_{agent.name}.png'))

def plot_winrate_heatmap(env_class, agent_classes, rewards_table, training_config, episodes=100, filename="winrate_heatmap"):
    from itertools import product
    from copy import deepcopy

    env = env_class(rewards_table=rewards_table, target_score=training_config.target_score)

    names = list(agent_classes.keys())
    matrix = np.zeros((len(names), len(names)))

    for i, j in tqdm(product(range(len(names)), repeat=2)):
        agent_A = deepcopy(agent_classes[names[i]])
        agent_B = deepcopy(agent_classes[names[j]])
        winrate = []
        for _ in range(episodes):
            env.reset()
            played_game = 0
            wins_A = 0

            while not env.is_done() and played_game < training_config.max_rounds:
                state = env.get_state()
                a_A = agent_A.select_action(state)
                a_B = agent_B.select_action(state)
                r_A, r_B = env.step(a_A, a_B)
                agent_A.update(state, a_A, r_A, env.get_state())
                agent_B.update(state, a_B, r_B, env.get_state())
                played_game += 1

            if hasattr(agent_A, "decay_epsilon"):
                agent_A.decay_epsilon()
            if hasattr(agent_B, "decay_epsilon"):
                agent_B.decay_epsilon()
            if hasattr(agent_A, "decay_temperature"):
                agent_A.decay_temperature()
            if hasattr(agent_B, "decay_temperature"):
                agent_B.decay_temperature()

            if env.self_score > env.oppo_score:
                wins_A += 1

            winrate.append(wins_A)
        matrix[i][j] = np.mean(winrate)


    plt.figure(figsize=(8, 6))
    plt.imshow(matrix, cmap="coolwarm", interpolation="nearest")
    plt.colorbar(label="Win rate vs Opponent")
    plt.xticks(ticks=np.arange(len(names)), labels=names)
    plt.yticks(ticks=np.arange(len(names)), labels=names)
    plt.title("Agent A win rate vs Agent B")
    for i in range(len(names)):
        for j in range(len(names)):
            plt.text(j, i, f"{matrix[i][j]:.2f}", ha='center', va='center', color='white')
    plt.tight_layout()

    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(os.path.join(save_path, f'{filename}.png'))

def summarize_agents_battle(agent_A, agent_B, rewards_table, training_config, actions=["Rock", "Paper", "Scissors", "Lizard", "Spock"]):
    from collections import Counter
    from env.rpsls_env import RPSLSEnv
    from copy import deepcopy

    env = RPSLSEnv(rewards_table=rewards_table, target_score=training_config.target_score)
    episodes = training_config.episodes
    max_rounds = training_config.max_rounds

    agent_A = deepcopy(agent_A)
    agent_B = deepcopy(agent_B)

    wins_A, wins_B, draws = 0, 0, 0
    action_count_A = Counter()
    action_count_B = Counter()
    for _ in tqdm(range(episodes)):
        env.reset()
        played_game = 0
        while not env.is_done() and played_game < max_rounds:
            state = env.get_state()
            a_A = agent_A.select_action(state)
            a_B = agent_B.select_action(state)
            r_A, r_B = env.step(a_A, a_B)
            agent_A.update(state, a_A, r_A, env.get_state())
            agent_B.update(state, a_B, r_B, env.get_state())
            action_count_A[a_A] += 1
            action_count_B[a_B] += 1
            played_game += 1

        if env.self_score > env.oppo_score:
            wins_A += 1
        elif env.self_score < env.oppo_score:
            wins_B += 1
        else:
            draws += 1

    def normalize(counter):
        total = sum(counter.values())
        return {actions[k]: round(v / total, 3) for k, v in sorted(counter.items())}
    
    print("\n🎯 Simulation Result")
    print(f"Agent A ({agent_A.name}) wins: {wins_A}")
    print(f"Agent B ({agent_B.name}) wins: {wins_B}")
    print(f"Draws: {draws}")
    print("\n📊 Action Distribution")
    print("Agent A:", normalize(action_count_A))
    print("Agent B:", normalize(action_count_B))