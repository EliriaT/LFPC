import string
import datetime
from token import Token
from error import Error

TOKEN_NUM	    = 'NUM'
TOKEN_STRING    = 'STRING'
TOKEN_DATE      = 'DATE'
TOKEN_COLON     = ':'
TOKEN_SEMICOLON = ';'
TOKEN_PLUS      = '+'
TOKEN_MINUS     = '-'
TOKEN_MUL       = '*'
TOKEN_DIV       = '/'
TOKEN_POWER     = 'POWER'
TOKEN_LPAREN    = 'LPAREN'
TOKEN_RPAREN    = 'RPAREN'
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
    'FALSE'
]

DIGIT = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGIT+'-'+'_'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.forward()

    def forward(self):
        self.pos+=1
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
                tokens.append(Token(TOKEN_NEWLINE))
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
                tokens.append(Token(TOKEN_PLUS))
                self.forward()
            elif self.current_char == '-':
                tokens.append(Token(TOKEN_MINUS))
                self.forward()
            elif self.current_char == '*':
                self.forward()
                if(self.current_char=='*'):
                    self.forward()
                    tokens.append(Token(TOKEN_POWER))
                    continue
                tokens.append(Token(TOKEN_MUL))
            elif self.current_char == '/':
                tokens.append(Token(TOKEN_DIV))
                self.forward()
            elif self.current_char == '(':
                tokens.append(Token(TOKEN_LPAREN))
                self.forward()
            elif self.current_char == ')':
                tokens.append(Token(TOKEN_RPAREN))
                self.forward()
            elif self.current_char == '[':
                tokens.append(Token(TOKEN_LSQBRACKER))
                self.forward()
            elif self.current_char == ']':
                tokens.append(Token(TOKEN_RSQBRACKER))
                self.forward()
            elif self.current_char == '\\':
                tokens.append(Token(TOKEN_SLASH))
                self.forward()
            elif self.current_char == ':':
                tokens.append(Token(TOKEN_COLON))
                self.forward()
            elif self.current_char == ';':
                tokens.append(Token(TOKEN_SEMICOLON))
                self.forward()
            elif self.current_char == '<':
                self.forward()
                if(self.current_char=='='):
                    self.forward()
                    tokens.append(Token(TOKEN_LEQ))
                    continue
                tokens.append(Token(TOKEN_LESSOP))
            elif self.current_char == '>':
                self.forward()
                if(self.current_char=='='):
                    self.forward()
                    tokens.append(Token(TOKEN_GEQ))
                    continue
                tokens.append(Token(TOKEN_GREATEROP))
            elif self.current_char == '=':
                self.forward()
                if(self.current_char=='='):
                    self.forward()
                    tokens.append(Token(TOKEN_EQUALOP))
                    continue
                tokens.append(Token(TOKEN_EQUAL))
            elif self.current_char == ',':
                tokens.append(Token(TOKEN_COMMA))
                self.forward()
            elif self.current_char == '!':
                self.forward()
                if(self.current_char=='='):
                    self.forward()
                    tokens.append(Token(TOKEN_INEQ))
                    continue
                return [], Error( 'Expected Character: = ', ';Found instead: ' + self.current_char )
                
            else:
                char = self.current_char
                self.forward()
                return [], Error( 'Illegal Character! ' ,'Found instead '+ char )
        tokens.append(Token(TOKEN_EOF))
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
            return Token(TOKEN_NUM, int(num_str))
        elif dot_count == 1:
            return Token(TOKEN_NUM, float(num_str))
        elif dot_count == 2:
            num_str=num_str.replace('.','-')
            return Token(TOKEN_DATE, datetime.date.fromisoformat(num_str))
        else:
            return Error('Illegal format: ' + num_str,' Please provide date in form of dd.mm.yyyy' )

    def construct_identifier(self):
        identifier=''
        while(self.current_char!=None and self.current_char in LETTERS_DIGITS):
            identifier+=self.current_char
            self.forward()
        if identifier.upper() in KEYWORDS:
            return Token(TOKEN_KEYWORD,identifier)
        return Token(TOKEN_IDENTIFIER,identifier)

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
                    string+=Token(TOKEN_IDENTIFIER,identif).print_token()
                    self.forward()
                else: 
                    string+=all_text 
                    continue
            
            string+=self.current_char
            self.forward()
            
        self.forward()
        return Token(TOKEN_STRING, string)