'''
Alejandro Garcia 
A00204253
CSCE 4220 202 SP22 - Programming Languages

The functions in my DustyDevilLexerGarcia.py file are now able to create the tokens and then use these
tokens and parse them. It is able to detect syntax errors as well as to detect error of not following the
BNF rules which are as follow:
    
<program>   ->>> <prog_name> PROG_START; <stmts> PROG_END;
<prog_name> ->>> <ident>
<stmts>     ->>> <stmt> | <stmt> <stmts>
<stmt>      ->>> <assign> | <write> | <read>
<write>     ->>> Write (<varl>);
<read>      ->>> Read (<varl> );
<assign>    ->>> <var> := <expr>;
<varl>      ->>> <var> | <var> , <varl>
<var>       ->>> <ident>
<ident>     ->>> <char> | <char> <ident>
<char>      ->>> A | B | C | … | Z | a | b | … | z
<expr>      ->>> <expr> + <term> | <expr> - <term> | <term> 
'''


import DustyDevilInterpreterGarcia

#All of the following is marked out because this is what I used to individually test values.
#This is done to be able to check if my functions are working while I am coding.
#Testing little by little is the best way to create a program.
'''
while True:
    text = input('DustyDevilInterpreterGarcia > ')
    result, error = DustyDevilInterpreterGarcia.run('<stdin>', text)
    if error:print(error.as_string())
    else: print(result)
'''

#The following opens the text file containing the input and it passes it through the run function.
#It outputs the results to the mentioned output file as well to the console.
#If error, it outputs the errors. 


text = open("DustyDevil+.in.txt", "r")
text = text.read()
result, error = DustyDevilInterpreterGarcia.run("DustyDevil+.in.txt", text)


#Print to screen

if error: print(error.as_string())
else: print(result)

#Print to file

sourceFile = open("DustyDevil+.out.txt", 'a')
if error: print(error.as_string(), file = sourceFile)
else: print(result, file = sourceFile)
#print("\nNumber of tokens: {}".format(len(result)), file = sourceFile)
sourceFile.close()

#print("\nNumber of tokens: {}".format(len(result)))