from Node_types import *
from error import *
from Token_Types import *


#Generating the AST
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.delete_newline()
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

    def delete_newline(self):
        self.tokens = list(filter(lambda i:not(i.type == TokenType.NEWLINE), self.tokens))

    def get_next_token(self):
        return self.tokens.pop(0)

    #Function to see the next token in the stream
    def peek(self):
        if(len(self.tokens)>0): return self.tokens[0] 
        else: return None

    def error(self, error_code, token,expected_token):
        raise ParserError( error_code=error_code,token=token, message=f'{error_code.value} -> {token}; Expected: {expected_token} at {token.linenum} : {token.column}')

    def eat(self, token_type):
        # It compares the current token type with the passed token
        # type and if they match the current token is "eaten" 
        # and assigned the next token to the self.current_token,
        # otherwise  an exception is raised.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error( error_code=ErrorCode.UNEXPECTED_TOKEN,   token=self.current_token, expected_token=token_type.name)

    def main_program(self):
        next_token=self.peek()
        functions=None
        if next_token.type == TokenType.FUNC:
            functions=self.function_decl()
        main_funct=self.main_func()
        program_node=Program(main_funct,functions)
        return program_node

    def function_decl(self):
        func_type=self.type_spec()
        
        self.eat(TokenType.FUNC)
        var_node = self.variable()
        function_name=var_node.value
  
        declaration_nodes = self.declarations()  #The formal parameters of a function
        self.eat(TokenType.COLON)
        block_node, return_statement = self.block()

        if(return_statement == None):
            self.eat(TokenType.RETURN)
            return_expression = self.boolean_expressions
            self.eat(TokenType.SEMICOLON)
            self.eat(TokenType.SLASH)
            return_statement=ReturnNode(return_expression)
        
        function_node=FunctionDecl(function_name, declaration_nodes, block_node,func_type,return_statement)

        return function_node

    def main_func(self):
        func_type=self.type_spec()
        self.eat(TokenType.MAIN)
        self.eat(TokenType.COLON)
        # self.eat(TokenType.ACTIONS)
        # self.eat(TokenType.COLON)
        block_node, return_statement = self.block()
        mainfunc_node=MainFunction(block_node,func_type)
        return mainfunc_node


    def declarations(self):
        """
        declarations : ( [(variable_declaration ;)+) ]
        """
        declarations = []

        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)

            while self.current_token.type in [TokenType.NUM,TokenType.STRING,TokenType.DATE,TokenType.BOOL,TokenType.ARRAY]:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(TokenType.SEMICOLON)
            self.eat(TokenType.RPAREN)

        return declarations

    def variable_declaration(self):
        """variable_declaration : [array] type_spec IDENTIFIER (COMMA IDENTIFIER)* """

        type_node = self.type_spec()
        var_nodes = [Var(self.current_token)]  # first Identifier
        self.eat(TokenType.IDENTIFIER)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.IDENTIFIER)

        # self.eat(TokenType.COLON)

        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations

    def type_spec(self):
        # type_spec : NUM| BOOL|DATE | STRING
