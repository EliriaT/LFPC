import textwrap
from NodeVisitor import NodeVisitor

class ASTPlotter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.ncount = 1 #The node counting
        self.dot_header = [textwrap.dedent("""\
        digraph astgraph {
          node [shape=record, fontsize=12, fontname="Courier", height=0.5,width=2, margin=0,fixedsize=shape];
          ranksep=0.8;
          edge [arrowsize=1]
        """)]
        self.dot_body = []
        self.dot_footer = ['}']


    def visit_Program(self, node):
        s = '  node{} [label="Program"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        if node.functions!=None: 
            self.visit(node.functions)
            s = '  node{} -> node{}\n'.format(node._num, node.functions._num)
            self.dot_body.append(s)

        self.visit(node.main)
        s = '  node{} -> node{}\n'.format(node._num, node.main._num)
        self.dot_body.append(s)


    def visit_FunctionDecl(self,node):
        s = '  node{} [label="{} Func: {}"]\n'.format(self.ncount,node.return_type.value,node.func_name)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for param in node.formal_params:                     # list of VarDecl nodes 
            self.visit(param)
            s = '  node{} -> node{}\n'.format(node._num, param._num)
            self.dot_body.append(s)

        self.visit(node.block_node)
        s = '  node{} -> node{}\n'.format(node._num, node.block_node._num)
        self.dot_body.append(s)


    def visit_MainFunction(self,node):
        s = '  node{} [label="{} Main "]\n'.format(self.ncount, node.return_type.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.block)
        s = '  node{} -> node{}\n'.format(node._num, node.block._num)
        self.dot_body.append(s)


    def visit_Block(self, node):
        s = '  node{} [label="Block"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.compound_statement)

        s = '  node{} -> node{}\n'.format(
            node._num,
            node.compound_statement._num
        )
        self.dot_body.append(s)


    def visit_Compound(self, node):
        s = '  node{} [label="Compound"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child in node.children:
            if isinstance(child,list):
                for child2 in child:       #Because variable declaration is a list: string num,last

                    self.visit(child2)
                    s = '  node{} -> node{}\n'.format(node._num, child2._num)
                    self.dot_body.append(s)
            else:
                self.visit(child)
                s = '  node{} -> node{}\n'.format(node._num, child._num)
                self.dot_body.append(s)



    def visit_VarDecl(self, node):
        s = '  node{} [label="VarDecl"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.var_node)
        s = '  node{} -> node{}\n'.format(node._num, node.var_node._num)
        self.dot_body.append(s)

        self.visit(node.type_node)
        s = '  node{} -> node{}\n'.format(node._num, node.type_node._num)
        self.dot_body.append(s)


    def visit_Type(self, node):
        if node.array_type != None: s = '  node{} [label="{} {}"]\n'.format(self.ncount,node.array_type.value ,node.value)
        else : s = '  node{} [label="{}"]\n'.format(self.ncount, node.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1


    def visit_Literal(self, node):
        s = '  node{} [label="{} : {}"]\n'.format(self.ncount, node.value,node.literal_type.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1


    def visit_BinOp(self, node):
        if node.op.value=='<' or node.op.value=='>': node.op.value='\\'+node.op.value
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.op.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.left)
        self.visit(node.right)

        for child_node in (node.left, node.right):
            s = '  node{} -> node{}\n'.format(node._num, child_node._num)
            self.dot_body.append(s)


    def visit_UnaryOp(self, node):
        s = '  node{} [label="unary {}"]\n'.format(self.ncount, node.op.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.expr)
        s = '  node{} -> node{}\n'.format(node._num, node.expr._num)
        self.dot_body.append(s)


    def visit_Assign(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.op.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.left)
        self.visit(node.right)
        for child_node in (node.left, node.right):
            s = '  node{} -> node{}\n'.format(node._num, child_node._num)
            self.dot_body.append(s)


    def visit_Var(self, node):
        if node.array_index!=None: 
            s = '  node{} [label="{}[{}]"]\n'.format(self.ncount, node.value,node.array_index)
        else: s = '  node{} [label="{}"]\n'.format(self.ncount, node.value)
        
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1


    def visit_NoOp(self, node):
        s = '  node{} [label="NoOp"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1


    def visit_FunctionCall(self, node):
        s = '  node{} [label="FuncCall:{}"]\n'.format(
            self.ncount,
            node.func_name
        )
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for param_node in node.actual_params:
            self.visit(param_node)
            s = '  node{} -> node{}\n'.format(node._num, param_node._num)
            self.dot_body.append(s)


    def visit_IfNode(self,node):
        s = '  node{} [label="If"]\n'.format(self.ncount )
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child_node in (node.expression, node.statements):
            self.visit(child_node)
            s = '  node{} -> node{}\n'.format(node._num, child_node._num)
            self.dot_body.append(s)


    def visit_IfElseNode(self,node):
        s = '  node{} [label="If Else"]\n'.format(self.ncount )
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child_node in (node.expression, node.statements):

            self.visit(child_node)
            s = '  node{} -> node{}\n'.format(node._num, child_node._num)
            self.dot_body.append(s)

        
        s = '  node{} [label="Else"]\n'.format(self.ncount  )
        self.ncount += 1
        self.visit(node.else_statements)
        s = '  node{} -> node{}\n'.format(self.ncount-1, node.else_statements._num)
        self.dot_body.append(s)


    def visit_UntilNode(self,node):
        s = '  node{} [label="Until"]\n'.format(self.ncount )
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child_node in (node.expression, node.statements):
            self.visit(child_node)
            s = '  node{} -> node{}\n'.format(node._num, child_node._num)
            self.dot_body.append(s)


    def visit_ArrayNode(self,node):
        s = '  node{} [label="Array"]\n'.format(self.ncount )
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for elem in node.values:
            self.visit(elem)
            s = '  node{} -> node{}\n'.format(node._num, elem._num)
            self.dot_body.append(s)


    def visit_PrintNode(self,node):
        s = '  node{} [label="Print"]\n'.format(self.ncount )
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for elem in node.actual_params:
            self.visit(elem)
            s = '  node{} -> node{}\n'.format(node._num, elem._num)
            self.dot_body.append(s)


    def visit_ReturnNode(self,node):
        s = '  node{} [label="Return"]\n'.format(self.ncount )
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.return_expression)
        s = '  node{} -> node{}\n'.format(node._num, node.return_expression._num)
        self.dot_body.append(s)


    def gendot(self):
        
        self.visit(self.tree)
        return ''.join(self.dot_header + self.dot_body + self.dot_footer)



