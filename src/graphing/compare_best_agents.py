import os
import json
import matplotlib.pyplot as plt
import pandas as pd

def fetch_agent_flags(base_path, generation, agent_names):
    flags_dict = {}
    for agent in agent_names:
        agent_color = "black_agents" if "Black" in agent else "white_agents"
        # Extract the agent number from the agent's name
        agent_number = ''.join(filter(str.isdigit, agent))
        flags_file_path = os.path.join(base_path, f"gen_{generation}", agent_color, f"agent_{agent_number}", "flags.json")
        if os.path.exists(flags_file_path):
            with open(flags_file_path, 'r') as file:
                data = json.load(file)
                flags_dict[agent] = data
    return flags_dict

def parse_tournament_results(tournament_file):
    winners = []
    max_score = float('-inf')
    with open(tournament_file, 'r') as file:
        for line in file:
            if 'Bot' in line:
                parts = line.split('|')
                agent = parts[1].strip()
                try:
                    score = float(parts[2].strip())  # Now parsing as float
                except ValueError as e:
                    print(f"Error parsing score for {agent}: {e}")
                    continue

                if score > max_score:
                    winners = [agent]
                    max_score = score
                elif score == max_score:
                    winners.append(agent)
    return winners


def compare_generation_winners(base_path, common_name_prefix, generations):
    all_flags = {}
    for generation in generations:
        tournament_file = os.path.join(base_path, f"{common_name_prefix}{generation}", "tournament_results.txt")
        winners = parse_tournament_results(tournament_file)
        flags = fetch_agent_flags(base_path, generation, winners)
        all_flags[generation] = flags
    return all_flags

def plot_flag_trends(winning_flags):
    flag_trends = {}
    generations = sorted(winning_flags.keys())
    for gen in generations:
        for agent, flags in winning_flags[gen].items():
            for flag, value in flags.items():
                if flag not in flag_trends:
                    flag_trends[flag] = [0] * len(generations)
                if value:
                    flag_trends[flag][gen-1] += 1  # Increment if flag is True

    plt.figure(figsize=(14, 8))
    for flag, counts in flag_trends.items():
        plt.plot(generations, counts, marker='o', linestyle='-', label=flag)

    plt.xlabel('Generation')
    plt.ylabel('Number of Winners with Flag')
    plt.title('Trends of Flags in Winners Over Generations')
    plt.legend(title="Flags", loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()