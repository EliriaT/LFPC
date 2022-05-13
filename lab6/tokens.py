from Token_Types import TokenType
class Token:
    def __init__(self, type, value="",lineno=None, column=None):
        self.type = type
        self.value = value
        self.linenum = lineno
        self.column = column
    
    def print_token(self):
        if self.value!="": 
            return f'{self.type}({self.value})'
        return f'{self.type}'

    def __str__(self):
        #String representation of the class object
        #Example:
        #     Token(TokenType.INTEGER, 7, position=5:10)
        
        return '[{type}, {value} {lineno}:{column}]'.format(
            type=self.type.name,
            value=repr(self.value),
            lineno=self.linenum,
            column=self.column,
        )

    def __repr__(self):
        return self.__str__()