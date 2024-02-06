from .cell import Cell

class Board:
    def __init__(self):
        self.board = [[Cell(i, j) for j in range(9)] for i in range(9)]
        
        #set the location of pawns to the start
        self.pawn_positions = 
        {
            'black': [0, 4],
            'white': [8, 4]
        }
        
        #place the pawns
        self.placePawns()
        
        #set the initial stae
        self.updateState
        
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
    
    def placeWall(self, orientation, startCell):
        if(orientation == 'horizontal'):
            direction = [0, 1]
        elif(orientation == 'vertical'):
            direction = [-1, 0]
        else:
            raise ValueError("Orientation must be 'horizontal' or 'vertical'")
        
        # Calculate the end cell's row and column indices
        end_row_index = startCell.position[0] + direction[0]
        end_col_index = startCell.position[1] + direction[1]

        # Check if the calculated position is valid
        if self.validLocation(end_row_index, end_col_index):
            # Access the end cell using the calculated indices
            endCell = self.board[end_row_index][end_col_index]
        else:
            raise IndexError("The wall extends out of bounds.")
        
        #if the orientation is horizontal the wall is placed along the top of the cells
        if(orientation == 'horizontal'):
            startCell.setWalls(False, True)
            endCell.setWalls(False, True)
        #otherwise the orientation is vertical and the wall is placed to the side of the cells
        else:
            startCell.setWalls(True, False)
            endCell.setWalls(True, False)

    
    def validLocation(self, i, j):
        # Return True if the location is on the board, False if it's off the board
        return 0 <= i <= 8 and 0 <= j <= 8

    
    def updateState(self):
        self.state = 
        {
            'board' : self.board,
            'pieces': self.pawn_positions
            'walled_cells': self.findWalledCells()
        }
                
                
                
    