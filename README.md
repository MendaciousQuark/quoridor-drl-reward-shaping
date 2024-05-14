Deep Reinforcement Learning Quoridor Agent

This repository contains the implementation of a deep reinforcement learning (DRL) agent trained to play the game of Quoridor. The project leverages adversarial training strategies, imitation learning, and genetic algorithms to optimize the reward functions and enhance the learning efficiency of the agents.
Project Overview

This project aims to develop and evaluate an unsupervised adversarial training strategy for generating and optimizing reward functions within DRL systems using the board game Quoridor as a test environment. The training combines DRL with Imitation Learning (IL) and Genetic Algorithms (GA) to streamline the learning process and improve agent performance.
Features
    Deep Q-Networks (DQN): Utilizes TensorFlow to construct and train the neural network models.
    Adversarial Training: Implements adversarial strategies to challenge the agents continuously, enhancing their adaptability and robustness.
    Imitation Learning: Provides initial guidance to agents by mimicking expert moves, accelerating the learning process.
    Genetic Algorithms: Fine-tunes neural network architectures and learning parameters to optimize performance.

Installation
    Clone the repository using html:
    git clone https://github.com/uol-feps-soc-comp3931-2324-classroom/final-year-project-MendaciousQuark.git
    Or using ssh: 
    git clone git@github.com:uol-feps-soc-comp3931-2324-classroom/final-year-project-MendaciousQuark.git

    Install the required dependencies:
    pip install -r requirements.txt
Usage
Training and Evaluation

The main script for training and evaluating the agents is main.py. This script supports various modes of operation, which can be specified using command-line arguments.
Command-Line Arguments
    --mode: Mode to run the script. Choices are train, play, baseline, compete-all, diversity, or ground-truth. Default is train.
    --with_ground_truths: Train with ground truths (only used in train mode).
    --use_pretrained: Use pretrained models (only used in train mode).
    --slow: Slow down the training process (only used in train mode).
    --verbose: Print verbose output (only used in train mode).
    --observe: Observe the training process (only used in train mode).
    --observe_from: Episodes to observe from (only used in train mode).
    --observe_until: Episodes to observe until (only used in train mode).
    --batch_episodes: Number of episodes per batch (only used in train mode).
    --batch_length: Number of moves per batch (only used in train mode).
    --batches_per_generation: Number of batches per generation (only used in train mode).
    --number_of_agents: Number of agents to train (only used in train mode).
    --learn_movement: Learn only movement actions (only used in train mode).
    --delete_after: Delete models after a certain number of generations (only used in train mode).
    --colour: Color for play mode (white or black) (only used in play mode).
    --game-mode: Play as a human vs bot (pve, pvp, eve) (only used in play mode).
    --num: Number of ground truths to create (only used in ground-truth mode).
    --gen: Generation to calculate diversity (only used in diversity mode).
    --base_path: Base path for the data (only used in diversity mode).
    --common_name_prefix: Common name prefix for the data (only used in diversity mode).

Example Usage
Train Mode



Train Mode
python main.py --mode train --with_ground_truths --verbose

Play Mode
python main.py --mode play --colour white --game-mode pve

Playing Commands

    move or m: Move a pawn to an adjacent cell.
    place or p: Place a wall on the board.
    jump or j: Jump over a pawn.
    help: Get more information on a specific action.
Detailed Commands
Move

The move action is used to move a pawn to an adjacent cell. The start and end locations, as well as the direction of movement, must be provided. The start and end locations should be in the format a1 or i9.
Example:
move up a1 a2

Place

The place action is used to place a wall on the board. The location and orientation of the wall must be provided. Walls can be placed horizontally or vertically. Vertical walls are placed to the left of the location and extend downwards. Horizontal walls are placed above the location and extend to the right. Walls are two cells long and cannot overlap.
Example:
place h a1

Jump

The jump action is used to jump over a pawn. The start and end locations and the direction of the jump must be provided. A jump must be straight (in the direction of the opponent) if possible. If a jump is not straight, a jump may be diagonal. For diagonal jumps, remember to take into account the orientation of the jump. The start and end locations should be in the format a1 or i9. The direction of the jump should be up, down, left, or right.
Example:
jump a1 a3 up

Help Command

To get more information on a specific action, use the help command followed by the action (move, place, jump).
Example: 
help move

Graphing Functionality

The graphing function generates various graphs to visualize the diversity and performance of the agents across generations (NOTE: this requires existing models). It includes the following steps:
    Read and plot current diversity.
    Read all generations and calculate differences.
    Plot line graphs of differences.
    Count and plot shared flags.
    Read and plot cumulative line graphs.
    Compare and plot trends of the best agents.

Development and Testing
    Programming Language: Python
    Libraries: TensorFlow, Pytest
    Development Tools: Git, GitHub Copilot
    Environment: Primarily developed on CPUs

Acknowledgements

This project was developed as part of an academic requirement for the degree of MEng Computer Science with Artificial Intelligence at the University of Leeds. Special thanks to my supervisor and the School of Computing for their support and guidance.


