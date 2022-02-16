from NFA import NFA 
from DFA import DFA 
from Input_Parser import InputParser

#getting the input in list format
states,symbols,rules,final_state=InputParser('test.txt').get_output()
#creating the NFA object
nfa_obj=NFA(states,symbols,rules,final_state)
nfa_obj.convert_to_dict()
nfa_obj.printFA("NFA")

#Creating the DFA object from the NFA object
dfa_obj=DFA(nfa_obj)
#Transforming to DFA
dfa_obj.convert_NFA()
dfa_obj.printFA("DFA")
