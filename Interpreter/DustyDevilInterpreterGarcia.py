#######################################
# IMPORTS
#######################################

#This import is to show ^ on errors. 
from strings_with_arrows import *

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


#######################################
# ERRORS
#######################################

#This error section is in charge of checking for errors as well as returning the position, type, and some details
#It also displays the file in which the error was found. 

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
        def __init__(self, pos_start, pos_end, details=''):
                super().__init__(pos_start, pos_end, 'Invalid Syntax', details)
                
class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result  = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result


#######################################
# POSITION
#######################################


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char = None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################

TT_FLOAT    = '<float>'
TT_PLUS     = '<addition>'
TT_MINUS    = '<substraction>'
TT_MUL      = '<multiplication>'
TT_DIV      = '<division>'
TT_LPAREN   = '<lparenthesis>'
TT_RPAREN   = '<rparenthesis>'
TT_COLON    = '<colon>'
TT_SCOLON   = '<semicolon>'
TT_EQUAL    = '<equal>'
TT_ASSIGN    = '<assign>'
TT_PROGSTART = '<prog_start>'
TT_PROGEND   = '<prog_end>'
TT_PROGRAM  = '<program>'
TT_NAME     = '<prog_name>'
TT_STATES   = '<stmts>'
TT_STATE    = '<stmt>'
TT_WRITE    = '<write>'
TT_ASSIGN   = '<assign>'
TT_VAR      = '<var>'
TT_IDENT    = '<ident>'
TT_CHAR     = '<char>'
TT_EXPR     = '<expr>'
TT_TERM     = '<term>'
TT_FACTOR   = '<factor>'
TT_INT      = '<integer>'
TT_DIGIT    = '<digit>'
TT_READ     = '<read>'
TT_COMMA    = '<comma>'
TT_EOF      = '<eof>'



class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
            
        if pos_end:
            self.pos_end = pos_end
    
    def __repr__(self):
        if self.value: return f'{self.value}'#f'{self.type} = {self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

class LexicalAnalyzer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in ' \n':
                self.advance()
            elif self.current_char in ' ':
                self.advance()                                        
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in CHARACTERS:
                tokens.append(self.make_word())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ':':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_ASSIGN, pos_start=self.pos))
                    self.advance()
                else:
                    tokens.append(Token(TT_COLON, pos_start=self.pos))
                    self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_EQUAL, pos_start=self.pos))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_SCOLON, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            if len(num_str) > 1:
                return Token(TT_INT, int(num_str), pos_start=self.pos)
            else :
                return Token(TT_DIGIT, int(num_str), pos_start=self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start=self.pos)
    
    
    def make_word(self):
        word_str = ''
        #char_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in CHARACTERS + '_':
            #char_count += 1
            word_str += self.current_char
            self.advance()

        #if char_count == 1:
            #return Token(TT_CHAR, str(word_str))
        if word_str == 'PROG_START':
            return Token(TT_PROGSTART,str(word_str), pos_start=self.pos)
        elif word_str == 'PROG_END':
            return Token(TT_PROGEND,str(word_str), pos_start=self.pos)
        elif word_str == 'Write':
            return Token(TT_WRITE, str(word_str), pos_start=self.pos)
        elif word_str == 'Read':
            return Token(TT_READ, str(word_str), pos_start=self.pos)
        else:
            return Token(TT_IDENT,str(word_str),  pos_start=self.pos)
    
#######################################
# NODES
#######################################

#All of these Nodes are the way to visualize the results to simulate the parse three. 

class ProgramNode:
    def __init__(self, op_tok, op_tok2, op_tok3, op_tok4, op_tok5, op_tok6):
        self.op_tok = op_tok
        self.op_tok2 = op_tok2
        self.op_tok3 = op_tok3
        self.op_tok4 = op_tok4
        self.op_tok5 = op_tok5
        self.op_tok6 = op_tok6
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.op_tok.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.op_tok2}, {self.op_tok3}, {self.op_tok4}, {self.op_tok5}, {self.op_tok6})'
    
class ProgramNameNode:
    def __init__(self, op_tok):
        self.op_tok = op_tok
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.op_tok.pos_end

    def __repr__(self):
        return f'({self.op_tok})'
    
