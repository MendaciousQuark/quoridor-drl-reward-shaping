from utils import UP, DOWN, LEFT, RIGHT 
from utils import getDirectionIndex, opposingPawnAdjacent, validLocation, locationToCell, getCellDirection, moveNumberToLetter
from logic import validateMove, boardToGraph, aStar
from game import Move
import pdb

class Model:
    def __init__(self, colour, pawns, name='Bot', description='Bot'):
        self.name = name
        #'black' or 'white'
        self.colour = colour
        self.description = description
        #the pawns representing players [white_pawn, black_pawn]
        self.pawns = {
            'white': pawns[0],
            'black': pawns[1]
        }
        # ... other attributes
        self.action_state = []
        
    def find_legal_moves(self, state):
        current_position = state[self.colour]
        walls = self.find_legal_walls(state)
        movement = self.find_legal_movement(state, current_position)
        walls_with_id = []
        self.action_state.extend(walls)
        self.action_state.extend(movement)
    
    def add_id_to_place(self, place, i, j):
        id =  None
        forced_integer_part = '9'
        location_part = f'{i}{j}'
        orientation_part = '0' if place.orientation == 'horizontal' else '1'
        colour_part = '0' if place.colour else '1'
        id = int(forced_integer_part + location_part + orientation_part + colour_part)
        return (place, id)
    
    def add_id_to_movement(self, move, opponent_direction=None, jump_direction=None):
        id =  None
        
        if move.action == 'move':
            if move.direction == UP:
                id = 1
            elif move.direction == DOWN:
                id = 2
            elif move.direction == LEFT:
                id = 3
            elif move.direction == RIGHT:
                id = 4
        elif move.action == 'jump':
            if jump_direction == opponent_direction:
                id = 7
            else:
                if jump_direction == LEFT:
                    id = 5
                else:
                    id = 6
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
        coulour_formatted = True if self.colour == 'white' else False
        for i, row in enumerate(state['board']):
            for j, cell in enumerate(row):
                #print(f"i: {i}, j: {j}, cell: {cell}")
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
                        if not (cell_below in state['walled_cells']['horizontal']):
                            move_and_id = self.add_id_to_place(Move(coulour_formatted, position_formatted, None, 'place', None, None, orientation), i, j)
                            partially_legal_walls.append(move_and_id)
                    
                if check_horizontal:
                    #crete a move object for the horizontal wall placement
                    orientation = 'horizontal'
                    cell_right = locationToCell(*getDirectionIndex([i, j], RIGHT), state['board']) if validLocation(*getDirectionIndex([i, j], RIGHT)) else None
                    #if the cell is already walled, skip it as it must be an illegal wall
                    if not(cell in state['walled_cells'][orientation]):
                        #if the cell is next to a vertical wall, skip it as it must be an illegal vertical wall
                        if not(cell_right in state['walled_cells']['vertical']):
                            move_and_id = self.add_id_to_place(Move(coulour_formatted, position_formatted, None, 'place', None, None, orientation), i, j)
                            partially_legal_walls.append(move_and_id)
        
        legal_walls = []
        for move_with_id in partially_legal_walls:
            if validateMove(move_with_id[0], state['board_object'], self.pawns[self.colour]):
                legal_walls.append(move_with_id)
        return legal_walls
    
    def find_legal_movement(self, state, current_position):
        moves_to_check = []
        coulour_formatted = True if self.colour == 'white' else False
        
        adjacent_opposing_pawn = opposingPawnAdjacent(self.colour, state['board'], locationToCell(*current_position, state['board']))
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
                    move_and_id = self.add_id_to_movement(Move(coulour_formatted, start_formatted, end_formatted, 'jump', None, jump_direction_formatted, None), opponent_direction, jump_direction_formatted)
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
                move_and_id = self.add_id_to_movement(Move(coulour_formatted, start_formatted, end_formatted, 'move', direction_formatted, None, None))
                moves_to_check.append(move_and_id)
        
        legal_moves = []
        for move_with_id in moves_to_check:
            try:
                if validateMove(move_with_id[0], state['board_object'], self.pawns[self.colour]):
                    legal_moves.append(move_with_id)
            except Exception as e:
                #move is invalid, skip it
                print(e)
                continue
        
        return legal_moves

    def calculate_rewards(self, state):
        #will need distance for both pawns multiple times, so calculate it once
        white_path, black_path = self.determine_best_paths(state)
        white_distance, black_distance = len(white_path) - 1, len(black_path) - 1 # -1 as the path includes the start position
        #victory or defeat reward
        victory_or_defeat_reward = self.defeat_or_victory(state)
        
        #the reward for the distance of the opponent from the end goal
        opponent_distance_reward = black_distance if self.colour == 'white' else white_distance
        
        ###print('black_distance:', black_distance, 'white_distance:', white_distance, 'opponent_distance_reward:', opponent_distance_reward)
        #the reward for the difference in distance between the two pawns
        path_difference_reward =  black_distance - white_distance if self.colour == 'white' else  white_distance - black_distance
        
        ###print('path_difference_reward:', path_difference_reward)
        #the punishment for having less walls than the opponent
        wall_difference_penalty = self.wall_difference_penalty()
        
        #the punishment for being further from the end goal than the opponent
        distance_penalty = white_distance if self.colour == 'white' else black_distance
        distance_penalty *= -1 #negate as punishment
        return victory_or_defeat_reward + path_difference_reward + wall_difference_penalty + opponent_distance_reward + distance_penalty
    
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
        #if board is in a victory or defeat state, return the reward for that state
        if(self.pawns['white'] == state['board'][8] and self.colour == 'white'):
            reward += 1000
        if(self.pawns['black'] == state['board'][0] and self.colour == 'black'):
            reward += 1000
        if(self.pawns['white'] == state['board'][8] and self.colour == 'black'):
            reward -= 1000
        if(self.pawns['black'] == state['board'][0] and self.colour == 'white'):
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
    