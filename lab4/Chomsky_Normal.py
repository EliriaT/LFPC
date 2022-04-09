from collections import defaultdict
import json
class Chomsky_Normal:
    #Neccesary parameters of the class constructor
    def __init__(self,non_terminals,terminals, productions):
        self.non_terminals = dict((el,1) for el in non_terminals)
        self.terminals = dict((el,1) for el in terminals)
        self.productions = productions
        self.x=dict()
        self.y=dict()
        
    #Function to Eliminate empty productions
    def eliminate_empty(self):
        flag=True
        #While loop for checking if empty productions appear in the for loop proccess
        while(flag==True):
            flag=False
            for key in self.productions:
                #Finding Empty production
                if 'emp' in self.productions[key]:
                    flag=True
                    symbol=key
                    #Looping through productions to construct new states from the states where the Symbol exists
                    for second_key in self.productions:
                        for transition in self.productions[second_key]:
                            #Function for constructing new possible transition
                            self.construct_new_transition(second_key,transition,symbol)
                    #Deleting the empty production         
                    self.productions[key].remove('emp')
        #print("1 Eliminate Empty Productions: ",self.productions) 
    
    def construct_new_transition(self,key,transition,symbol):
        length=len(transition)
        for i in range(0,length):           #Looping throught the transition
            if symbol==transition[i]:       #Finding the Symbol
                if (transition[:i] + '' + transition[i+1:])=='': 
                    if 'emp' not in self.productions[key]: self.productions[key].append('emp')       
                elif (transition[:i] + '' + transition[i+1:]) not in self.productions[key]:self.productions[key].append(transition[:i] + '' + transition[i+1:])                #Appending the new transition by deleting the symbol at index i
                # self.productions[key]=list(set(self.productions[key]))

    #Function to eliminate Unitary Production
    def eliminate_renamings(self):
        flag=True
        #While loop for checking if Unitary Production appear in the for loop proccess
        while(flag==True):
            flag=False
            #Looping through all transitions
            for key in self.productions:
                for elem in self.productions[key]:
                    #Checking if a transition is in the non-terminals set
                    if self.non_terminals.get(elem): 
                        #Adding all the productions of that non-terminal to the key's list of transition and deleting the unitary production
                        self.productions[key].extend(self.productions[elem])
                        self.productions[key].remove(elem)
                        flag=True
        #print("2 Eliminate Unit: ",self.non_terminals,self.terminals,self.productions) 

    #Recursive function to find all the accessible non-terminals, it will start from state=S
    def get_unaccessible(self,state, accessible):
        #Base case when to stop recursion
        if(len(accessible)==len(self.productions.keys())): return 0
        #Add to accessible set the current state
        accessible.add(state)
        #Adding to accessible set all the states that can be reached through curent state
        for transition in self.productions[state]:
            for letter in transition:
                if self.non_terminals.get(letter):
                    if letter not in accessible: self.get_unaccessible(letter,accessible) #The recursive call for the reached states that are not in the set
                    
        return set(self.non_terminals.keys()).difference(accessible)  #Returning the final set of unaccessable states
        
    #Function to remove unaccessible state 
    def remove_unaccessible(self,states):
        for elem in states:
            del self.productions[elem]
            del self.non_terminals[elem]
        #print("3 Eliminate Unaccessible: ",self.non_terminals,self.terminals,self.productions) 

    #Function to find unproductive states
    def find_unproductive(self):
        #First step is finding direct productive states
        direct_productive=self.find_direct_productive()
        indirect_productive=set()
        remaining=set(self.non_terminals.keys()).difference(direct_productive)
        #Checking if a state from the remaining ones can be productive by an indirect transormation
        for state in remaining:
            for transition in self.productions[state]:
                if(self.find_indirect_productive(transition,direct_productive)): indirect_productive.add(state)
        return remaining.difference(indirect_productive)

    def find_direct_productive(self):
        productive=set()
        for key in self.productions:
            for transition in self.productions[key]:
                #If the transition consists only of terminals, than the state key is productive
                if(self.contains_terminals(transition)): productive.add(key)
        return productive

    def contains_terminals(self,transition):
        for letter in transition:
            if not(self.terminals.get(letter)): return False
        return True

    #A function to find indirect productive states: it will be productive if it contains a transition consisting only of terminals and productive symbols
    def find_indirect_productive(self,transition, direct_productive):
        for letter in transition:
            if not(self.terminals.get(letter)) and not(letter in direct_productive): return False
        return True

    #Function to check if a transition has unproductive symbols, if yes it is deleted further
    def check_transition(self,transition,unproductive:dict):
        for letter in transition:
            if unproductive.get(letter): return True
        return False

    #
    def remove_unproductive(self):
        unproductive=self.find_unproductive()
        unproductive=dict((el,1) for el in unproductive)
        self.remove_unaccessible(unproductive)
        unproductive_transition=set()
        #Firslty finding all the transitions containing unproductive states
        for transition_list in self.productions.values():
            for transition in transition_list:
                if(self.check_transition(transition,unproductive)): unproductive_transition.add(transition)
        #Deleting the corresponding transitions from the list of transitions
        self.productions ={i: [a for a in j if a not in unproductive_transition] for i,j in self.productions.items()}
        #Transforming back to a default dict
        self.productions=defaultdict(list,self.productions)
        #print("4 Eliminate Unproductive: ",self.non_terminals,self.terminals,self.productions) 
        
    def check_transition_form(self,transition:str):
        length=len(transition)
        
        #Base case when length of transition is 2
        if length==2:
            if self.terminals.get(transition[0]):

                if self.x.get(transition[0]):  
                    x_string=self.x[transition[0]] 
                    # print(x_string)
                else : 
                    x_string='X'+str(len(self.x.values()))
                    self.x[transition[0]]=x_string
                    self.productions[x_string].append(transition[0])
                    # print(x_string)
                transition = transition[:0] + x_string + transition[0 + 1:]

            if(len(transition)>2):
                if self.terminals.get(transition[2]):

                    if self.x.get(transition[2]):  
                        x_string=self.x[transition[2]] 
                        # print(x_string)
                    else : 
                        x_string='X'+str(len(self.x.values()))
                        self.x[transition[2]]=x_string
                        self.productions[x_string].append(transition[2])
                        # print(x_string)
                    transition = transition[:2] + x_string + transition[2 + 1:]
            else:
                if self.terminals.get(transition[1]):
                    if self.x.get(transition[1]):  
                        x_string=self.x[transition[1]] 
                        # print(x_string)
                    else : 
                        x_string='X'+str(len(self.x.values()))
                        self.x[transition[1]]=x_string
                        self.productions[x_string].append(transition[1])
                        # print(x_string)
                    transition = transition[:1] + x_string + transition[1 + 1:]
            return transition

        #Base case when length of transition is 3
        elif length==3: 
            #Check last two characters
            substring=transition[1:]
            if self.y.get(substring): 
                y_string=self.y[substring] 
            else : 
                y_string='Y'+str(len(self.y.values()))
                self.y[substring]=y_string
                chomsky_transition=self.check_transition_form(substring)
                self.productions[y_string].append(chomsky_transition)
            

            #Check first character
            first_character=transition[:1]
            if self.terminals.get(first_character):
                if self.x.get(first_character): 
                    x_string=self.x[first_character] 
                    first_character=x_string
                else : 
                    x_string='X'+str(len(self.x.values()))
                    self.x[first_character]=x_string
                    self.productions[x_string].append(first_character)
                    first_character=x_string

            transition = first_character+y_string
            return transition

        else :
            cut = round(length/2)
            substring_one=transition[:cut]
            substring_two=transition[cut:]

            if self.y.get(substring_one): 
                y_string_one=self.y[substring_one] 
            else : 
                y_string_one='Y'+str(len(self.y.values()))
                self.y[substring_one]=y_string_one
                chomsky_transition=self.check_transition_form(substring_one)
                self.productions[y_string_one].append(chomsky_transition)

            if self.y.get(substring_two): 
                y_string_two=self.y[substring_two] 
            else : 
                y_string_two='Y'+str(len(self.y.values()))
                self.y[substring_two]=y_string_two
                chomsky_transition=self.check_transition_form(substring_two)
                self.productions[y_string_two].append(chomsky_transition)

            return y_string_one+y_string_two

    #Function to substitute transitions that are not in Chomsky form 
    def substitute_transitions(self):
        for key in list(self.productions):
            for transition in self.productions[key]:
                i = self.productions[key].index(transition)     #Getting the index of the current transition in the list for further changing it
                if len(transition)>1:
                    # if len(transition)>2 and self.y.get(transition): #If there is already such a substitution made previously in the Y dictionary
                    #     y_string=self.y[transition] 
                    #     self.productions[key] = self.productions[key][:i]+[y_string]+self.productions[key][i+1:]        #Substituting with the Chomsky form
                    # else:
                    new_transition=self.check_transition_form(transition)       #Getting the Chomsky form transition from a recursive function
                    self.productions[key] = self.productions[key][:i]+[new_transition]+self.productions[key][i+1:]

    def convert_to_Chosmky(self):
        self.eliminate_empty()
        self.eliminate_renamings()
        unaccessible=self.get_unaccessible('S',set())
        self.remove_unaccessible(unaccessible)
        self.remove_unproductive()
        self.substitute_transitions()
        
        for key in self.productions:
            self.productions[key]=list(set(self.productions[key]))


    def print_Chomsky_grammar(self):
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        #print("5 Finals are:",self.non_terminals,self.terminals) 
        non_terminals=list(self.non_terminals.keys())
        non_terminals.extend(self.y.values())
        non_terminals.extend(self.x.values())
        self.non_terminals = dict((el,1) for el in non_terminals)

        print("___________________________________________________________________________________________________________________________________________________________________________________\n")
        print("The Chomsky Grammar is : ","Vn= ",non_terminals," Vt= ",list(self.terminals.keys())) 
        print(json.dumps(self.productions).translate(SUB))
        print("___________________________________________________________________________________________________________________________________________________________________________________\n")

