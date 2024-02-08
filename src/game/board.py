from .cell import Cell
from utils.directions import UP, DOWN, LEFT, RIGHT, getDirectionIndex
from utils.string_board import *
from utils.utils import validLocation, joinWithNewlines
import pdb

class Board:
    def __init__(self):
        self.board = [[Cell(i, j) for j in range(9)] for i in range(9)]
        
        #set the location of pawns to the start
        self.pawn_positions = {
            'black': [0, 4],
            'white': [8, 4]
        }
        
        #place the pawns
        self.placePawns()
        
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
        
    def findWalledCells(self):
        cells_with_walls = []
        #iterate through all cells in the board
        for row in self.board:
            for cell in row:
                if(cell.has_wall_up or cell.has_wall_left):
                    cells_with_walls.append(cell)
        #return the cells that have walls
        return cells_with_walls
    
    def placeWall(self, orientation, start_cell):
        if(orientation == 'horizontal'):
            direction = RIGHT
        elif(orientation == 'vertical'):
            direction = DOWN
        else:
            raise ValueError("Orientation must be 'horizontal' or 'vertical'")
        
        # Calculate the end cell's row and column indices
        end_cell_location = getDirectionIndex(start_cell.position, direction)
        #pdb.set_trace()
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
    
    def updateState(self):
        self.state = {
            'board' : self.board,
            'pieces': self.pawn_positions,
            'walled_cells': self.findWalledCells()
        }
    
    def printBoard(self):
        #pdb.set_trace()
        '''
        Example board
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   | @ |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---+---+---+---+---+---+---+---+---+
        # |   |   |   |   |   |   |   |   |   |
        # +---#---+---+---+---+---+---+---+---+
        # |   #   |   |   |   |   |   |   |   |
        # +---#---+---=========---+---+---+---+
        # |   #   |   |   |   |   |   |   |   |
        # +---#---+---+---+---+---+---+---+---+
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
        print(str(self.board[1][2]))
        print(str(self.board[2][2]))
        for row in self.board:
            for i in range(2):
                for cell in row:
                    #determine which edges the cell is touching
                    edge_left = True if cell.neighbour_left is None else False
                    edge_right = True if cell.neighbour_right is None else False
                    edge_up = True if cell.neighbour_up is None else False
                    edge_down = True if cell.neighbour_down is None else False
                    #pdb.set_trace()
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
                        #pdb.set_trace()
                        #determin if and which pawn is present
                        pawn_present = False if cell.occupant is None else True
                        white_present = True if cell.occupant is 'white' else False
                        black_present = True if cell.occupant is 'black' else False
                        
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
                        #pdb.set_trace()
                #add the border symbols
                if(i == 0):
                    #for horizontal lines (lines with +)
                    string_board.append(BORDER_HORIZONTAL)
                else:
                    #for vertical lines (lines with |)
                    string_board.append(BORDER_VERTICAL)
        #iterate for the length of the board to add a bottom border
        for j in range(len(self.board[0])):
            string_board.append(BORDER_BOTTOM)
        #need to add the edge border onelast time
        string_board.append(BORDER_HORIZONTAL)
        print(len(string_board))
        #print(string_board)
        #return a joined string_board we do len(self.board[0]) + 2 to account for the length of each row and the borders
        return joinWithNewlines(string_board, len(self.board[0]) + 2)
                        
                        
        
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
        
                    
                
                
    