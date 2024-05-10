from utils.utils import get_next_directory_number
import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

def read_all_generations_cummulative_line(base_path, common_name_prefix):
    max_generation = get_next_directory_number(base_path, common_name_prefix) - 1
    all_configs = defaultdict(set)
    for generation in range(1, max_generation + 1):
        color_path = os.path.join(base_path, f"{common_name_prefix}{generation}")
        if os.path.exists(color_path):
            for color in ["black_agents", "white_agents"]:
                agent_color_path = os.path.join(color_path, color)
                if os.path.exists(agent_color_path):
                    for agent_dir in os.listdir(agent_color_path):
                        agent_path = os.path.join(agent_color_path, agent_dir, "flags.json")
                        if os.path.exists(agent_path):
                            with open(agent_path, 'r') as file:
                                data = json.load(file)
                                true_flags = frozenset(k for k, v in data.items() if v)
                                all_configs[generation].add(true_flags)
    return all_configs

def plot_cumulative_configs(all_configs):
    generations = sorted(all_configs.keys())
    unique_configs = []
    cumulative_configs = set()

    for gen in generations:
        cumulative_configs.update(all_configs[gen])
        unique_configs.append(len(cumulative_configs))

    plt.figure(figsize=(12, 8))
    plt.plot(generations, unique_configs, marker='o', linestyle='-', color='blue')
    plt.xlabel('Generation')
    plt.ylabel('Cumulative Number of Unique Configurations')
    plt.title('Cumulative Unique Genetic Configurations Over Generations')
    plt.xticks(generations)
    plt.grid(True)
    plt.show()