class ProgramStartNode:
    def __init__(self, op_tok):
        self.op_tok = op_tok
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.op_tok.pos_end

    def __repr__(self):
        return f'{self.op_tok}'

class SemicolonNode:
    def __init__(self, op_tok):
        self.op_tok = op_tok
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.op_tok.pos_end

    def __repr__(self):
        return f'{self.op_tok}'
    
class StmtsNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'({self.tok})'
    
class StmtNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'({self.tok})'
    
class WriteNode:
    def __init__(self, op_tok, op_tok2, op_tok3, op_tok4, op_tok5):
        self.op_tok = op_tok
        self.op_tok2 = op_tok2
        self.op_tok3 = op_tok3
        self.op_tok4 = op_tok4
        self.op_tok5 = op_tok5
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.op_tok.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.op_tok2}, {self.op_tok3}, {self.op_tok4}, {self.op_tok5})'
    
class ReadNode:
    def __init__(self, op_tok, op_tok2, op_tok3, op_tok4, op_tok5):
        self.op_tok = op_tok
        self.op_tok2 = op_tok2
        self.op_tok3 = op_tok3
        self.op_tok4 = op_tok4
        self.op_tok5 = op_tok5
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.op_tok.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.op_tok2}, {self.op_tok3}, {self.op_tok4}, {self.op_tok5})'
    
class AssignNode:
    def __init__(self, op_tok, op_tok2, op_tok3, op_tok4):
        self.op_tok = op_tok
        self.op_tok2 = op_tok2
        self.op_tok3 = op_tok3
        self.op_tok4 = op_tok4
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.op_tok.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.op_tok2}, {self.op_tok3}, {self.op_tok4})'
    
class VarlNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'({self.tok})' 

class VarNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self):
        return f'({self.var_name_tok})'
    
class IdentNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'({self.tok})'
    
class ProgramEndNode:
    def __init__(self, op_tok):
        self.op_tok = op_tok
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.op_tok.pos_end

    def __repr__(self):
        return f'({self.op_tok})'
    
    
class ReadOpNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'
    
class WriteOpNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class AssignOpNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'
    

class CommaNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'({self.tok})'
    
class LParenNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class RParenNode:
    def __init__(self, tok):
        self.tok = tok
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'{self.left_node}, {self.op_tok}, {self.right_node}'
    
class VarlOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'{self.left_node}, {self.op_tok}, {self.right_node}'
    
class StmtsOpNode:
    def __init__(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node
        
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.left_node.pos_end

    def __repr__(self):
        return f'{self.left_node}, {self.right_node}'

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'{self.op_tok}, {self.node}'

#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

#######################################
# PARSER
#######################################

#The parsing starts from the program function.

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.program()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Input Error"
            ))
        sourceFile = open("DustyDevil+.out.txt", 'w')
        print('Welcome to the DustyDevil Programming Language! \n', file = sourceFile)
        return res

    ###################################
    
#This is the start. It defines the BNF Rule <program> ->>> <prog_name> PROG_START; <stmts> PROG_END; 
#All of the functions are recurvise because they call other fucntions. For example, here 5 out of the 6
#return values are called from a fucntion that will return the node, but one of them jsut keeps calling other
#functions until it finishes. This is the stmts function.
    
    def program(self):
        res = ParseResult()
        if res.error: return res
        
        return res.success(ProgramNode(res.register(self.prog_name()), res.register(self.prog_start()), res.register(self.semicolon())
                                       , res.register(self.stmts()), res.register(self.prog_end()), res.register(self.semicolon())))

#This function returns the program name node if there is no errors. Following the BNF rule
# <prog_name> ->>> <ident>
    
    def prog_name(self):
        res = ParseResult()
        tok = self.current_tok
    
        if tok.type == TT_IDENT:
            res.register(self.advance())
            return res.success(ProgramNameNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Input Error"
            ))

#This function returns the program start node if there is no errors. It looks for the program start token.

    def prog_start(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_PROGSTART:
            res.register(self.advance())
            return res.success(ProgramStartNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Syntax Error"
            ))

#This fucntion is useful for all the BNF rules that need semicolons. It can be called from other functions 
#to returnt he semicolon node.
        
    def semicolon(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_SCOLON:
            res.register(self.advance())
            return res.success(SemicolonNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Syntax Error"
            ))
        
