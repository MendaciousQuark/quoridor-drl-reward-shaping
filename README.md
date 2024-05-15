# Deep Reinforcement Learning Quoridor Agent

This repository contains the implementation of a deep reinforcement learning (DRL) agent trained to play the game of Quoridor. The project leverages adversarial training strategies, imitation learning, and genetic algorithms to optimize the reward functions and enhance the learning efficiency of the agents.

## Project Overview

This project aims to develop and evaluate an unsupervised adversarial training strategy for generating and optimizing reward functions within DRL systems using the board game Quoridor as a test environment. The training combines DRL with Imitation Learning (IL) and Genetic Algorithms (GA) to streamline the learning process and improve agent performance.

### Features
- **Deep Q-Networks (DQN)**: Utilizes TensorFlow to construct and train the neural network models.
- **Adversarial Training**: Implements adversarial strategies to challenge the agents continuously, enhancing their adaptability and robustness.
- **Imitation Learning**: Provides initial guidance to agents by mimicking expert moves, accelerating the learning process.
- **Genetic Algorithms**: Fine-tunes neural network architectures and learning parameters to optimize performance.

## Installation

1. Clone the repository using html:
       git clone https://github.com/uol-feps-soc-comp3931-2324-classroom/final-year-project-MendaciousQuark.git
   Or using ssh:
       git clone git@github.com:uol-feps-soc-comp3931-2324-classroom/final-year-project-MendaciousQuark.git

2. Install the required dependencies:
    pip install -r requirements.txt

## Usage
### Training and Evaluation

The main script for training and evaluating the agents is `main.py`. This script supports various modes of operation, which can be specified using command-line arguments.

### Command-Line Arguments by Mode

#### Train Mode
- `--mode`: Mode to run the script. Default is `train`.
- `--with_ground_truths`: Train with ground truths.
- `--use_pretrained`: Use pretrained models.
- `--slow`: Slow down the training process.
- `--verbose`: Print verbose output.
- `--observe`: Observe the training process.
- `--observe_from`: Episodes to observe from.
- `--observe_until`: Episodes to observe until.
- `--batch_episodes`: Number of episodes per batch.
- `--batch_length`: Number of moves per batch.
- `--batches_per_generation`: Number of batches per generation.
- `--number_of_agents`: Number of agents to train.
- `--learn_movement`: Learn only movement actions.
- `--delete_after`: Delete models after a certain number of generations.

#### Play Mode
(Note: Due to an unhandled bug you will need to train multiple generations of agents before playing works. Alternatively, set the file path diretly within the game.py file.)
- `--mode`: Mode to run the script.
- `--colour`: Color for play mode (white or black).
- `--game-mode`: Play as a human vs bot (`pve`, `pvp`, `eve`).

#### Diversity (graphing) Mode
- `--mode`: Mode to run the script.
- `--gen`: Generation to calculate diversity.
- `--base_path`: Base path for the data.
- `--common_name_prefix`: Common name prefix for the data.

#### Ground-Truth Mode
- `--mode`: Mode to run the script.
- `--num`: Number of ground truths to create.

#### Example Usage
**Train Mode**
python main.py --mode train --with_ground_truths --verbose

**Play Mode**
python main.py --mode play --colour white --game-mode pve

### Playing Commands

- `move` or `m`: Move a pawn to an adjacent cell.
- `place` or `p`: Place a wall on the board.
- `jump` or `j`: Jump over a pawn.
- `help`: Get more information on a specific action.

#### Detailed Commands
**Move**

The move action is used to move a pawn to an adjacent cell. The start and end locations, as well as the direction of movement, must be provided. The start and end locations should be in the format `a1` or `i9`.
Example: move up a1 a2

**Place**

The place action is used to place a wall on the board. The location and orientation of the wall must be provided. Walls can be placed horizontally or vertically. Vertical walls are placed to the left of the location and extend downwards. Horizontal walls are placed above the location and extend to the right. Walls are two cells long and cannot overlap.
Example: place h a1

**Jump**

The jump action is used to jump over a pawn. The start and end locations and the direction of the jump must be provided. A jump must be straight (in the direction of the opponent) if possible. If a jump is not straight, a jump may be diagonal. For diagonal jumps, remember to take into account the orientation of the jump. The start and end locations should be in the format `a1` or `i9`. The direction of the jump should be up, down, left, or right.
Example: jump a1 a3 up

**Help Command**

To get more information on a specific action, use the help command followed by the action (`move`, `place`, `jump`).
Example: help move

## Graphing Functionality

The graphing functionality generates various graphs to visualize the diversity and performance of the agents across generations (NOTE: this requires existing models). It includes the following steps:
- Read and plot current diversity.
- Read all generations and calculate differences.
- Plot line graphs of differences.
- Count and plot shared flags.
- Read and plot cumulative line graphs.
- Compare and plot trends of the best agents.

## Getting Started with the Codebase

To effectively understand and navigate the codebase, it is recommended to follow a specific order of study. This structured approach will help you grasp the fundamental concepts and how they interact within the framework.

### Foundation Classes
1. **Board Class**: Start with the Board class to understand the layout and basic functioning of the Quoridor game board.
2. **Cell Class**: Next, explore the Cell class to get acquainted with the properties of individual cells on the board.
3. **Pawn Class**: The Pawn class will help you understand the attributes and actions of the pawns used in the game.

### Game State to Model State Conversion
- **BoardToStateConverter Class**: This class is crucial for learning how the game state is converted into a model state that the neural network can process. Understanding this class is key for bridging the game mechanics with the learning algorithms.

### Reinforcement Learning Agent
- **DQNAgent in deep_q_learning.py**: Before moving on to training, familiarize yourself with the `DQNAgent` class in `deep_q_learning.py`. This class is essential for understanding the reinforcement learning algorithms that drive agent behavior.

### Training Flow
- **training_setup.py**: Begin understanding the training flow by reading this script. This script handles the control flow going through the IL, DRL and GA steps iteratively.
- **train.py**: Follow up with the train.py script to understand actual training process of the agents.

### Deep Learning Model and Adaptation
- **model.py**: This file is critical for understanding how the rewards are structured and how mutations in the learning process occur. It contains the definitions and functionalities related to the neural network model.

### Main Program Control
- **main.py**: This script integrates all components and shows how to control the overall program flow. It is essential for seeing how all parts of the project come together in operation.

### Additional Information
While other files in the repository provide more detailed functionalities and enhancements, the files listed above are sufficient to gain a basic understanding of the core operations of the project.


## Development and Testing
- **Programming Language**: Python
- **Libraries**: TensorFlow, Pytest
- **Development Tools**: Git, GitHub Copilot
- **Environment**: Primarily developed on CPUs

## Acknowledgements

This project was developed as part of an academic requirement for the degree of MEng Computer Science with Artificial Intelligence at the University of Leeds. Special thanks to my supervisor and the School of Computing for their support and guidance.

