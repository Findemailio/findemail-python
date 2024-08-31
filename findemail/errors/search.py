class InvalidInputError(Exception):
    """The entered values are invalid!"""
    def __init__(self):
        super().__init__('The entered values are invalid!')

class InvalidTypeError(Exception):
    """Invalid type!"""
    def __init__(self, message: str):
        super().__init__(message)