import string
import datetime
from tokens import Token
from error import Error
from Token_Types import TokenType

TOKEN_NUM_LIT	    = 'NUM_LIT'
TOKEN_STRING_LIT    = 'STRING_LIT'
TOKEN_DATE_LIT     = 'DATE_LIT'
TOKEN_BOOL_LIT     = 'BOOL_LIT'
TOKEN_COLON     = ':'
TOKEN_SEMICOLON = ';'
TOKEN_PLUS      = '+'
TOKEN_MINUS     = '-'
TOKEN_MUL       = '*'
TOKEN_DIV       = '/'
TOKEN_POWER     = 'POWER'
TOKEN_LPAREN    = '('
TOKEN_RPAREN    = ')'
TOKEN_EQUAL     = '='
TOKEN_EQUALOP   = '=='
TOKEN_GREATEROP = '>'
TOKEN_LESSOP    = '<'
TOKEN_GEQ       = '>='
TOKEN_LEQ       = '<='
TOKEN_INEQ      = '!='
TOKEN_SLASH     = '\\'
TOKEN_LSQBRACKER= '['
TOKEN_RSQBRACKER= ']'
TOKEN_COMMA     = ','
TOKEN_NEWLINE	= '\n'
TOKEN_KEYWORD	= 'KEYWORD'
TOKEN_IDENTIFIER= 'IDENTIFIER'
TOKEN_EOF       = 'EOF'

KEYWORDS = [
    'FUNC',
    'AND',
    'OR',
    'MAIN',
    'IF',
    'ARRAY',
    'ELSE',
    'UNTIL',
    'NUM',
    'STRING',
    'DATE',
    'BOOL',
    'RETURN',
    'TRUE',
    'FALSE',
    'PRINT',
     'NOT'
]

