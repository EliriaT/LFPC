import nested_dict as nd

class NFA:
    def __init__(self, states, symbols,rules,final_state):
        self.states = states
        self.symbols = symbols
        self.rules = rules
        self.final_state=final_state

    #Converting to dictionary representation
    def convert_to_dict(self):
        self.dict_NFA=nd.nested_dict(2, set)
        for rule in self.rules:
            self.dict_NFA[rule[0]][rule[1]].add(rule[2])  
        self.dict_NFA=self.dict_NFA.to_dict()

    #Printing the finate automaton
    def printFA(self,type):
        print("\n----------------------------------------------------\nThe %s is: "% (type))
        for key in self.dict_NFA:
            print (key+": "+str(self.dict_NFA[key]))
        print("\nFinal states are :", self.final_state)
        print("----------------------------------------------------\n")
        