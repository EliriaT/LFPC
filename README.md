## University Laboratories Works on Formal Languages and Compiler Design course

#### 1. Lab 1 - Regular Grammar to Finite Automata
#### 2. Lab 2 - NFA to DFA conversion
#### 3. Lab 3 - Lexer
#### 4. Lab 4 - Chomsky Normal Form
#### 5. Lab 4.5 - Greibach Normal Form
#### 6. Lab 6 - Parser and AST construction
---
### Final laboratory 6 results:
Example program input in `functions2.utm`:
```
num main:
\
    string message ;
    message = HelloFAF("Irina",2022.03.09, [9.8,2.5,7.6,7.1555,9.880],5);
    num calculate;
    calculate=5*(5+4) + 15 /8 ;
    print(message);
\
```

Program output: 

##### AST(Abstract Syntax Tree) image result:

![ast](https://user-images.githubusercontent.com/67596753/168443708-7d512b9f-466c-49c4-9616-c470c9476c80.png)

Another example of valid program:

```
string  func HelloFAF(string firstName, lastName; date today; array num marks; num length ;):
\
    string name;
    name=firstName+lastName;

    num i, calculate;
    string test;
    calculate=(4+5)*25;
    i=0;

    if [i!=0] \ print("Error"); \;

    num average;
    until[i<length]
    \
        average=average+marks[i];
        i=i+1;
    \;
    average=average/length;
    string text;
    text = "Hi {   name }. Nice to meet you today on this beautiful day of {today}. You average mark is: {average} .";
    text="test";
    return text;
\


num main:
\
    string message ;
    message = HelloFAF("Irina","Tiora",2022.03.09, [9.8,2.5,7.6,7.1555,9.880],5);
    print(message);
\
```

Designed Language Grammar:
```
VN = {<program>,<function-decl>,<main_function>, <type> , <identifier> ,<var-decl>, <statements>, <char>, <nums_char> ,<digit> ,<starting_digit> , <type> , |<expression>, <func-call> , <literals> ,<return-statement> ,<num-literal>, <date-literal>  , <year> , <month>, <day>  , <delimeter> ,<string-literal> ,<bool-literal>, <array-literal>, <flow-control>, <expression>, <term>, <factor>, <exp>, <assignment>, <logic-operator>};


VT ={func, main, :, \, -, _, +, - , * , / , ( , ) , < , > , = , <= ,>= ,== ,num , string ,date, bool ,array ,[ , ], return,until,if ,else,and,or,**, 0,1….9,  a | b | ... | z | A | B | ... | Z |,}
[ ]  - is  optional
* - zero or more occurances
[ ]  - terminal
() - terminal
()-used for grouping


<program>→<function-decl>* <main_function>
<function-decl>→<type> func <identifier> ( <var-decl>; * ) : \ <statements>*  ;\
<main_function> →<type> main : \ <statements>*  \
<identifier>→<char> <nums_char>* | <char> <nums_char>* [<num-literal>]
<char>→ a | b | ... | z | A | B | ... | Z | _ | 
<nums_char>→<char> | <digit> | - | 
<digit>→0 | <starting_digit>
<starting_digit> → 1 | 2 | ... | 9
<var-decl> → [array] <type> <identifier>* 
<type>→num | string | date | bool
<statement>→<var-decl> | <func-call> | <flow-control>| <return-statement> | <assignment> |<expression>;
<func-call>→ <identifier>((<identifier>| <literals> ,)*)
<literals>→<num-literal> | <date-literal> | <string-literal> | <bool-literal> |  <array-literal>
<return-statement>→ return <boolean_expressions> 
<num-literal>→[-|+]<starting_digit> <digit>* | 0.<digit>+
<date-literal> → <year><delimeter> <month><delimeter> <day>
<year>  → <starting_digit><digit><digit><digit>
<month>  → 0<digit> | 10 |11 |12
<day> → <starting_digit><digit>
<delimeter> → - 
<string-literal>→”<chars>*  [{<identifier>}]”
<bool-literal>→ true | false
<array-literal>→[   (<identifier>| <literals>|<expression> ,)*   ]
<flow-control>→ if [ <expression> ]  \ <statements>* \  else    \  <statements>*  \   
                     | until[ <expression> ]   \ <statements>* \
<boolean_expressions>→comp_expr ((AND|OR) comp_expr)*
comp_expr		→ NOT (comp_expr) |
						expr (<logic-operator> expr)*
expr	→	term ((+|-) term)*
<term>→<factor> [ * | /  <factor>]*
<factor>→<factor> [** <factor>]* | (+|-)<factor> |( <boolean_expressions> )|<identifier> | <num-literal> | <string-literal>|  <func-call>

 <assignment>→ <identifier>   =  <boolean_expressions> 
<logic-operator>→ == | < | > | != | >= | <=
```
