from utils import UP, DOWN, LEFT, RIGHT, distance
from utils import getDirectionIndex, opposingPawnAdjacent, validLocation, locationToCell, getCellDirection, moveNumberToLetter
from logic.move_validation import validateMove
from logic.board_to_graph import boardToGraph
from logic.a_star import aStar
from .reward_normalisation import RewardNormalizer  
from game import Move
import json
import os
import random
import pdb

class Model:
    def __init__(self, colour, pawns, name='Bot', description='Bot', flags_path='src/trained_models/DQNagents/gen_0/white_agents/agent_0/flags.json'):
        self.name = name
        self.normalizer = RewardNormalizer()
        #'black' or 'white'
        self.colour = colour
        self.description = description
        #the pawns representing players [white_pawn, black_pawn]
        self.pawns = pawns
        #flags representing what rewards to use
        self.flags_path = flags_path  # Default path for storing flags
        self.flags = {}
        self.initialize_flags()

        # ... other attributes
        self.action_state = []
        self.action_state_movements = []
        self.white_position_memory = []
        self.black_position_memory = []
        self.reward_memory = []
        self.last_action = None
        
    def find_legal_moves(self, state):
        self.action_state = []
        current_position = state['board_object'].pawn_positions[self.colour]
        movement = self.find_legal_movement(state, current_position)
        if self.last_action is None or 90000 <= self.last_action <= 98811:
            walls = self.find_legal_walls(state)
            if len(walls) > 0:
                self.action_state.extend(walls)
        if len(movement) > 0:
            self.action_state.extend(movement)
        self.action_state_movements = movement
        return self.action_state

    def add_id_to_place(self, place, i, j):
        id =  None
        forced_integer_part = '9'
        location_part = f'{i}{j}'
        orientation_part = '0' if place.orientation == 'horizontal' else '1'
        colour_part = '0' if place.colour == 'white' else '1'
        id = int(forced_integer_part + location_part + orientation_part + colour_part)
        return (place, id)

    def add_id_to_movement(self, move, opponent_direction=None, jump_direction=None):
        id =  None
        
        if move.action == 'move':
            if move.direction == UP:
                id = 0
            elif move.direction == DOWN:
                id = 1
            elif move.direction == LEFT:
                id = 2
            elif move.direction == RIGHT:
                id = 3
            else:
                id = -1
        elif move.action == 'jump':
            if jump_direction == opponent_direction:
                id = 6
            elif jump_direction == LEFT or jump_direction == UP:
                id = 4
            elif jump_direction == RIGHT or jump_direction == DOWN:
                id = 5
            else:
                id = -1
        return (move, id)

    def find_legal_walls(self, state):
        '''
        for horizontal walls:
        - check from j = 0 to j = 7, and from i = 1 to i = 8 (inclusive) (walls are two cells wide)
        for vertical walls:
        - check from j = 1 to j = 8, and from i = 0 to i = 7 (inclusive) (walls are two cells tall)
        
        
        I have celled walls finding function. Already found since using state, and use tem to determine definite illegal walls (blocking etc.) should speed things up
        
        '''
        check_vertical = False
        check_horizontal = False
        partially_legal_walls = []
        colour = 'white' if state['turn'] % 2 == 0 else 'black'
        for i, row in enumerate(state['board']):
            for j, cell in enumerate(row):
                #determine if it makes sense to check for a vertical or horizontal wall
                check_vertical = i<= 7 and (1 <= j <= 8)
                check_horizontal = (1 <= i <= 8) and j <= 7
                
                #convert the current position to the move format (e.g. [1, 0] -> 'a2' (when i = 1 = 2, j = 0 = a))
                position_formatted = moveNumberToLetter(j) + str(9 - i)
                
                if check_vertical:
                    #crete a move object for the vertical wall placement
                    orientation = 'vertical'
                    #if the cell is already walled, skip it as it must be an illegal wall
                    if not (cell in state['walled_cells'][orientation]):
                        move_and_id = self.add_id_to_place(Move(colour, position_formatted, None, 'place', None, None, orientation), i, j)
                        partially_legal_walls.append(move_and_id)
                    
                if check_horizontal:
                    #crete a move object for the horizontal wall placement
                    orientation = 'horizontal'
                    #if the cell is already walled, skip it as it must be an illegal wall
                    if not(cell in state['walled_cells'][orientation]):
                        move_and_id = self.add_id_to_place(Move(colour, position_formatted, None, 'place', None, None, orientation), i, j)
                        partially_legal_walls.append(move_and_id)
        
        legal_walls = []
        for move_with_id in partially_legal_walls:
            try:
                if validateMove(move_with_id[0], state['board_object'], self.pawns[colour])[0]:
                    legal_walls.append(move_with_id)
            except Exception as e:
                continue
        return legal_walls

    def find_legal_movement(self, state, current_position):
        moves_to_check = []
        colour = self.colour
        adjacent_opposing_pawn = opposingPawnAdjacent(colour, state['board'], locationToCell(*current_position, state['board']))
        #if there is an opposing pawn adjacent to the current pawn
        if(adjacent_opposing_pawn[0]):
            # create all possible jump moves in the direction of the opposing pawn
            opponent_direction = getCellDirection(adjacent_opposing_pawn[1], locationToCell(*current_position, state['board']))
            
            directions_to_visit = []
            if(opponent_direction == UP):
                directions_to_visit = [UP, LEFT, RIGHT]
            elif(opponent_direction == DOWN):
                directions_to_visit = [DOWN, LEFT, RIGHT]
            elif(opponent_direction == LEFT):
                directions_to_visit = [LEFT, UP, DOWN]
            elif(opponent_direction == RIGHT):
                directions_to_visit = [RIGHT, UP, DOWN]
            
            for direction in directions_to_visit:
                #convert the current position to the move format (e.g. [1, 0] -> 'a2' (when i = 1 = 2, j = 0 = a))
                start_formatted = moveNumberToLetter(current_position[1]) + str(9 - current_position[0])
                #determine the end position of the jump move and format it
                end_position = getDirectionIndex(adjacent_opposing_pawn[1].position, direction)
                if(validLocation(*end_position)):
                    end_formatted = moveNumberToLetter(end_position[1]) + str(9 - end_position[0])
                    #convert the direction to a string for the move object
                    jump_direction_formatted = 'up' if direction == UP else 'down' if direction == DOWN else 'left' if direction == LEFT else 'right'
                    #create the move object and add it to the list of moves to check
                    move_and_id = self.add_id_to_movement(Move(colour, start_formatted, end_formatted, 'jump', None, jump_direction_formatted, None), opponent_direction, direction)
                    moves_to_check.append(move_and_id)
                
        #create all possible moves in the four cardinal directions
        for direction in [UP, DOWN, LEFT, RIGHT]:
            #convert the current position to the move format (e.g. [1, 0] -> 'a2' (when i = 1 = 2, j = 0 = a))
            start_formatted = moveNumberToLetter(current_position[1]) + str(9-current_position[0])
            #determine the end position of the move and format it
            end_position = getDirectionIndex(current_position, direction)
            if(validLocation(*end_position)):
                end_formatted = moveNumberToLetter(end_position[1]) + str(9-end_position[0])
                #convert the direction to a string for the move object
                direction_formatted = 'up' if direction == UP else 'down' if direction == DOWN else 'left' if direction == LEFT else 'right'
                #create the move object and add it to the list of moves to check
                move_and_id = self.add_id_to_movement(Move(colour, start_formatted, end_formatted, 'move', direction_formatted, None, None))
                moves_to_check.append(move_and_id)
        
        legal_moves = []
        for move_with_id in moves_to_check:
            try:
                if validateMove(move_with_id[0], state['board_object'], self.pawns[colour])[0]:
                    legal_moves.append(move_with_id)
            except Exception as e:
                continue
        return legal_moves

    def initialize_flags(self, available_flags=None):
        '''
            Initialize flags at random if they do not exist. If the flags file does not exist, it initializes the flags
            with random values based on a mutation factor.
            
            :param flags_list: A list of flag names to initialize. If None, uses a default list.
            :param mutation_factor: Determines the probability of a flag being True. Defaults to 0.5 for equal chances.
        '''
        if not os.path.exists(self.flags_path):
            print(f"No existing flags found at {self.flags_path}. Initializing with a random subset of active flags.")
            if available_flags is None:
                available_flags = [
                    'defeat_or_victory', 'wall_difference_penalty', 'changed_memory_reward', 
                    'distance_from_goal_row', 'distance_difference', 'a_star_distance',
                    'a_star_distance_opponent', 'distance_from_nearest_edge', 'distance_from_nearest_wall',
                    'average_distance_from_walls', 'average_oppononent_distance_from_walls', 'average_distance_between_walls',
                    'furthest_distance_between_walls', 'closest_distance_between_walls', 'enemy_wall_adjacency',
                    'self_wall_adjacency', 'distance_from_opponent', 'own_wall_amount', 'opponent_wall_amount',
                ]  #flags represent the names of the functions to be used as rewards

            # Initialize all flags to False initially
            initial_flags = {flag: False for flag in available_flags}

            # Randomly determine the number of flags to set to True, ensuring at least one is selected
            active_flag_count = random.randint(1, len(available_flags))

            # Randomly select a subset of flags to activate
            flags_to_activate = random.sample(available_flags, active_flag_count)

            # Set the chosen flags to True
            for flag in flags_to_activate:
                initial_flags[flag] = True

            self.flags = initial_flags
            self.store_flags()
        else:
            # If the file exists, load the existing flags
            self.load_flags()

    def store_flags(self, file_path=None):
        path = file_path if file_path else self.flags_path
        
        # Ensure 'flags.json' is at the end of the path
        if not path.endswith('flags.json'):
            path = os.path.join(path, 'flags.json')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w') as file:
            # Use indent=4 for pretty printing, sort_keys=True to sort the keys alphabetically
            json.dump(self.flags, file, indent=4, sort_keys=True)

    def load_flags(self, file_path=None):
        path = file_path if file_path else self.flags_path

        # Ensure 'flags.json' is at the end of the path
        if not path.endswith('flags.json'):
            path = os.path.join(path, 'flags.json')

        if os.path.exists(path):
            with open(path, 'r') as file:
                self.flags = json.load(file)
        else:
            self.flags = {}

    def mutate_flags(self, mutation_factor=0.05, num_mutations=1):
        mutations_count = 0
        flags_to_mutate = list(self.flags.keys())  # Get a list of all flag keys
        random.shuffle(flags_to_mutate)  # Shuffle the list to select flags randomly
        for key in flags_to_mutate:
            if random.random() < mutation_factor and mutations_count < num_mutations:
                self.flags[key] = not self.flags[key]
            mutations_count += 1

    def calculate_rewards(self, state):
        total_reward = 0
        for key in self.flags.keys():
            if self.flags[key]:
                # Assuming methods named after keys exist and calculate partial rewards
                component_reward = getattr(self, key)(state)
                total_reward += self.normalizer.normalize(component_reward)

        return float(format(total_reward, '.5g'))

    def determine_best_paths(self, state):
        black_end = [cell.position for cell in state['board'][8]]
        black_start = tuple(self.pawns['black'].position)
        black_path = aStar(boardToGraph(state['board']), 'black', black_start, black_end)
        
        #repeat for white (graph needs to reinitiated as a_star modifies the graph)
        white_end = [cell.position for cell in state['board'][0]]
        white_start = tuple(self.pawns['white'].position)
        white_path = aStar(boardToGraph(state['board']), 'white', white_start, white_end)
        
        return white_path, black_path 

    def distance_difference(self, state):
        white_path, black_path = self.determine_best_paths(state)
        actual_distance = len(white_path) - 1 if state['turn'] % 2 == 0 else len(black_path) -1
        opponent_distance = len(black_path) - 1 if state['turn'] % 2 == 0 else len(white_path) - 1
        return actual_distance - opponent_distance * 10 #*10 to make it more significant
    
    def a_star_distance(self, state):
        white_path, black_path = self.determine_best_paths(state)
        actual_distance = len(white_path) - 1 if state['turn'] % 2 == 0 else len(black_path) -1
        return actual_distance
    
    def a_star_distance_opponent(self, state):
        white_path, black_path = self.determine_best_paths(state)
        opponent_distance = len(black_path) - 1 if state['turn'] % 2 == 0 else len(white_path) - 1
        return opponent_distance

    def defeat_or_victory(self, _):
        reward = 0
        colour = self.colour
        #if board is in a victory or defeat state, return the reward for that state
        
        if(self.pawns['white'].position[0] == 0 and colour == 'white'):
            #if white won and it's white's turn, reward 1000
            reward += 1000
        if(self.pawns['black'].position[0] == 8 and colour == 'white'):
            #if black won and it's white's's turn, reward -1000
            reward -= 1000
        if(self.pawns['white'].position[0] == 0 and colour == 'black'):
            #if white won and it's blacks turn reward -1000
            reward -= 1000
        if(self.pawns['black'].position[0] == 8 and colour == 'black'):
            #if black won and it's black's turn reward 1000
            reward += 1000
        
        #returns 0 if both players in winning state or neither are else -1000 for defeat and 1000 for victory
        return reward

    def distance_from_goal_row(self, state):
        #rewards for moving up the board
        distance_from_goal_row = 0
        if state['turn'] % 2 == 0:
            if self.pawns['white'].position[0] > 6:
                distance_from_goal_row += -10
            elif self.pawns['white'].position[0] > 4:
                distance_from_goal_row += -5
            elif self.pawns['white'].position[0] > 2:
                distance_from_goal_row += -2
            elif self.pawns['white'].position[0] > 1:
                distance_from_goal_row += -1
            elif self.pawns['white'].position[0] == 0:
                distance_from_goal_row += 1000
        else:
            if self.pawns['black'].position[0] < 2:
                distance_from_goal_row += -10
            elif self.pawns['black'].position[0] < 4:
                distance_from_goal_row += -5
            elif self.pawns['black'].position[0] < 6:
                distance_from_goal_row += -2
            elif self.pawns['black'].position[0] < 7:
                distance_from_goal_row += -1
            elif self.pawns['black'].position[0] == 8:
                distance_from_goal_row += 1000
        return distance_from_goal_row

    def distance_from_nearest_edge(self, state):
        #current position
        current_position = state['pieces'][self.colour]
        #distance from the nearest edge
        return min(abs(0 - current_position[1]), abs(8 - current_position[1]))
    
    def changed_memory_reward(self, state):
        #add position to memory
        self.white_position_memory.append(self.pawns['white'].position) if state['turn'] % 2 == 0 else self.black_position_memory.append(self.pawns['black'].position)
        #if more than 10 moves rememberd, remove the oldest
        if len(self.white_position_memory) > 50:
            self.white_position_memory.pop(0)
        
        changed_memory_reward = 0
        counter = 0
        unique_positions = set(tuple(position) for position in self.white_position_memory) if state['turn'] % 2 == 0 else set(tuple(position) for position in self.black_position_memory)   
        if (state['turn'] % 2 == 0) and len(self.white_position_memory) > 1:
            for unique_position in unique_positions:
                # count how often the position has occurred
                for position in self.white_position_memory:
                    if tuple(position) == unique_position:
                        counter += 1
        elif (state['turn'] % 2 != 0) and len(self.black_position_memory) > 1:
            for unique_position in unique_positions:
                # count how often the position has occurred
                for position in self.black_position_memory:
                    if tuple(position) == unique_position:
                        counter += 1
        changed_memory_reward += counter/max(len(unique_positions), 1)
        
        return changed_memory_reward

    def wall_difference_penalty(self, _):
        #determin colour being represented
        difference = 0
        if(self.colour == 'white'):
            #return the difference in walls between the two players or 0 if the player has more walls than the opponent
            difference =  min(self.pawns['white'].walls - self.pawns['black'].walls, 0)
        else:
            #same as above but for black
            difference =  min(self.pawns['black'].walls - self.pawns['white'].walls, 0)
        return difference
    
    def own_wall_amount(self, state):
        return self.pawns[self.colour].walls
    
    def opponent_wall_amount(self, state):
        return self.pawns['black' if self.colour == 'white' else 'white'].walls

    def enemy_wall_adjacency(self, state):
        horizontal_walled_cells = state['walled_cells']['horizontal']
        vertical_walled_cells = state['walled_cells']['vertical']
        walled_cells = horizontal_walled_cells + vertical_walled_cells
        walls_adjacent = 0
        #for each wall in walled cells check the adjacent cells for the opponent
        for walled_cell in walled_cells:
            if(distance(state['pieces']['black' if self.colour == 'white' else 'white'], walled_cell.position) == 1):
                walls_adjacent += 1
        return walls_adjacent
    
    def self_wall_adjacency(self, state):
        horizontal_walled_cells = state['walled_cells']['horizontal']
        vertical_walled_cells = state['walled_cells']['vertical']
        walled_cells = horizontal_walled_cells + vertical_walled_cells
        walls_adjacent = 0
        #for each wall in walled cells check the adjacent cells for the player
        for walled_cell in walled_cells:
            if(distance(state['pieces'][self.colour], walled_cell.position) == 1):
                walls_adjacent += 1
        return -1*walls_adjacent #negative as it is a penalty
    
    def distance_from_nearest_wall(self, state):
        horizontal_walled_cells = state['walled_cells']['horizontal']
        vertical_walled_cells = state['walled_cells']['vertical']
        walled_cells = horizontal_walled_cells + vertical_walled_cells
        closest_distance = 100000
        current_position = state['pieces'][self.colour]
        for walled_cell in walled_cells:
            closest_distance = min(closest_distance, distance(current_position, walled_cell.position))
        return closest_distance
    
    def average_distance_from_walls(self, state):
        horizontal_walled_cells = state['walled_cells']['horizontal']
        vertical_walled_cells = state['walled_cells']['vertical']
        walled_cells = horizontal_walled_cells + vertical_walled_cells
        total_distance = 0
        current_position = state['pieces'][self.colour]
        for walled_cell in walled_cells:
            total_distance += distance(current_position, walled_cell.position)
        return total_distance/max(len(walled_cells), 1)
    
    def average_oppononent_distance_from_walls(self, state):
        horizontal_walled_cells = state['walled_cells']['horizontal']
        vertical_walled_cells = state['walled_cells']['vertical']
        walled_cells = horizontal_walled_cells + vertical_walled_cells
        total_distance = 0
        current_position = state['pieces']['black' if self.colour == 'white' else 'white']
        for walled_cell in walled_cells:
            total_distance += distance(current_position, walled_cell.position)
        return total_distance/max(len(walled_cells), 1)
    
    def average_distance_between_walls(self, state):
        horizontal_walled_cells = state['walled_cells']['horizontal']
        vertical_walled_cells = state['walled_cells']['vertical']
        walled_cells = horizontal_walled_cells + vertical_walled_cells
        total_distance = 0
        for i, walled_cell in enumerate(walled_cells):
            for j, other_walled_cell in enumerate(walled_cells):
                if i != j:
                    total_distance += distance(walled_cell.position, other_walled_cell.position)
        return total_distance/(max(len(walled_cells), 1)**2)
    
    def furthest_distance_between_walls(self, state):
        horizontal_walled_cells = state['walled_cells']['horizontal']
        vertical_walled_cells = state['walled_cells']['vertical']
        walled_cells = horizontal_walled_cells + vertical_walled_cells
        furthest_distance = 0
        for i, walled_cell in enumerate(walled_cells):
            for j, other_walled_cell in enumerate(walled_cells):
                if i != j:
                    furthest_distance = max(furthest_distance, distance(walled_cell.position, other_walled_cell.position))
        return furthest_distance
    
    def closest_distance_between_walls(self, state):
        horizontal_walled_cells = state['walled_cells']['horizontal']
        vertical_walled_cells = state['walled_cells']['vertical']
        walled_cells = horizontal_walled_cells + vertical_walled_cells
        closest_distance = 100000
        for i, walled_cell in enumerate(walled_cells):
            for j, other_walled_cell in enumerate(walled_cells):
                if i != j:
                    closest_distance = min(closest_distance, distance(walled_cell.position, other_walled_cell.position))
        return closest_distance
                    
    def distance_from_opponent(self, state):
        return distance(state['pieces'][self.colour], 
                           state['pieces']['black' if self.colour == 'white' else 'white'])