from enum import Enum

class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'

class Error(Exception):
    def __init__(self, error_code, token,message=None):
        self.error_code = error_code
        self.token = token
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)
    
    def print_message(self):
        message  = f'{self.error_code} - {self.token}\n'
        return message

class ParserError(Error):
    pass
