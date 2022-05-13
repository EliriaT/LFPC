class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Literal(AST):
    def __init__(self, token,literal_type):
        self.token = token
        self.value = token.value
        self.literal_type=literal_type



class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = op
        self.op = op
        self.expr = expr 


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token =op
        self.op = op
        self.right = right


class Var(AST):
    """The Var node is constructed out of Identifier token."""
    def __init__(self, token,array_index=None):
        self.token = token
        self.value = token.value
        self.array_index=array_index #Saving only the value

    def __str__(self):
        
        return '[ {value} {lineno}:{column}]'.format(
            value=repr(self.value),
            lineno=self.token.linenum,
            column=self.token.column,
        )

    def __repr__(self):
        return self.__str__()


class NoOp(AST):
    pass


class Program(AST):
    def __init__(self,  main, functions=None,):
        self.functions = functions
        self.main = main


class MainFunction(AST):
    def __init__(self, block,return_type):
        self.block = block
        self.return_type = return_type


class Block(AST): #must have declarations
    def __init__(self,compound_statement):
        self.compound_statement = compound_statement
        # self.declarations=declarations


class Compound(AST): #A list of statements, the body
    """Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []



class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):  #The token and token's value num/date
    def __init__(self, token,array_type=None):
        self.token = token
        self.array_type=array_type
        self.value = token.value


# class Param(AST):
#     def __init__(self, var_node, type_node):
#         self.var_node = var_node
#         self.type_node = type_node


class FunctionDecl(AST):
    def __init__(self, func_name, formal_params, block_node, return_type, return_expression ):
        self.func_name = func_name
        self.formal_params = formal_params  # a list of Param nodes
        self.block_node = block_node
        self.return_type = return_type 
        self.return_expression = return_expression

class ReturnNode(AST):
    def __init__(self,expression):
        self.return_expression=expression


class PrintNode(AST):
    def __init__(self, actual_params  ):
        self.actual_params = actual_params  


class FunctionCall(AST):
    def __init__(self, func_name, actual_params, token):
        self.func_name = func_name
        self.actual_params = actual_params  # a list of AST nodes,actual parameters
        self.token = token
        # # a reference to procedure declaration symbol
        # self.proc_symbol = None


class IfNode(AST):
    def __init__(self, boolean_expression, statements):
        self.expression = boolean_expression
        self.statements = statements


class IfElseNode(AST):
    def __init__(self, boolean_expression, statements, else_statements):
        self.expression = boolean_expression
        self.statements = statements
        self.else_statements = else_statements


class UntilNode(AST):
    def __init__(self, boolean_expression, statements):
        self.expression = boolean_expression
        self.statements = statements

class ArrayNode(AST):
    def __init__(self, values):
        self.values = values

# class ExprNode(AST):
#     def __init__(self, left, expression, right):
#         self.left = left
#         self.expression = expression   #In the case of not it is an expression, otherwise and operation :and not >
#         self.right = right