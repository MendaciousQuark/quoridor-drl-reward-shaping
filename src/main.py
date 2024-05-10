import argparse

def graphing(args):
    from graphing.read_current_diversity import read_agent_data, plot_genetic_diversity 
    attributes = read_agent_data(args.base_path, args.gen)
    plot_genetic_diversity(attributes)

    from graphing.read_generational_diversity import read_all_generations, calculate_differences, plot_differences
    generation_data = read_all_generations(args.base_path, args.common_name_prefix)
    differences = calculate_differences(generation_data)
    #plot_differences(differences)

    from graphing.read_generational_diversity import plot_differences_line_graph
    plot_differences_line_graph(generation_data)

    from graphing.shared_flags import count_shared_flags, plot_common_flags, read_all_generations_shared_flags
    generation_data_shared_flags = read_all_generations_shared_flags(args.base_path, args.common_name_prefix)
    common_counts = count_shared_flags(generation_data_shared_flags)
    plot_common_flags(common_counts)

    from graphing.cummulative_line_graph import read_all_generations_cummulative_line, plot_cumulative_configs
    generation_data_cummulative = read_all_generations_cummulative_line(args.base_path, args.common_name_prefix)
    plot_cumulative_configs(generation_data_cummulative)

    from graphing.compare_best_agents import compare_generation_winners, plot_flag_trends
    winning_flags = compare_generation_winners(args.base_path, args.common_name_prefix, range(1, 24))
    plot_flag_trends(winning_flags)
    
    from graphing.compare_best_agents import aggregate_flags_and_scores, plot_flags_vs_scores
    df = aggregate_flags_and_scores(args.base_path, args.common_name_prefix, range(1, 24))
    plot_flags_vs_scores(df)

def main():
    parser = argparse.ArgumentParser(description='Train or play the game.')
    parser.add_argument('--mode', choices=['train', 'play', 'ground-truth', 'baseline', 'diversity'], default='train', help='Mode to run the game. Choices are "train", "play", "baseline", "diversity" or "ground-truth". Default is "train".')

    parser.add_argument('--mode', choices=['train', 'play', 'ground_truth', 'train_baseline'], default='train', help='Mode to run the game. Choices are "train", "play" or "ground_truth", "train_baseline". Default is "train".')
    
    #arguments for train mode
    parser.add_argument('--with_ground_truths', action='store_true', help='Train with ground truths. Default is False. Note: This argument is only used in train mode.')
    parser.add_argument('--use_pretrained', action='store_true', help='Use pretrained models. Default is False. Note: This argument is only used in train mode.')
    parser.add_argument('--slow', action='store_true', help='Slow down the training process. Default is False. Note: This argument is only used in train mode.')
    parser.add_argument('--verbose', action='store_true', help='Print verbose output. Default is False. Note: This argument is only used in train mode.')
    parser.add_argument('--observe', action='store_true', help='Observe the training process. Default is False. Note: This argument is only used in train mode.')
    parser.add_argument('--observe_from', type=int, nargs='+', default=[0, 11, 21, 31, 41, 51, 61, 71, 81, 91], help='Episodes to observe from. Default is [0, 11, 21, 31, 41, 51, 61, 71, 81, 91]. Note: This argument is only used in train mode.')
    parser.add_argument('--observe_until', type=int, nargs='+', default=[5, 15, 25, 35, 45, 55, 65, 75, 85, 95], help='Episodes to observe until. Default is [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]. Note: This argument is only used in train mode.')
    parser.add_argument('--batch_episodes', type=int, default=1000, help='Number of episodes per batch. Default is 1000. Note: This argument is only used in train mode.')
    parser.add_argument('--batch_length', type=int, default=25, help='Number of moves per batch. Default is 25. Note: This argument is only used in train mode.')
    parser.add_argument('--batches_per_generation', type=int, default=2, help='Number of batches per generation. Default is 2. Note: This argument is only used in train mode.')
    parser.add_argument('--number_of_agents', type=int, default=10, help='Number of agents to train. Default is 10. Note: This argument is only used in train mode.')
    parser.add_argument('--learn_movement', action='store_true', help='Learn only movement actions. Default is False. Note: This argument is only used in train mode.')
    parser.add_argument('--delete_after', type=int, default=0, help='Delete models after a certain number of generations. Default is 0. Set as 0 for no deletion. Note: This argument is only used in train mode.')

    #arguments for play mode
    parser.add_argument('--colour', choices=['white', 'black'], default='white', 
                        help='Color for play mode. Choices are "white" or "black". Default is "white". Note: This argument is only used in play mode.')    
    parser.add_argument('--game-mode', choices=['pve', 'pvp', 'eve'], default='pve', help='Play as a human vs bot. Default is False. Note: This argument is only used in play mode.')
    
    #arguments for ground-truth mode
    parser.add_argument('--num', type=int, default=1, help='Number of ground truths to create. Default is 1. Note: This argument is only used in ground-truth mode.')
    
    #arguments for diversity mode
    parser.add_argument('--gen', type=int, default=0, help='Generation to calculate diversity. Default is 0. Note: This argument is only used in diversity mode.')
    parser.add_argument('--base_path', type=str, default='src/trained_models/DQNagents', help='Base path for the data. Default is "data". Note: This argument is only used in diversity mode.')
    parser.add_argument('--common_name_prefix', type=str, default='gen_', help='Common name prefix for the data. Default is "gen_". Note: This argument is only used in diversity mode.')

    args = parser.parse_args()

    if args.mode == 'train':
        from models.training_setup import init_training
        init_training(args.with_ground_truths, args.use_pretrained, args.learn_movement, args.slow, args.verbose, args.observe,
               args.observe_from, args.observe_until, args.batch_episodes, args.batch_length,
               args.batches_per_generation, args.number_of_agents, args.delete_after)
    elif args.mode == 'baseline':
        from models.training_setup import init_training
        init_training(args.with_ground_truths, args.use_pretrained, args.learn_movement, args.slow, args.verbose, args.observe,
               args.observe_from, args.observe_until, args.batch_episodes, args.batch_length,
               args.batches_per_generation, args.number_of_agents, args.base_path)
    elif args.mode == 'play':
        from game.game import Game
        game = Game()
        game.play(args.colour, args.game_mode)
    elif args.mode == 'ground_truth':
        from utils.create_groundtruth import creatGroundTruth
        for _ in range(args.num):
            creatGroundTruth()
    elif args.mode == 'diversity':
        graphing(args)

if __name__ == '__main__':
    main()