DIGIT = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGIT+'-'+'_'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.line = 1
        self.column = 0
        self.forward()

    def forward(self):
        self.pos+=1
        self.column += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos] 
        else:
            self.current_char=None

    def tokenise(self):

        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.forward()
            elif self.current_char in '\n':
                tokens.append(Token(TokenType.NEWLINE,lineno=self.line, column=self.column))
                self.line += 1
                self.column = 0
                self.forward()
            elif self.current_char in DIGIT:
                result=self.construct_number()
                if(isinstance(result, Token)):
                    tokens.append(result)
                else:
                    return [], result
            elif self.current_char in LETTERS:
                tokens.append(self.construct_identifier())
            elif self.current_char =='"':
                tokens.append(self.construct_string())
            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS,TokenType.PLUS.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == '-':
                tokens.append(Token(TokenType.MINUS,TokenType.MINUS.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == '*':
                self.forward()
                if(self.current_char=='*'):
                    self.forward()
                    tokens.append(Token(TokenType.POWER,TokenType.POWER.value,lineno=self.line, column=self.column))
                    continue
                tokens.append(Token(TokenType.MUL,TokenType.MUL.value,lineno=self.line, column=self.column))
            elif self.current_char == '/':
                tokens.append(Token(TokenType.DIV,TokenType.DIV.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == '(':
                tokens.append(Token(TokenType.LPAREN,TokenType.LPAREN.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RPAREN,TokenType.RPAREN.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == '[':
                tokens.append(Token(TokenType.LSQBRACKER,TokenType.LSQBRACKER.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == ']':
                tokens.append(Token(TokenType.RSQBRACKER,TokenType.RSQBRACKER.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == '\\':
                tokens.append(Token(TokenType.SLASH,TokenType.SLASH.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == ':':
                tokens.append(Token(TokenType.COLON,TokenType.COLON.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == ';':
                tokens.append(Token(TokenType.SEMICOLON,TokenType.SEMICOLON.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == '<':
                self.forward()
                if(self.current_char=='='):
                    self.forward()
                    tokens.append(Token(TokenType.LEQ,TokenType.LEQ.value,lineno=self.line, column=self.column))
                    continue
                tokens.append(Token(TokenType.LESSOP,TokenType.LESSOP.value,lineno=self.line, column=self.column))
            elif self.current_char == '>':
                self.forward()
                if(self.current_char=='='):
                    self.forward()
                    tokens.append(Token(TokenType.GEQ,TokenType.GEQ.value,lineno=self.line, column=self.column))
                    continue
                tokens.append(Token(TokenType.GREATEROP,TokenType.GREATEROP.value,lineno=self.line, column=self.column))
            elif self.current_char == '=':
                self.forward()
                if(self.current_char=='='):
                    self.forward()
                    tokens.append(Token(TokenType.EQUALOP,TokenType.EQUALOP.value,lineno=self.line, column=self.column))
                    continue
                tokens.append(Token(TokenType.EQUAL,TokenType.EQUAL.value,lineno=self.line, column=self.column))
            elif self.current_char == ',':
                tokens.append(Token(TokenType.COMMA,TokenType.COMMA.value,lineno=self.line, column=self.column))
                self.forward()
            elif self.current_char == '!':
                self.forward()
                if(self.current_char=='='):
                    self.forward()
                    tokens.append(Token(TokenType.INEQ,TokenType.INEQ.value,lineno=self.line, column=self.column))
                    continue
                return [], Error( 'Expected Character: = ', ';Found instead: ' + self.current_char )
                
            else:
                char = self.current_char
                self.forward()
                return [], Error( 'Illegal Character! ' ,'Found instead '+ char )
        tokens.append(Token(TokenType.EOF,TokenType.EOF.value,lineno=self.line, column=self.column))
        return tokens, None

    def construct_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char != None and self.current_char in (DIGIT + '.'):
            if self.current_char == '.':
                dot_count += 1
            num_str += self.current_char
            self.forward()

        if dot_count == 0:
            return Token(TokenType.NUM_LIT, int(num_str),lineno=self.line, column=self.column)
        elif dot_count == 1:
            return Token(TokenType.NUM_LIT, float(num_str),lineno=self.line, column=self.column)
        elif dot_count == 2:
            num_str=num_str.replace('.','-')
            return Token(TokenType.DATE_LIT, datetime.date.fromisoformat(num_str),lineno=self.line, column=self.column)
        else:
            return Error('Illegal format: ' + num_str,' Please provide date in form of dd.mm.yyyy' )

    def construct_identifier(self):
        identifier=''
        while(self.current_char!=None and self.current_char in LETTERS_DIGITS):
            identifier+=self.current_char
            self.forward()
        if identifier.upper() in KEYWORDS:
            return Token( TokenType(identifier.upper()),identifier,lineno=self.line, column=self.column)
        return Token(TokenType.IDENTIFIER,identifier,lineno=self.line, column=self.column)

    def construct_string(self):
        string=''
        self.forward()
        while(self.current_char!=None and self.current_char != '"'):
            if(self.current_char=='{'):
                self.forward()
                identif=''
                all_text='{'
                flag=False
                flag_close=False

                while( self.current_char in LETTERS_DIGITS+' '):
                    if(identif!='' and self.text[self.pos-1]==' ' and self.current_char in LETTERS_DIGITS): 
                        flag=True
                    
                    if(self.current_char==' '): all_text+=self.current_char
                    
                    else:
                        if(flag): break
                        all_text+=self.current_char
                        
                        identif+=self.current_char
                    
                    self.forward()
        
                if(identif!='' and self.current_char=='}' and flag!=True ): flag_close=True
                if(flag_close and not(flag)): 
                    string+=Token(TokenType.IDENTIFIER,identif,lineno=self.line, column=self.column).print_token()
                    self.forward()
                else: 
                    string+=all_text 
                    continue
            
            string+=self.current_char
            self.forward()
            
        self.forward()
        return Token(TokenType.STRING_LIT, string,lineno=self.line, column=self.column)