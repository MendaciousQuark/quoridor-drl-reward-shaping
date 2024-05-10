from utils.utils import get_next_directory_number
import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

def read_all_generations(base_path, common_name_prefix):
    max_generation = get_next_directory_number(base_path, common_name_prefix) - 1
    generation_data = {}
    for generation in range(1, max_generation + 1):
        attributes = defaultdict(list)
        colors = ["black_agents", "white_agents"]
        for color in colors:
            color_path = os.path.join(base_path, f"{common_name_prefix}{generation}", color)
            if os.path.exists(color_path):
                for agent_dir in os.listdir(color_path):
                    agent_path = os.path.join(color_path, agent_dir, "flags.json")
                    if os.path.exists(agent_path):
                        with open(agent_path, 'r') as file:
                            data = json.load(file)
                            for key, value in data.items():
                                attributes[key].append(value)
        generation_data[generation] = {key: sum(value) for key, value in attributes.items()}
    return generation_data

def calculate_differences(generation_data):
    differences = {}
    generations = sorted(generation_data.keys())
    for i in range(1, len(generations)):
        current_gen = generations[i]
        previous_gen = generations[i - 1]
        current_data = generation_data[current_gen]
        previous_data = generation_data[previous_gen]
        differences[current_gen] = {}
        for key in current_data:
            current_count = current_data[key]
            previous_count = previous_data.get(key, 0)
            differences[current_gen][key] = current_count - previous_count
    return differences

def plot_differences(differences):
    for gen, diff_data in differences.items():
        flags = list(diff_data.keys())
        diff_counts = list(diff_data.values())

        plt.figure(figsize=(12, 8))
        plt.bar(flags, diff_counts, color='salmon')
        plt.xlabel('Flags')
        plt.ylabel(f'Difference in True Count from Gen {gen-1} to Gen {gen}')
        plt.title(f'Differences in Flag True Counts from Gen {gen-1} to Gen {gen}')
        plt.xticks(rotation=90)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def plot_differences_line_graph(generation_data):
    fig, ax = plt.subplots(figsize=(14, 8))
    generations = sorted(generation_data.keys())
    flags = list(generation_data[generations[0]].keys())  # assuming all generations have the same flags

    # Prepare data for each flag across generations
    for flag in flags:
        values = [generation_data[gen].get(flag, 0) for gen in generations]
        ax.plot(generations, values, marker='o', label=flag)  # Plot each flag as a separate line

    ax.set_xlabel('Generation')
    ax.set_ylabel('Number of Agents with Flag Set to True')
    ax.set_title('Evolution of Flag Settings Across Generations')
    ax.legend(title='Flags', bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
    plt.xticks(generations)  # Ensure all generations are marked
    plt.grid(True)
    plt.tight_layout()
    plt.show()