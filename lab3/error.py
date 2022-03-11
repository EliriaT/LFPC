class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
    
    def print_message(self):
        message  = f'{self.error_name} - {self.details}\n'
        return message