class MoveFormatError(Exception):
    def __init__(self, field, message="Invalid move format."):
        
        self.field = field
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.field}: {self.message}"