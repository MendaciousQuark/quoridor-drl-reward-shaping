from utils import validLocation, moveLetterToNumber, UP, DOWN, LEFT, RIGHT
from errors import MoveLocationError, MoveFormatError

class Move:
    def __init__(self, colour, start, end, action, direction, jumpDirection=None, orientation=None):
        self.parseMove(colour, action, start, end, direction, jumpDirection, orientation)
    
    def parseMove(self, colour, action, start, end, direction, jumpDirection=None, orientation=None):
        #parse the colour
        self.colour = self.parseColour(colour)
        
        #parse the action
        self.action = self.parseAction(action)
        if(self.action == "jump"):
            self.direction = self.parseDirection(jumpDirection)
        elif(self.action == "place"):
            self.orientation = self.parseOrientation(orientation)
        
        #parse start and end positions
        self.start = self.parseLocation(start)
        if(not validLocation(self.start)):
            raise MoveLocationError("start", f"Invalid start location: {start}")
        
        #only one location and orinetation (not direction) is needed for placing a wall
        if(self.action == "place"):
            self.end = None
            self.direction = None
        else:
            self.end = self.parseLocation(end)
            if(not validLocation(self.end)):
                raise MoveLocationError("end", f"Invalid end location: {end}")
        
        #parse the direction
        self.direction = self.parseDirection(direction)
    
    def parseColour(self, colour):
        colour = colour.lower()
        if(colour == "white" or colour == 'w'):
            return "white"
        elif(colour == "black" or colour == 'b'):
            return "black"
        else:
            raise MoveFormatError("colour", f"Invalid colour: {colour}\nColour should be one of 'white' or 'black'")
    
    def parseLocation(self, location):
        #parse the location
        parts = list(location)
        if(len(parts) != 2):
            raise MoveLocationError("location", f"Invalid location: {location}\nLocation should be a letter and a number. e.g. 'a1'")
        try:
            i = moveLetterToNumber(parts[0])
            j = int(parts[1]) - 1
        except ValueError:
            raise MoveLocationError("location", f"Invalid location: {location}\nLocation should be a letter followed by a number. e.g. 'b3'")
        return (i, j)
    
    def parseAction(self, action):
        #format the action
        action = action.lower()
        
        #parse the action
        if(action == "move" or action == 'm'):
            return "move"
        elif(action == "jump" or action == 'j'):
            return "jump"
        elif(action == "place" or action == 'p'):
            return "place"
        else:
            raise MoveFormatError("action", f"Invalid action: {action}\nAction should be one of 'move', 'place', or 'jump'")
    
    def parseOrientation(self, orientation):
        #format the orientation
        orientation = orientation.lower()
        
        #parse the orientation
        if(orientation == "vertical" or orientation == 'v'):
            return "vertical"
        elif(orientation == "horizontal" or orientation == 'h'):
            return "horizontal"
        else:
            raise MoveFormatError("orientation", f"Invalid orientation: {orientation}\nOrientation should be one of 'vertical' or 'horizontal'")
    
    def parseDirection(self, direction):
        #format the direction
        direction = direction.lower()
        
        #no movement direction is needed for placing a wall
        if(self.action == "place"):
                return None
        
        #parse the direction
        if(direction == "up" or direction == 'u'):
            return UP
        elif(direction == "down" or direction == 'd'):
            return DOWN
        elif(direction == "left" or direction == 'l'):
            return LEFT
        elif(direction == "right" or direction == 'r'):
            return RIGHT
        else:
            raise MoveFormatError("direction", f"Invalid direction: {direction}\nDirection should be one of 'up', 'down', 'left', or 'right'")
        
    def __str__(self):
        return f"Colour: {self.colour}\nAction: {self.action}\nStart: {self.start}\nEnd: {self.end}\nDirection: {self.direction}\nOrientation: {self.orientation}, jumpDirection: {self.jumpDirection}  "