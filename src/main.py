import argparse

def main():
    parser = argparse.ArgumentParser(description='Train or play the game.')
    parser.add_argument('--mode', choices=['train', 'play', 'ground-truth'], default='train', help='Mode to run the game. Choices are "train", "play" or "ground-truth". Default is "train".')
    
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


    #arguments for play mode
    parser.add_argument('--colour', choices=['white', 'black'], default='white', 
                        help='Color for play mode. Choices are "white" or "black". Default is "white". Note: This argument is only used in play mode.')    
    parser.add_argument('--game-mode', choices=['pve', 'pvp', 'eve'], default='pve', help='Play as a human vs bot. Default is False. Note: This argument is only used in play mode.')
    
    #arguments for ground-truth mode
    parser.add_argument('--num', type=int, default=1, help='Number of ground truths to create. Default is 1. Note: This argument is only used in ground-truth mode.')
    
    args = parser.parse_args()

    if args.mode == 'train':
        from models.training_setup import init_training
        init_training(args.with_ground_truths, args.use_pretrained, args.slow, args.verbose, args.observe,
               args.observe_from, args.observe_until, args.batch_episodes, args.batch_length,
               args.batches_per_generation, args.number_of_agents)
    elif args.mode == 'play':
        from game.game import Game
        game = Game()
        game.play(args.colour, args.game_mode)
    elif args.mode == 'ground-truth':
        from utils.create_groundtruth import creatGroundTruth
        for _ in range(args.num):
            creatGroundTruth()

if __name__ == '__main__':
    main()
