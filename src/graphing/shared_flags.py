from utils.utils import get_next_directory_number
import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

def read_all_generations_shared_flags(base_path, common_name_prefix):
    max_generation = get_next_directory_number(base_path, common_name_prefix) - 1
    generation_data = {}
    for generation in range(1, max_generation + 1):
        agents_data = {}
        colors = ["black_agents", "white_agents"]
        for color in colors:
            color_path = os.path.join(base_path, f"{common_name_prefix}{generation}", color)
            agents_data[color] = defaultdict(list)
            if os.path.exists(color_path):
                for agent_dir in os.listdir(color_path):
                    agent_path = os.path.join(color_path, agent_dir, "flags.json")
                    if os.path.exists(agent_path):
                        with open(agent_path, 'r') as file:
                            data = json.load(file)
                            true_flags = [k for k, v in data.items() if v]
                            agents_data[color][frozenset(true_flags)].append(agent_dir)
        generation_data[generation] = agents_data
    return generation_data

def count_shared_flags(generation_data, min_shared=2):
    shared_counts = {}
    for generation, colors in generation_data.items():
        shared_counts[generation] = {}
        for color, agents_flags in colors.items():
            shared_agents = 0
            flag_count = Counter(len(v) for v in agents_flags.values())
            for agent_count, num_agents in flag_count.items():
                if agent_count >= min_shared:
                    shared_agents += num_agents
            shared_counts[generation][color] = shared_agents
    return shared_counts

def plot_common_flags(common_counts):
    generations = sorted(common_counts.keys())
    plt.figure(figsize=(14, 8))
    
    # Plot data for each color
    for color in ["black_agents", "white_agents"]:
        common_flags = [common_counts[gen][color] for gen in generations if color in common_counts[gen]]
        plt.plot(generations, common_flags, marker='o', linestyle='-', label=f'{color}')

    plt.xlabel('Generation')
    plt.ylabel('Number of Agents with 2 or More Shared Flags')
    plt.title('Number of Agents with 2 or More Shared Flags per Color')
    plt.xticks(generations)
    plt.legend(title="Agent Color")
    plt.grid(True)
    plt.tight_layout()
    plt.show()