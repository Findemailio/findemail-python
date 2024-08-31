class ApiKeyError(Exception):
    """The entered api_key is invalid!"""
    def __init__(self, message: str = None):
        super().__init__('The entered api_key is invalid!' or message)

class UnknownError(Exception):
    """Unknown Error!"""
    def __init__(self, status_code: int):
        super().__init__(f'invalid status code ~> {status_code}!')

class AccessForbiddenError(Exception):
    """Access Forbidden Error!"""
    def __init__(self, message: str):
        super().__init__(message)

class NotFoundError(Exception):
    """Not Found Error!"""
    def __init__(self):
        super().__init__("Not Found!")

class MethodNotAllowedError(Exception):
    """Method Not Allowed Error!"""
    def __init__(self, message: str):
        super().__init__(message)

class FloodWaitError(Exception):
    """Flood Wait Error!"""
    def __init__(self, message: str):
        super().__init__(message)
