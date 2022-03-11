from fileinput import filename
import sys
from lexer import Lexer,Error

#filename = sys.argv[1]
filename='functions.utm'
program = open(filename,"r")
program_content = program.read()

# print(program_content)

lexer = Lexer(program_content)
tokens, errors = lexer.tokenise()
print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
for i in tokens:
    print(i.print_token(), end =" ")

if(isinstance(errors,Error)):
    print(errors.print_message())
print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
