from utils import UP, DOWN, LEFT, RIGHT 
from utils import getDirectionIndex, opposingPawnAdjacent, validLocation, locationToCell, getCellDirection, moveNumberToLetter
from logic import validateMove
from game import Move
class Model:
    def __init__(self, colour, name='Bot', description='Bot'):
        self.name = name
        #'black' or 'white'
        self.colour = colour
        self.description = description
        # ... other attributes
        self.action_state = []
        
    def find_legal_moves(self, state):
        current_position = state[self.colour]
        walls = self.find_legal_walls(state, current_position)
        movement = self.find_legal_movement(state, current_position)
        self.action_state.extend(walls)
        self.action_state.extend(movement)
    
    def find_legal_walls(self, state, current_position):
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
                #determine if it makes sense to check for a vertical or horizontal wall
                check_vertical = i<= 7 and (1 <= j <= 8)
                check_horizontal = (1 <= i <= 8) and j <= 7
                
                #convert the current position to the move format (e.g. [1, 0] -> 'a2' (when i = 1 = 2, j = 0 = a))
                position_formatted = moveNumberToLetter(j) + str(i + 1)
                
                if check_vertical:
                    #crete a move object for the vertical wall placement
                    orientation = 'vertical'
                    #if the cell is already walled, skip it as it must be an illegal wall
                    if cell in state['walled_cells'][orientation]:
                        continue
                    partially_legal_walls.append(Move(coulour_formatted, position_formatted, None, 'place', None, None, orientation))
                    
                if check_horizontal:
                    #crete a move object for the horizontal wall placement
                    orientation = 'horizontal'
                    #if the cell is already walled, skip it as it must be an illegal wall
                    if cell in state['walled_cells'][orientation]:
                        continue
                    partially_legal_walls.append(Move(coulour_formatted, position_formatted, None, 'place', None, None, orientation))
        
        legal_walls = []
        for wall in partially_legal_walls:
            if validateMove(wall, state['board_object'], self):
                legal_walls.append(wall)
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
                    moves_to_check.append(Move(coulour_formatted, start_formatted, end_formatted, 'jump', None, jump_direction_formatted, None))
                
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
                moves_to_check.append(Move(coulour_formatted, start_formatted, end_formatted, 'move', direction_formatted, None, None))
        
        legal_moves = []
        for move in moves_to_check:
            #try:
            if validateMove(move, state['board_object'], self):
                legal_moves.append(move)
            # except Exception as e:
            #     continue
        
        return legal_moves