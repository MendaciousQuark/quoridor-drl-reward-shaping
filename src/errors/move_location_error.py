class MoveLocationError(Exception):
    def __init__(self, field, message="The location chosen for the move is invalid. (probably off the board)"):
        
        self.field = field
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.field}: {self.message}"