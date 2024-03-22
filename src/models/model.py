from utils import UP, DOWN, LEFT, RIGHT, distance
from utils import getDirectionIndex, opposingPawnAdjacent, validLocation, locationToCell, getCellDirection, moveNumberToLetter
from logic.move_validation import validateMove
from logic.board_to_graph import boardToGraph
from logic.a_star import aStar
from game import Move
import pdb

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
        self.action_state_movements = []
        self.white_position_memory = []
        self.black_position_memory = []
        self.reward_memory = []
        self.last_action = None
        
    def find_legal_moves(self, state):
        self.action_state = []
        current_position = state['board_object'].pawn_positions[self.colour]
        # walls = []
        # if(self.last_action == None):
        #     walls = self.find_legal_walls(state)
        # elif(90000 <= self.last_action < 100000):
        #     walls = self.find_legal_walls(state)
        walls = self.find_legal_walls(state)
        movement = self.find_legal_movement(state, current_position)
        if(len(walls) > 0):
            self.action_state.extend(walls)
        if(len(movement) > 0):
            self.action_state.extend(movement)
        self.action_state_movements = movement

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
                # if(move_with_id[0].action == 'jump'):
                #     pdb.set_trace()
                if validateMove(move_with_id[0], state['board_object'], self.pawns[colour])[0]:
                    legal_moves.append(move_with_id)
            except Exception as e:
                continue
        #pdb.set_trace()
        return legal_moves

    def calculate_rewards(self, state):
        
        # abs diff sum of distance from goal
        #will need distance for both pawns multiple times, so calculate it once
        white_path, black_path = self.determine_best_paths(state)
        if len(white_path) == 0 or len(black_path) == 0:
            return -10000
        current_reward = self.distance_difference(state, white_path, black_path) + self.distance_from_goal_row(state) 
        current_reward += self.defeat_or_victory() - self.wall_difference_penalty() + self.changed_memory_reward(state)
        past_average_reward = 1
        if len(self.reward_memory) > 1:
            past_average_reward = sum(self.reward_memory)/len(self.reward_memory)
        self.reward_memory.append(current_reward)
        
        actual_reward = current_reward - past_average_reward
        
        return actual_reward

    def determine_best_paths(self, state):
        black_end = [cell.position for cell in state['board'][8]]
        black_start = tuple(self.pawns['black'].position)
        black_path = aStar(boardToGraph(state['board']), 'black', black_start, black_end)
        
        #repeat for white (graph needs to reinitiated as a_star modifies the graph)
        white_end = [cell.position for cell in state['board'][0]]
        white_start = tuple(self.pawns['white'].position)
        white_path = aStar(boardToGraph(state['board']), 'white', white_start, white_end)
        
        return white_path, black_path 

    def distance_difference(self, state, white_path, black_path):
        actual_distance = len(white_path) - 1 if state['turn'] % 2 == 0 else len(black_path) -1
        opponent_distance = len(black_path) - 1 if state['turn'] % 2 == 0 else len(white_path) - 1
        return actual_distance - opponent_distance * 10 #*10 to make it more significant
    
    def defeat_or_victory(self):
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
        changed_memory_reward += counter/len(unique_positions)*10
        
        return changed_memory_reward