class WallTypeError(Exception):
    def __init__(self, field, message="Wall tpe should be vertical or horizontal."):
        
        self.field = field
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.field}: {self.message}"