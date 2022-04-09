from collections import defaultdict
import json
from Chomsky_Normal import Chomsky_Normal
import string

class Greibach_Normal_Form:
    #Neccesary parameters of the class constructor
    def __init__(self,non_terminals,terminals, productions):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.available_letters=set(string.ascii_uppercase).difference(set(non_terminals.keys())).difference(set({'X','Y'}))

        #A set of non_terminals which have only productions in Greibach form
        self.greibach_non_terminals=defaultdict(int) 
        self.non_left_factored=defaultdict(int) 


    #Function for substituting first non_terminal in a production
    def replace_production(self,key,non_terminal,index):

        for transition in self.productions[non_terminal]:
            if non_terminal[0]=='X' or non_terminal[0]=='Y': self.productions[key].append(transition+self.productions[key][index][2:])
            else:  self.productions[key].append(transition+self.productions[key][index][1:])
        del self.productions[key][index]

    #Eliminate left_recursion for a key
    def eliminate_left_recursion(self,key):
        letter=self.available_letters.pop()     
        self.non_terminals[letter]=1
        #The non_recursive productions of a non-terminal
        free_part=list()
        #The part which follows after the recursive letter
        post_recursive_part=list()

        for transition in list(self.productions[key]):
            if(transition[0]!='X' and transition[0]!='Y'):
                if transition[0]==key:                                
                    post_recursive_part.append(transition[1:])
                    self.productions[key].remove(transition)
                else: free_part.append(transition)

            elif (transition[0]=='X' or transition[0]=='Y'):

                if transition[0]+transition[1]==key:                                  
                    post_recursive_part.append(transition[2:])
                    self.productions[key].remove(transition)
                else: free_part.append(transition)

        for elem in free_part:
            self.productions[key].append(elem+letter)

        for elem in post_recursive_part:
            self.productions[letter].append(elem)
            self.productions[letter].append(elem+letter)

    def find_greibach_non_terminals(self):
        for key in self.productions:
            flag=True
            for transition in self.productions[key]:
                if self.non_terminals.get(transition[0]) or self.non_terminals.get(transition[:2]): 
                    flag=False
                    break
            if(flag): self.greibach_non_terminals[key]=1

    #Used to check for recursion after the substitution step
    def check_for_direct_recursion(self,key):
        non_terminal=''

        for transition in list(self.productions[key]):
            if (transition[0] == 'X' or transition[0] == 'Y'): non_terminal=transition[0]+transition[1]
            elif self.non_terminals.get(transition[0]): non_terminal=transition[0] 
            if non_terminal==key: 
                return True
        return False

    def print_result(self):
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

        print("___________________________________________________________________________________________________________________________________________________________________________________\n")
        print("The Greibach Grammar is : ","Vn= ",list(self.non_terminals.keys()),"\n"," Vt= ",list(self.terminals.keys()),"\n") 
        print(json.dumps(self.productions).translate(SUB))
        print("___________________________________________________________________________________________________________________________________________________________________________________\n")

    def transform_Greibach(self):
        while(len(self.greibach_non_terminals.keys())!=len(self.non_terminals.keys())):
            for key in list(self.productions.keys()):
                flag=False
                for transition in list(self.productions[key]):
                    
                    non_terminal=''
                    if self.non_terminals.get(transition[0]) or transition[0] == 'X' or transition[0] == 'Y' :
                        if (transition[0] == 'X' or transition[0] == 'Y'): non_terminal=transition[0]+transition[1]
                        else: non_terminal=transition[0]
                        if non_terminal == key: 
                            flag=True
                        else: 
                            index=self.productions[key].index(transition)
                            self.replace_production(key,non_terminal,index)

                if(flag): self.eliminate_left_recursion(key)

                elif self.check_for_direct_recursion(key): self.eliminate_left_recursion(key)
                self.find_greibach_non_terminals()
                
        Chomsky_grammar = Chomsky_Normal(self.non_terminals,self.terminals, self.productions)
        unaccessible=Chomsky_grammar.get_unaccessible('S',set())
        Chomsky_grammar.remove_unaccessible(unaccessible)
        self.terminals=Chomsky_grammar.terminals
        self.non_terminals=Chomsky_grammar.non_terminals
        self.productions=Chomsky_grammar.productions 
        

            
    def determine_factored_substring(self,key):
        frequency=defaultdict(int)
        right_part=defaultdict(list)
        for transition in list(self.productions[key]):
                length=len(transition)+1
                for i in range(1,length):
                    if transition[i-1]=='X' or transition[i-1]=='Y': substring=transition[0:i+1]
                    elif transition[i-1].isnumeric(): continue
                    else: substring=transition[0:i]
                    frequency[substring]=frequency[substring]+1
                    if transition[i:length]=='' : right_part[substring].append('emp')
                    elif transition[i-1]=='X' or transition[i-1]=='Y':
                        if transition[i+1:length]=='': right_part[substring].append('emp') 
                        else: right_part[substring].append(transition[i+1:length])
                    else : right_part[substring].append(transition[i:length])
        return frequency,right_part

    def sort_dictionary_values(self, diction):
        sorted_dict = {}
        sorted_keys = sorted(diction, key=diction.get,reverse=True) 

        for w in sorted_keys:
            sorted_dict[w] = diction[w]
        return sorted_dict

    def eliminate_left_factoring(self):
        
        for key in list(self.productions.keys()):
            flag=True
            while(flag==True):  #Untill there is a recursion for  a specific key;After eliminating a recursion, we should again update frequency, and right part
                flag=False

                frequency,right_part=self.determine_factored_substring(key)
                
                frequency=self.sort_dictionary_values(frequency)

                prefix=next(iter(frequency)) #Getting the first prefix with the biggest count occurence
                if frequency[prefix]>2 or (frequency[prefix]==2 and 'emp' not in right_part[prefix]):
                    flag=True

                    #Deleting those containing the prefix 
                    self.productions[key] = [transition for transition in self.productions[key] if not (transition.find(prefix)==0 and len(transition)>len(prefix))]

                    letter=self.available_letters.pop()    
                    self.non_terminals[letter]=1
                    self.productions[key].append(prefix+letter)
                    for substring in right_part[prefix]:
                        if(substring!='emp'): self.productions[letter].append(substring)

            self.non_left_factored[key]=1


    def eliminate_duplicates(self):
        for key in self.productions:
            self.productions[key]=list(set(self.productions[key]))


    def transform_Greibach_and_left_factor(self):

            self.eliminate_left_factoring()

            self.eliminate_duplicates()
        
