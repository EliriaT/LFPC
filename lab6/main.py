from fileinput import filename
from Token_Types import TokenType
from lexer import Lexer,Error
from parser import Parser
from ASTplot import ASTPlotter
import os

#filename = sys.argv[1]
filename='functions2.utm'
program = open(filename,"r")
program_content = program.read()


lexer = Lexer(program_content)
tokens, errors = lexer.tokenise()
print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
for i in tokens:
    if i.type == TokenType.NEWLINE: 
        print()
    else : print(i, end =" ")


if(isinstance(errors,Error)):
    print(errors.print_message())
print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")

parser = Parser(tokens)
ast_tree=parser.parse()

ast_plot = ASTPlotter(ast_tree)
content = ast_plot.gendot()
f = open("ast.dot", "w")
f.write(content)
f.close()

os.system("./setdotlabelwidth 20 < ast.dot | dot -Tpng -o ast.png && xdg-open ast.png")
