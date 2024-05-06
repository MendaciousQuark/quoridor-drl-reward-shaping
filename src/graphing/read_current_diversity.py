import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

def read_agent_data(base_path, generation):
    attributes = defaultdict(list)
    colors = ["black_agents", "white_agents"]
    for color in colors:
        color_path = os.path.join(base_path, f"gen_{generation}", color)
        for agent_dir in os.listdir(color_path):
            agent_path = os.path.join(color_path, agent_dir, "flags.json")
            if os.path.exists(agent_path):
                with open(agent_path, 'r') as file:
                    data = json.load(file)
                    for key, value in data.items():
                        attributes[key].append(value)
    return attributes

def plot_genetic_diversity(attributes):
    true_counts = {key: sum(value) for key, value in attributes.items()}
    flags = list(true_counts.keys())
    counts = list(true_counts.values())

    plt.figure(figsize=(12, 8))
    plt.bar(flags, counts, color='skyblue')
    plt.xlabel('Flags')
    plt.ylabel('Number of Agents with True')
    plt.title('Number of Agents with Flag Set to True by Flag')
    plt.xticks(rotation=90)  # Rotate flag names for better readability
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to make room for label rotation
    plt.show()