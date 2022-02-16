from NFA import NFA 
import nested_dict as nd

class DFA(NFA):  
    
    def __init__(self, nfa_obj):
        #Taking the grammar of the NFA
        self.nfa_obj=nfa_obj
        self.nfa_states=nfa_obj.states
        self.nfa_symbols=nfa_obj.symbols
        self.nfa_dict=nd.nested_dict(nfa_obj.dict_NFA)
        self.dict_NFA=nd.nested_dict(2, set) 
    
    #Main function in converting to DFA
    def convert_NFA(self):
        #The set of states
        Q=list()
        new_state=set({'q0'}) #Starting state
        #Finding all the new states of the DFA
        self.find_states(new_state,Q)
        self.dict_NFA=self.dict_NFA.to_dict()  
        self.states=Q
        self.find_final_states()
    
    #Function to find all the new states and transitions
    def find_states(self,state,Q):
        #If the state is already present, it is not studied further and the recursive function returns
        if state in Q:
            return Q
        else:
            print("New state is : ",self.set_to_string(state))
            #The new state is added to the list
            Q.append(state)
            for symbol in self.nfa_symbols:
                    #Finding to which state we arrive via a symbol
                    new_state=self.step(state,symbol)
                    if(len(new_state)!=0):
                        #Print the conversion steps 
                        self.print_conversion_steps(state,symbol,new_state)
                        #Constructing the dictionary form of the DFA
                        self.construct_dict(state,symbol,new_state)
                        #The recursive call of the function with the found state
                        self.find_states(new_state,Q)
                    
                    
                    
    #Function to find to which state we arrive via a symbol
    def step(self,list_nodes,symbol):
        state=set()             #The state to which we get via another composed state
        for node in list_nodes:
            #Traversing the nfa via a symbol and checking if the connection exists
            if self.nfa_dict[node][symbol]!={} :
                state.update(self.nfa_dict[node][symbol]) 
        return state

    #Function to construct the dictionary of the DFA
    def construct_dict(self,state,trans,new_state):
        str_state=''
        for x in state:
            str_state=str_state+x
        self.dict_NFA[str_state][trans]=self.set_to_string(new_state)
    
    #Print the logic of the conversion
    def print_conversion_steps(self,node,transition,destination):
        node=self.set_to_string(node)
        destination=self.set_to_string(destination)
        print("From state ", node," through [", transition,"] to ",destination)

    def set_to_string(self,set):
        str='( '
        for elem in set:
            str=str+elem
        return str+" )"

    #Find the final states of the DFA
    def find_final_states(self):
        self.final_state=list()
        for state in self.states:
            if self.nfa_obj.final_state in state:
                str=''
                for symbol in state:
                    str=str+symbol
                self.final_state.append(str)
        



