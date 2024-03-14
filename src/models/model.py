from utils import UP, DOWN, LEFT, RIGHT, distance
from utils import getDirectionIndex, opposingPawnAdjacent, validLocation, locationToCell, getCellDirection, moveNumberToLetter
from logic.move_validation import validateMove
from logic.board_to_graph import boardToGraph
from logic.a_star import aStar
from game import Move
import pdb
import random
class Model:
    def __init__(self, colour, pawns, name='Bot', description='Bot'):
        self.name = name
        #'black' or 'white'
        self.colour = colour
        self.description = description
        #the pawns representing players [white_pawn, black_pawn]
        self.pawns = pawns
        # ... other attributes
        self.action_state = []
        self.white_position_memory = []
        self.black_position_memory = []
        
    def find_legal_moves(self, state):
        self.action_state = []
        current_position = state['pieces']['white' if state['turn'] % 2 == 0 else 'black']
        walls = self.find_legal_walls(state)
        movement = self.find_legal_movement(state, current_position)
        self.action_state.extend(walls)
        self.action_state.extend(movement)
    
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
        elif move.action == 'jump':
            if jump_direction == opponent_direction:
                id = 6
            else:
                if jump_direction == LEFT:
                    id = 4
                else:
                    id = 3
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
                    cell_below = locationToCell(*getDirectionIndex([i, j], DOWN), state['board']) if validLocation(*getDirectionIndex([i, j], DOWN)) else None
                    #if the cell is already walled, skip it as it must be an illegal wall
                    if not (cell in state['walled_cells'][orientation]):
                    #if the cell is above a horizontal wall, skip it as it must be an illegal vertical wall
                        #if not (cell_below in state['walled_cells']['horizontal'] and cell_below is not None):
                        move_and_id = self.add_id_to_place(Move(colour, position_formatted, None, 'place', None, None, orientation), i, j)
                        partially_legal_walls.append(move_and_id)
                    
                if check_horizontal:
                    #crete a move object for the horizontal wall placement
                    orientation = 'horizontal'
                    cell_right = locationToCell(*getDirectionIndex([i, j], RIGHT), state['board']) if validLocation(*getDirectionIndex([i, j], RIGHT)) else None
                    #if the cell is already walled, skip it as it must be an illegal wall
                    if not(cell in state['walled_cells'][orientation]):
                        #if the cell is next to a vertical wall, skip it as it must be an illegal vertical wall
                        #if not(cell_right in state['walled_cells']['vertical'] and cell_right is not None):
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
        colour = 'white' if state['turn'] % 2 == 0 else 'black'
        adjacent_opposing_pawn = opposingPawnAdjacent(colour, state['board'], locationToCell(*current_position, state['board']))
        #if there is an opposing pawn adjacent to the current pawn
        if(adjacent_opposing_pawn[0]):
            # create all possible jump moves in the direction of the opposing pawn
            opponent_direction = getCellDirection(adjacent_opposing_pawn[1], locationToCell(*current_position, state['board']))
            for direction in [opponent_direction, LEFT, RIGHT]:
                #convert the current position to the move format (e.g. [1, 0] -> 'a2' (when i = 1 = 2, j = 0 = a))
                start_formatted = moveNumberToLetter(current_position[1]) + str(9 - current_position[0])
                #determine the end position of the jump move and format it
                end_position = getDirectionIndex(current_position, direction)
                if(validLocation(*end_position)):
                    end_formatted = moveNumberToLetter(end_position[1]) + str(9 - end_position[0])
                    #convert the direction to a string for the move object
                    jump_direction_formatted = 'up' if direction == UP else 'down' if direction == DOWN else 'left' if direction == LEFT else 'right'
                    #create the move object and add it to the list of moves to check
                    move_and_id = self.add_id_to_movement(Move(colour, start_formatted, end_formatted, 'jump', None, jump_direction_formatted, None), opponent_direction, jump_direction_formatted)
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

    def calculate_rewards(self, state):
        #add position to memory
        self.white_position_memory.append(self.pawns['white'].position) if state['turn'] % 2 == 0 else self.black_position_memory.append(self.pawns['black'].position)
        #if more than 10 moves rememberd, remove the oldest
        if len(self.white_position_memory) > 50:
            self.white_position_memory.pop(0)
        changed_memory_reward = 0
        counter = 0
       
        changed_memory_reward = 0
        counter = 0
        if (state['turn'] % 2 == 0) and len(self.white_position_memory) > 1:
            unique_positions = set(tuple(position) for position in self.white_position_memory)
            for unique_position in unique_positions:
                # count how often the position has occurred
                for position in self.white_position_memory:
                    if tuple(position) == unique_position:
                        counter += 1
        elif (state['turn'] % 2 != 0) and len(self.black_position_memory) > 1:
            unique_positions = set(tuple(position) for position in self.black_position_memory)
            for unique_position in unique_positions:
                # count how often the position has occurred
                for position in self.black_position_memory:
                    if tuple(position) == unique_position:
                        counter += 1
                    # if the position has occurred more than once, punish the agent
        if counter > 1:
            changed_memory_reward = counter*0.1      
        #if the position has occured more than once, punish the agent
        if counter > 1:
            changed_memory_reward = -1*counter
        #rewards for moving up the board
        distance_from_goal_row = 0
        if state['turn'] % 2 == 0:
            if self.pawns['white'].position[0] > 6:
                distance_from_goal_row += -10
            elif self.pawns['white'].position[0] > 4:
                distance_from_goal_row += -5
            elif self.pawns['white'].position[0] > 2:
                distance_from_goal_row += -2
            elif self.pawns['white'].position[0] > 0:
                distance_from_goal_row += -1
            else:
                distance_from_goal_row += 10
        else:
            if self.pawns['black'].position[0] < 2:
                distance_from_goal_row += -10
            elif self.pawns['black'].position[0] < 4:
                distance_from_goal_row += -5
            elif self.pawns['black'].position[0] < 6:
                distance_from_goal_row += -2
            elif self.pawns['black'].position[0] < 8:
                distance_from_goal_row += -1
            else:
                distance_from_goal_row += 10
        
        # abs diff sum of distance from goal
        #will need distance for both pawns multiple times, so calculate it once
        white_path, black_path = self.determine_best_paths(state)
        white_manhattan_sum = 0
        black_manhattan_sum = 0
        for colour in ['white', 'black']:
            #determine the manhattan distance of the pawn from the end goal
            for cell in state['board'][8 if colour == 'white' else 0]:
                if colour == 'white':
                    white_manhattan_sum += distance(cell.position, self.pawns[colour].position)
                else:
                    black_manhattan_sum += distance(cell.position, self.pawns[colour].position)
        actual_distance_penalty = len(white_path) - 1 if state['turn'] % 2 == 0 else len(black_path) -1
        opponent_distance_reward = len(black_path) - 1 if state['turn'] % 2 == 0 else len(white_path) - 1
        return - actual_distance_penalty + opponent_distance_reward + distance_from_goal_row + changed_memory_reward
        
        # white_distance, black_distance = len(white_path) - 1, len(black_path) - 1 # -1 as the path includes the start position
        # #victory or defeat reward
        # victory_or_defeat_reward = self.defeat_or_victory(state)
        
        # #the reward for the distance of the opponent from the end goal
        # opponent_distance_reward = black_distance if state['turn'] % 2 == 0 else white_distance
        
        # #the reward for the difference in distance between the two pawns
        # path_difference_reward =  black_distance - white_distance if state['turn'] % 2 == 0 else  white_distance - black_distance
        
        # #the punishment for having less walls than the opponent
        # wall_difference_penalty = self.wall_difference_penalty()
        
        # #the punishment for being further from the end goal than the opponent
        # distance_penalty = white_distance if state['turn'] % 2 == 0 else black_distance
        # distance_penalty *= -1 #negate as punishment
        # #print('victory_or_defeat_reward:', victory_or_defeat_reward, 'path_difference_reward:', path_difference_reward, 'wall_difference_penalty:', wall_difference_penalty, 'opponent_distance_reward:', opponent_distance_reward, 'distance_penalty:', distance_penalty)
        # return victory_or_defeat_reward + path_difference_reward + wall_difference_penalty + opponent_distance_reward + distance_penalty
    
    def determine_best_paths(self, state):
        black_end = [cell.position for cell in state['board'][8]]
        black_start = tuple(self.pawns['black'].position)
        black_path = aStar(boardToGraph(state['board']), 'black', black_start, black_end)
        
        #repeat for white (graph needs to reinitiated as a_star modifies the graph)
        white_end = [cell.position for cell in state['board'][0]]
        white_start = tuple(self.pawns['white'].position)
        white_path = aStar(boardToGraph(state['board']), 'white', white_start, white_end)
        
        return white_path, black_path 
    
    def defeat_or_victory(self, state):
        reward = 0
        colour = 'white' if state['turn'] % 2 == 0 else 'black'
        #if board is in a victory or defeat state, return the reward for that state
        if(self.pawns['white'] == state['board'][8] and colour == 'white'):
            reward += 1000
        if(self.pawns['black'] == state['board'][0] and colour == 'black'):
            reward += 1000
        if(self.pawns['white'] == state['board'][8] and colour == 'black'):
            reward -= 1000
        if(self.pawns['black'] == state['board'][0] and colour == 'white'):
            reward -= 1000
        
        #returns 0 if both players in winning state or neither are else -1000 for defeat and 1000 for victory
        return reward
    
    def wall_difference_penalty(self):
        #determin colour being represented
        difference = 0
        if(self.colour == 'white'):
            #return the difference in walls between the two players or 0 if the player has more walls than the opponent
            difference =  min(self.pawns['white'].walls - self.pawns['black'].walls, 0)
        else:
            #same as above but for black
            difference =  min(self.pawns['black'].walls - self.pawns['white'].walls, 0)
        return difference
    