from collections import defaultdict
class InputParser:
    def __init__(self,file):
        self.grammar = open(file,"r")

    #Setting the symbols of grammar
    def read_non_terminals(self):
        self.grammar.readline()
        first_line=self.grammar.readline()
        first_line=self.replace_chars(first_line)
        self.non_terminals=set()
        for sym in first_line:
            self.non_terminals.add(sym)         
        
    #Function to replace unneccesary symbols
    def replace_chars(self,line):
        replacements = [("G", ""), ("VN", ""),("VT", ""),("=", ""), ("(", ""), (")", ""), (",", ""), ("{", ""), ("}", ""),("\n",""),(".",""),(" ",""),("P", ""),("-", ""),(">", "")]
        [line := line.replace(a, b) for a, b in replacements]
        return line
    
    #Creating the list of states of the NFA by counting occurrences of 'q'
    def read_terminals(self):
        second_line=self.grammar.readline()
        second_line=self.replace_chars(second_line)
        self.terminals=set()
        for sym in second_line:
            self.terminals.add(sym)

    #Reading the third line which contains the final state and the symbols of the alphabet
    def read_productions(self):
        self.productions=defaultdict(list)
        for line in self.grammar:
            # print(line)
            line=self.replace_chars(line)
            self.productions[line[0]].append(line[1:len(line)])

    #Returning the NFA formatted grammar
    def get_output(self):
        self.read_non_terminals()
        self.read_terminals()
        self.read_productions()
        return self.non_terminals,self.terminals,self.productions
    