# TokenType.NUM,TokenType.STRING,TokenType.DATE,TokenType.BOOL
        token = self.current_token
        if self.current_token.type == TokenType.NUM:
            self.eat(TokenType.NUM)
        elif self.current_token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
        elif self.current_token.type == TokenType.DATE:
            self.eat(TokenType.DATE)
        elif self.current_token.type == TokenType.BOOL:
            self.eat(TokenType.BOOL)
        elif self.current_token.type == TokenType.ARRAY:
            self.eat(TokenType.ARRAY)
            if self.current_token.type in [TokenType.NUM,TokenType.STRING,TokenType.DATE,TokenType.BOOL]:
                array_type=self.current_token.type
                self.eat(self.current_token.type)
                return Type(token,array_type)
            else: self.error( error_code=ErrorCode.UNEXPECTED_TOKEN,   token=self.current_token, expected_token="array type")
        else: self.error( error_code=ErrorCode.UNEXPECTED_TOKEN,   token=self.current_token, expected_token="type token")

        node = Type(token)
        return node


    def block(self):
        """block : \  compound_statement \\"""
        self.eat(TokenType.SLASH)
        compound_statement_node, return_statement = self.compound_statement()
        self.eat(TokenType.SLASH)
        node = Block( compound_statement_node)
        return node, return_statement


    def compound_statement(self): #The statements will be registered only before the first return statement
        """
        compound_statement:  statement_list 
        """
 
        nodes = self.statement_list()

        root = Compound()
        return_statement=None
        for node in nodes:
            root.children.append(node)
            if isinstance(node, ReturnNode): 
                return_statement=node
                return root, return_statement
            
        return root,return_statement

    def statement_list(self): #Print to add
        """
        statement_list : statement
                        | statement SEMICOLON statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
            results.append(self.statement())

        return results


    def statement(self):
        """
        statement :| function_call ;
                  | assignment_statement;
                  | if else;
                  |until;
                  |do until;
                  | variable declaration;
                  | print();
                  | empty;
        """
   
        next_token=self.peek()
        if self.current_token.type == TokenType.IDENTIFIER and next_token.type == TokenType.LPAREN:
            node = self.function_call_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            node = self.assignment_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.if_statement()
        elif (self.current_token.type == TokenType.UNTIL):
            node = self.until_statement()
        elif self.current_token.type in [TokenType.NUM,TokenType.STRING,TokenType.DATE,TokenType.BOOL,TokenType.ARRAY]:
            node = self.variable_declaration()
        elif self.current_token.type == TokenType.PRINT:
            node = self.print()
        elif self.current_token.type == TokenType.RETURN:
            self.eat( TokenType.RETURN)
            expr=self.boolean_expressions()
            node=ReturnNode(expr)
            
        else:
            node = self.empty()
        return node


    def function_call_statement(self):
        token = self.current_token

        function_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        actual_params = []
        if self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.LSQBRACKER:
                node=self.construct_array()
            else: node = self.boolean_expressions()
            actual_params.append(node)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            if self.current_token.type==TokenType.LSQBRACKER:
                node=self.construct_array()
            else: node = self.boolean_expressions()
            actual_params.append(node)

        self.eat(TokenType.RPAREN)

        node = FunctionCall(
            func_name=function_name,
            actual_params=actual_params,
            token=token,
        )
        return node


    def print(self): #Does not allow array printing
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        actual_parameters=[]
        if self.current_token != TokenType.RPAREN:
            actual_parameters.append(self.boolean_expressions())
            while(self.current_token == TokenType.COMMA):
                actual_parameters.append(self.boolean_expressions())
        self.eat(TokenType.RPAREN)
        return PrintNode(actual_parameters)


    def construct_array(self): #Function when there is an array as an argument
        self.eat(TokenType.LSQBRACKER)
        values=[]
        node = self.boolean_expressions()
        values.append(node)
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = self.boolean_expressions()
            values.append(node)
        self.eat(TokenType.RSQBRACKER)
        return ArrayNode(values)


    def if_statement(self):
        self.eat(TokenType.IF)

        self.eat(TokenType.LSQBRACKER)
        boolean_expression = self.boolean_expressions()
        self.eat(TokenType.RSQBRACKER)
        statements, return_statemen = self.block()
        
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            else_statements, return_statemen = self.block()
            return IfElseNode(boolean_expression, statements, else_statements)
        else:
            return IfNode(boolean_expression, statements)


    def until_statement(self):
        self.eat(TokenType.UNTIL)
        self.eat(TokenType.LSQBRACKER)
        boolean_expression = self.boolean_expressions()
        self.eat(TokenType.RSQBRACKER)

        statements , return_statement= self.block()
        return UntilNode(boolean_expression, statements)

    
    def assignment_statement(self): #Dupa egal pot sa am function call //array
        """
        assignment_statement : variable ASSIGN boolexpr?
        """
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.EQUAL)
        
        right = self.boolean_expressions()
 
        node = Assign(left, token, right)
        return node
  

    def variable(self):
        """
        variable : Identifier | Identifier[num-literal | identifier]
        """
        
        next_token=self.peek()
        # print(next_token)
        if next_token.type==TokenType.LSQBRACKER:
            node_identif=self.current_token
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.LSQBRACKER)
            array_index=self.current_token.value
            if self.current_token.type == TokenType.IDENTIFIER:
                self.eat(TokenType.IDENTIFIER)
            else: self.eat(TokenType.NUM_LIT)
            self.eat(TokenType.RSQBRACKER)
            node = Var(node_identif,array_index)
            return node
        
        node = Var(self.current_token)
        self.eat(TokenType.IDENTIFIER)
        return node


    def boolean_expressions(self): #Sa adaug [ ]
        """
        expression : comp_expression ((AND|OR) comp_expression)*
        """
        
        node = self.comp_expression()
        while (self.current_token.type == TokenType.AND) or (self.current_token.type == TokenType.OR):
            sign = self.current_token
            self.eat(sign.type)
            second_expr=self.comp_expression()
            node = BinOp(node, sign, second_expr)

        return node

        
    def comp_expression(self):
        if self.current_token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            expression_one=self.comp_expression()
            return UnaryOp(self.current_token, expression_one)

        expression_one=self.expr()

        while self.current_token.type in [TokenType.GREATEROP,TokenType.LESSOP,TokenType.GEQ,TokenType.LEQ,TokenType.INEQ,TokenType.EQUALOP]:
            op=self.current_token
            self.eat(self.current_token.type)
            expression_Two=self.expr()
            return BinOp(expression_one, op, expression_Two)

        return expression_one


    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node


    def term(self):
        """term : factor ((MULT | DIV factor)*"""
        node = self.factor()

        # if node.token.type == TokenType.TEXT_LITERALS:
        #     return node

        while self.current_token.type in (
                TokenType.MUL,
                TokenType.DIV,
        ):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node


    def factor(self): #Sa adaug puterea?
        """factor : PLUS factor
                  | MINUS factor
                  | LPAREN boolean_expressions RPAREN
                  | variable |date literal | bool literal | string literal | num literal | func_call
                
        """
        token = self.current_token
        next_token=self.peek()
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.IDENTIFIER and next_token.type==TokenType.LPAREN:
            node = self.function_call_statement()
            return node
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.boolean_expressions()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.NUM_LIT:
            self.eat(TokenType.NUM_LIT)
            return Literal(token,token.type)
        elif token.type == TokenType.STRING_LIT:
            self.eat(TokenType.STRING_LIT)
            return Literal(token,token.type)
        elif token.type == TokenType.DATE_LIT:
            self.eat(TokenType.DATE_LIT)
            return Literal(token,token.type)
        elif token.type == TokenType.BOOL_LIT:
            self.eat(TokenType.BOOL_LIT)
            return Literal(token,token.type)
        else:
            node = self.variable()
            return node

    
    def empty(self):
        """An empty production"""
        return NoOp()
        

    def parse(self):
    
        node = self.main_program()
        if self.current_token.type != TokenType.EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
                expected_token=TokenType.EOF
            )

        return node