#This functions calls the stmt function and it keeps on calling it while there is a read, write , or assign
# operations after the stmt is called. This fucntion also goes to stmtsop.
        
    def stmts(self):
        return self.stmtsop(self.stmt, [TT_READ, TT_WRITE, TT_IDENT])
  
#This function calls the write, read, or assign operator depending on what the input is.    
  
    def stmt(self):
        res = ParseResult()
        tok = self.current_tok
        
        
        if tok.type == TT_WRITE:
            return res.success(StmtNode(res.register(self.write())))
        elif tok.type == TT_READ:
            return res.success(StmtNode(res.register(self.read())))
        else:
            return res.success(StmtNode(res.register(self.assign())))
        
#This function is made to be able to have many back to back read, write, and assign operators.
        
    def stmtsop(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            #op_tok = self.current_tok
            #res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = StmtsOpNode(left, right)

        return res.success(left)
  
#This function returns an Assign node if it contains what it needs according to the BNF Rule.
#<assign> ->>> <var> := <expr>;    
  
    def assign(self):
        res = ParseResult()
        if res.error: return res
        
        return res.success(AssignNode(res.register(self.var()), res.register(self.assignop()), res.register(self.expr()) 
                                       , res.register(self.semicolon())))

#This function looks for the assign operator (:=) and if it finds it, it returns a toke for it. If not error
#is returned. 
    
    def assignop(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_ASSIGN:
            res.register(self.advance())
            return res.success(AssignOpNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Invalid Statement"
            ))

#This function returns an Write node if it contains what it needs according to the BNF Rule.
#<write> ->>> Write (<varl>);
        
    def write(self):
        res = ParseResult()
        if res.error: return res
        
        return res.success(WriteNode(res.register(self.writeop()), res.register(self.lparenthesis()), res.register(self.varl())
                                       , res.register(self.rparenthesis()), res.register(self.semicolon())))

#This function looks for the write operator (Write) and if it finds it, it returns a toke for it. If not error
#is returned.
    
    def writeop(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_WRITE:
            res.register(self.advance())
            return res.success(WriteOpNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Invalid Statement"
            ))

#This function returns an Read node if it contains what it needs according to the BNF Rule.
#<read> ->>> Read (<varl> );
        
    def read(self):
        res = ParseResult()
        if res.error: return res
        
        return res.success(ReadNode(res.register(self.readop()), res.register(self.lparenthesis()), res.register(self.varl())
                                       , res.register(self.rparenthesis()), res.register(self.semicolon())))

#This function looks for the read operator (Read) and if it finds it, it returns a toke for it. If not error
#is returned.
    
    def readop(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_READ:
            res.register(self.advance())
            return res.success(ReadOpNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Invalid Statement"
            ))
        
#This function calls the varl_op function.
        
    def varl(self):
        return self.varl_op(self.expr, TT_COMMA) #Testing putting .expr instead of .var
    
#This function calls the var operator and it keeps on calling it while there is a comma after it.
    
    def varl_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = VarlOpNode(left, op_tok, right)

        return res.success(left)
    
##This function looks for comma operator (,) and if it finds it, it returns a toke for it. If not error
#is returned. 
    
    def comma(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_COMMA:
            res.register(self.advance())
            return res.success(CommaNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Syntax Error"
            ))
        
#This function looks to see if there is an identifier, and if there is we return a var node.        
            
    def var(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_IDENT:
            res.register(self.advance())
            return res.success(VarNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Invalid Statement"
            ))
     
##This function looks for left parenthesis operator (() and if it finds it, it returns a toke for it. If not error
#is returned.        
        
    def lparenthesis(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_LPAREN:
            res.register(self.advance())
            return res.success(LParenNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Syntax Error"
            ))

##This function looks for comma operator ()) and if it finds it, it returns a toke for it. If not error
#is returned.
        
    def rparenthesis(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_RPAREN:
            res.register(self.advance())
            return res.success(RParenNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Syntax Error"
            ))
        
#This function check for numbers. It is able to detect negative and positive number, parenthesis, and 
#identifiers.
  
    def integer(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            integer = res.register(self.integer())
            if res.error: return res
            return res.success(UnaryOpNode(tok, integer))
        
        elif tok.type in (TT_INT, TT_FLOAT, TT_DIGIT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_IDENT:
            res.register(self.advance())
            return res.success(VarNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
        
        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Invalid Expression"
        ))
 
#This function calls the integer fucntion and it continues to call it while there is a multiply or division token after.

    def term(self):
        return self.bin_op(self.integer, (TT_MUL, TT_DIV))

#This function calls the term function and it continues to call it while there is a plus or minus token after.

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
 
#This function is able call another function while the operator given are in there. 
 
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

#This function returns the program end node if there is no errors. It looks for the program start token. 
    
    def prog_end(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type == TT_PROGEND:
            res.register(self.advance())
            return res.success(ProgramEndNode(tok))
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Syntax Error"
            ))
        
        

#######################################
# RUNTIME RESULT
#######################################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

#######################################
# VALUES
#######################################

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return str(self.value)


#######################################
# CONTEXT
#######################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

#######################################
# INTERPRETER
#######################################


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################
    
    def visit_ProgramNode(self, node, context):
        res = RTResult()
        var_name = node.op_tok4
        value = res.register(self.visit(var_name, context))
        if res.error: return res

        #context.symbol_table.set(var_name, value)
        return res.success(value)
    
    def visit_StmtsNode(self, node, context):
        
        res = RTResult()
        var_name = node.tok
        value = res.register(self.visit(var_name, context))
        if res.error: return res

        #context.symbol_table.set(var_name, value)
        return res.success(value)
        
        
    def visit_StmtsOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res
        
        #result, error = left.stmts(right)
        
        left = StmtsOpNode(left, right)
        
        return res.success(left)#.set_pos(node.pos_start, node.pos_end))
        
        
        
    def visit_StmtNode(self, node, context):
        res = RTResult()
        var_name = node.tok
        value = res.register(self.visit(var_name, context))
        if res.error: return res

        #context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )


    def visit_VarNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        
        
        value = global_symbol_table.get(var_name)
        
        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        #value = value.copy().set_pos(node.pos_start, node.pos_end)
        sourceFile = open("DustyDevil+.out.txt", 'a')
        print(f'{var_name} = {value}', file = sourceFile)
        print(f'{var_name} = {value}')
        return res.success(value)
    
    
    def visit_VarlNode(self, node, context):
        
        res = RTResult()
        value = res.register(self.visit(node.tok , context))
        return res.success(value)
    
    
    def visit_VarlOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        left = VarlOpNode(left, '', right)
        
        return res.success(left)

    def visit_AssignNode(self, node, context):
        res = RTResult()
        var_name = node.op_tok
        var_name1 = str(var_name)
        var_name2 = var_name1[1:-1]
        value = res.register(self.visit(node.op_tok3, context))
        
        if res.error: return res
        
        context.symbol_table.set(var_name2, value)
        #global_symbol_table.set(var_name, value)
        #print(var_name, context.symbol_table.get(var_name))
        #print(context.symbol_table.get(var_name))
        return res.success(value)
    
    
    def visit_WriteNode(self, node, context):
        res = RTResult()
        value = res.register(self.visit(node.op_tok3, context))
        
        return res.success(value)
        
    def visit_ReadNode(self, node, context):
        
        res = RTResult()
        var_name = node.op_tok3
        var_name1 = str(var_name)
        
        new = var_name1.split(", ")
        for x in range(0, len(new), 2):
            var_name1 = new[x]
            var_name2 = var_name1[1:-1]
            value = input(f"Enter a value for {var_name2}: ")
            value = int(value)
            value = Number(value)
            if res.error: return res
        
            context.symbol_table.set(var_name2, value)
        
        return res.success('')
        
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))




#######################################
# RUN
#######################################


global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

#This is the run function that initializes the lexer and parser and returns the ast node or error.

def run(fn, text):
    lexer = LexicalAnalyzer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error
    
    parser = Parser(tokens)
    ast = parser.parse()

    #return ast.node, ast.error
    #return tokens, error
    
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    '''
    global_symbol_table.set('Five', 5)
    global_symbol_table.set('Three', 3)
    global_symbol_table.set('Two', 2)
    global_symbol_table.set('One', 1)
    
    
    print(global_symbol_table.get('Five'))
    print(global_symbol_table.get('Three'))
    print(global_symbol_table.get('Two'))
    print(global_symbol_table.get('One'))
    '''
    
    
    return result.value, result.error
    