from Chomsky_Normal import Chomsky_Normal
from Input_Parser import InputParser

#Get the input to InputParser class
non_terminals,terminals,productions=InputParser('myVariant4.txt').get_output()

#Transform CFG to CNF
Chomsky_grammar = Chomsky_Normal(non_terminals,terminals, productions)
Chomsky_grammar.convert_to_Chosmky()
Chomsky_grammar.print_Chomsky_grammar()