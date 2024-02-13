class MoveValidationError(Exception):
    def __init__(self, field, message="Unknown error during move validation."):
        
        self.field = field
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.field}: {self.message}"