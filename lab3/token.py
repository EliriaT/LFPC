class Token:
    def __init__(self, type, value=""):
        self.type = type
        self.value = value
    
    def print_token(self):
        if self.value!="": 
            return f'{self.type}({self.value})'
        return f'{self.type}'