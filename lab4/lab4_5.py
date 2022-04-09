from operator import le
import string
from  Greibach_Normal_Form import  Greibach_Normal_Form
from Chomsky_Normal import Chomsky_Normal
from Input_Parser import InputParser
from collections import defaultdict
import json
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

#Get the input to InputParser class
non_terminals,terminals,productions=InputParser('myVariant9.txt').get_output()

#Transform CFG to CNF
Chomsky_grammar = Chomsky_Normal(non_terminals,terminals, productions)
Chomsky_grammar.convert_to_Chosmky()
Chomsky_grammar.print_Chomsky_grammar()

terminals=Chomsky_grammar.terminals
non_terminals=Chomsky_grammar.non_terminals
productions=Chomsky_grammar.productions

Greibach_grammar =Greibach_Normal_Form(non_terminals,terminals, productions)
Greibach_grammar.transform_Greibach()
Greibach_grammar.print_result()
# Greibach_grammar.transform_Greibach_and_left_factor()
# Greibach_grammar.print_result()


