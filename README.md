# Programming-Language
## Creation of a simplified programming language.
1. Lexical Analyzer (Scanner)

    * Code takes in an input file and reads each character, ignoring spaces and comments, and creates tokens that will then be passed to the parser.
    
2. Parser

    * Code takes the tokens created from the lexical analyzer and it creates a parser three if there is no errors or the BNF rules of our language correlate.

BNF rules for the language:
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
   <term>      ->>> <term> * <factor> | <term> / <factor> | <factor>
   <factor>    ->>> ( <expr> ) | <var> | <integer>
   <integer>   ->>> <digit> | <digit> <integer>
   <digit>     ->>> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
