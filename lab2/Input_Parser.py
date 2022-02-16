class InputParser:
    def __init__(self,file):
        self.nfa = open(file,"r")

    #Setting the symbols of grammar
    def define_symbols(self):
        first_line=self.nfa.readline()
        first_line=self.replace_chars(first_line)
        first_line=first_line.split(" ")          
        self.production_symbol=first_line[2]      #the u symbol in my case
        self.alphabet_symbol=first_line[1]        #the t symbol in my case   
        self.final_state_symbol=first_line[4]     #the F symbol denoting finate state
        self.initial_state=first_line[3]          #usually it is q0

    #Function to replace unneccesary symbols
    def replace_chars(self,line):
        replacements = [("AF", ""), ("=", ""), ("(", ""), (")", ""), (",", ""), ("{", ""), ("}", ""),("\n",""),(".","")]
        [line := line.replace(a, b) for a, b in replacements]
        return line
    
    #Creating the list of states of the NFA by counting occurrences of 'q'
    def create_the_states_list(self):
        states_number=self.nfa.readline().count("q")
        states=list()
        for x in range(states_number):
            states.append('q'+str(x))
        self.states=states

    #Reading the third line which contains the final state and the symbols of the alphabet
    def read_third_line(self):
        symbols, final_state=self.nfa.readline().split(self.final_state_symbol)
        symbols=self.replace_chars(symbols)
        symbols=symbols.replace(self.alphabet_symbol,"").split(" ")
        self.symbols = [ elem for elem in symbols if elem != ""]
        final_state=self.replace_chars(final_state)
        self.final_state=final_state.replace(" ","")

    #Reading the transition functions
    def read_transitions(self):
        rules=list()
        for line in self.nfa:
            line=self.replace_chars(line)
            line=line.replace(self.production_symbol,"").split(" ")
            line = [ elem for elem in line if elem != ""]
            rules.append(line)
        self.nfa.close()
        self.rules=rules
    
    #Returning the NFA formatted grammar
    def get_output(self):
        self.define_symbols()
        self.create_the_states_list()
        self.read_third_line()
        self.read_transitions()
        return self.states,self.symbols,self.rules,self.final_state
    