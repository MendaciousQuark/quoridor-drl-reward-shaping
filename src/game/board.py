from .cell import Cell
from utils import joinWithNewlines, getDirectionIndex, validLocation, UP, DOWN, LEFT, RIGHT
from utils.string_board import *
import pdb

class Board:
    def __init__(self):
        self.board = [[Cell(i, j) for j in range(9)] for i in range(9)]
        
        #set the location of pawns to the start
        self.pawn_positions = {
            'black': [0, len(self.board[0])//2],
            'white': [len(self.board[0]) - 1, len(self.board[0])//2]
        }
        
        #place the pawns
        self.placePawns()
        self.turn = 0
        #set the initial state
        self.updateState()
        
    def placePawns(self):
        # Place black pawn
        i, j = self.pawn_positions['black']
        #place holder for when I have implemented the paen class
        self.board[i][j].occupant = 'black'

        # Place white pawn
        i, j = self.pawn_positions['white']
        self.board[i][j].occupant = 'white'
    
    def removePawns(self):
        # Remove black pawn
        i, j = self.pawn_positions['black']
        self.board[i][j].occupant = None

        # Remove white pawn
        i, j = self.pawn_positions['white']
        self.board[i][j].occupant = None
    
    def findWalledCells(self):
        cells_with_walls = {
            'horizontal': [],
            'vertical': []
        }
        #iterate through all cells in the board
        for row in self.board:
            for cell in row:
                if(cell.has_wall_up):
                    cells_with_walls['horizontal'].append(cell)
                if(cell.has_wall_left):
                    cells_with_walls['vertical'].append(cell)
        #return the cells that have walls
        return cells_with_walls

    def makeMove(self, move, board, colour):
        if(move.action == "move" or move.action == "jump"):
            board.movePawn(colour, move.end)
        elif(move.action == "place"):
            board.placeWall(move.orientation, self.board[move.start[0]][move.start[1]])
        self.turn += 1
        self.updateState()
    
    def movePawn(self, colour, end):
        self.removePawns()
        pawn_colour = 'white' if colour == 'white' else 'black'
        self.pawn_positions[pawn_colour] = list(end)
        self.placePawns()
        self.updateState()
    
    def placeWall(self, orientation, start_cell):
        if(orientation == 'horizontal'):
            direction = RIGHT
        elif(orientation == 'vertical'):
            direction = DOWN
        else:
            raise ValueError("Orientation must be 'horizontal' or 'vertical'")
        
        # Calculate the end cell's row and column indices
        end_cell_location = getDirectionIndex(start_cell.position, direction)
        
        # Check if the calculated position is valid
        if validLocation(*end_cell_location):
            # Access the end cell using the calculated indices
            end_cell = self.board[end_cell_location[0]][end_cell_location[1]]
        
        #if the orientation is horizontal the wall is placed along the top of the cells
        if(orientation == 'horizontal'):
            start_cell.setWalls(True, start_cell.has_wall_left)
            end_cell.setWalls(True, end_cell.has_wall_left)
        #otherwise the orientation is vertical and the wall is placed to the side of the cells
        else:
            start_cell.setWalls(start_cell.has_wall_up, True)
            end_cell.setWalls(end_cell.has_wall_up, True)
        
        self.updateState()
    
    def updateState(self):
        self.state = {
            'turn': self.turn,
            'board_object': self,
            'board' : self.board,
            'pieces': self.pawn_positions,
            'walled_cells': self.findWalledCells()
        }
    
    def printBoard(self):
        
        '''
        Example board
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   | @ |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   | * |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        '''
        string_board = []
        #add column labels to top
        string_board.append(BORDER_COLUMNS)
        for j, row in enumerate(self.board):
            for i in range(2):
                for cell in row:
                    #determine which edges the cell is touching
                    edge_left = True if cell.neighbour_left is None else False
                    edge_right = True if cell.neighbour_right is None else False
                    edge_up = True if cell.neighbour_up is None else False
                    edge_down = True if cell.neighbour_down is None else False
                    
                    #horizontal row (rows with '+')
                    if(i == 0):
                        
                        #if we are in the top left corner
                        if(edge_left and edge_up):
                            #add the border for the horizontall lines and the top of the first cell
                            string_board.append(BORDER_HORIZONTAL)
                            string_board.append(CELL_HORIZONTAL_EDGE)
                        #if we are in the top right corner
                        elif(edge_right and edge_up):
                            string_board.append(CELL_HORIZONTAL)
                            
                        #if we are in the top row but not in a corner
                        elif(edge_up):
                            string_board.append(CELL_HORIZONTAL)
                        #if we are in the first column but not in the top left
                        elif(edge_left):
                            string_board.append(BORDER_HORIZONTAL)
                            #cells inn the first column can't continue walls so if there is a ceiling wall we are starting it
                            if(cell.has_wall_up):
                                string_board.append(CELL_HORIZONTAL_EDGE_WALLED)
                            #since cells only draw to the left and up and walls to the left of this column are just the edge of the board
                            #there is no need to check anymore walls
                            else:
                                string_board.append(CELL_HORIZONTAL_EDGE)
                        #if we are in the last column but not in the top right
                        elif(edge_right):
                            cell_up = self.board[cell.neighbour_up[0]][cell.neighbour_up[1]]
                            cell_left = self.board[cell.neighbour_left[0]][cell.neighbour_left[1]]
                            
                            #if we are continuing a ceiling wall
                            if(cell_left.has_wall_up and cell.has_wall_up):
                                string_board.append(CELL_HORIZONTAL_WALLED_CONNECTED)
                            #if we are continuing a wall on the left from the top
                            elif(cell_up.has_wall_left and cell.has_wall_left):
                                string_board.append(CELL_HORIZONTAL_INTERSECTION)
                            #can't have both walls from top and from left as walls are 2 cells long
                            else:
                                string_board.append(CELL_HORIZONTAL)
                        #if we are somewhere in between first and last column and/or on the last row (also in between first and last column)
                        elif((not edge_left) and (not edge_up) and (not edge_right)):
                            cell_up = self.board[cell.neighbour_up[0]][cell.neighbour_up[1]]
                            cell_left = self.board[cell.neighbour_left[0]][cell.neighbour_left[1]]
                            
                            #if walls form a T intersection (imgine T lying down to the left)
                            if(cell_up.has_wall_left and cell.has_wall_left and cell.has_wall_up):
                                string_board.append(CELL_HORIZONTAL_WALLED_INTERSECTION)
                            #if this cell continues a vertical wall from above
                            elif(cell_up.has_wall_left and cell.has_wall_left and not (cell.has_wall_up)):
                                string_board.append(CELL_HORIZONTAL_INTERSECTION)
                            #if the cell continues a ceiling wall from the left
                            elif(cell_left.has_wall_up and cell.has_wall_up):
                                string_board.append(CELL_HORIZONTAL_WALLED_CONNECTED)
                            #if the cell starts a ceiling wall
                            elif(cell.has_wall_up):
                                string_board.append(CELL_HORIZONTAL_WALLED)
                            #no walls pass the ceiling threshold
                            else:
                                string_board.append(CELL_HORIZONTAL)
                    #vertical row (rows with '|')
                    elif(i == 1):
                        
                        #determin if and which pawn is present
                        pawn_present = False if cell.occupant is None else True
                        white_present = True if cell.occupant == 'white' else False
                        black_present = True if cell.occupant == 'black' else False
                        
                        #if we are in the first column
                        if(edge_left):
                            string_board.append(BORDER_VERTICAL)
                            #if there is a pawn present
                            if(pawn_present):
                                #check which one
                                if(white_present):
                                    string_board.append(CELL_VERTICAL_EDGE_PAWN_WHITE)
                                elif(black_present):
                                    string_board.append(CELL_VERTICAL_EDGE_PAWN_BLACK)
                            else:
                                string_board.append(CELL_VERTICAL_EDGE)
                        #in very other column, we can do the same thing because all the walls are to the left and therefore the same (we draw left to right) 
                        else:
                            #if a cells is walled and occupied
                            if(cell.has_wall_left and pawn_present):
                                #check which pawn is present
                                if(white_present):
                                    string_board.append(CELL_VERTICAL_WALLED_PAWN_WHITE)
                                elif(black_present):
                                    string_board.append(CELL_VERTICAL_WALLED_PAWN_BLACK)
                            #if there is just a pawn
                            elif(pawn_present):
                                if(white_present):
                                    string_board.append(CELL_VERTICAL_PAWN_WHITE)
                                elif(black_present):
                                    string_board.append(CELL_VERTICAL_PAWN_BLACK)
                            #if there is just a wall and no pawn
                            elif(cell.has_wall_left):
                                string_board.append(CELL_VERTICAL_WALLED)
                            #if there is no wall and no pawn
                            else:
                                string_board.append(CELL_VERTICAL)
                        
                #add the border symbols
                if(i == 0):
                    #for horizontal lines (lines with +)
                    string_board.append(BORDER_HORIZONTAL)
                    string_board.append(" ")
                    string_board.append(" ")
                    string_board.append(" ")
                else:
                    #for vertical lines (lines with |)
                    string_board.append(BORDER_VERTICAL)
                    string_board.append(" ")
                    string_board.append(str(9-j))
                    string_board.append(" ")
        #iterate for the length of the board to add a bottom border
        for j in range(len(self.board[0])):
            string_board.append(BORDER_BOTTOM)
        #need to add the edge border onelast time
        string_board.append(BORDER_HORIZONTAL)
        #now add the column labels again
        string_board.append(BORDER_COLUMNS)
        #pdb.set_trace()
        #return a joined string_board we do len(self.board[0]) + 5 to account for the length of each row and the borders (includin 9-1 a-i etc)
        return joinWithNewlines(string_board, len(self.board[0]) + 5)
    
    def copy(self):
        new_board = Board()
        new_board.board = [[self.board[i][j].copy() for j in range(9)] for i in range(9)]
        new_board.pawn_positions = {
            'black': [self.pawn_positions['black'][0], self.pawn_positions['black'][1]],
            'white': [self.pawn_positions['white'][0], self.pawn_positions['white'][1]]
        }
        new_board.placePawns()
        new_board.updateState()
        return new_board
    
    def __str__(self):
        return self.printBoard()
    
    def __eq__(self, other_board: object) -> bool:
        if not isinstance(other_board, Board):
            return False
        return self.state == other_board.state
        
                    
                
                
    