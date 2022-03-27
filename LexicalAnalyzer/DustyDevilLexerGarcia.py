#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

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

    def advance(self, current_char):
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

#TT_INT		= 'INT'
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

#TT_IDENT    = 'IDENT'
#TT_EQUAL    = 'ASSIGN_OP'
#TT_SEMCO    = 'SEMICOLON'

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
TT_INT      = '<interger>'
TT_DIGIT    = '<digit>'






class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type} = {self.value}'
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
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == ':':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_ASSIGN))
                    self.advance()
                else:
                    tokens.append(Token(TT_COLON))
                    self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_EQUAL))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_SCOLON))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_DIGIT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
    
    
    def make_word(self):
        word_str = ''
        char_count = 0

        while self.current_char != None and self.current_char in CHARACTERS + '_':
            char_count += 1
            word_str += self.current_char
            self.advance()

        if char_count == 1:
            return Token(TT_CHAR, str(word_str))
        elif word_str == 'PROG_START' or word_str == 'PROG_END':
            return Token(TT_PROGRAM)
        elif word_str == 'Write':
            return Token(TT_WRITE)
        else:
            return Token(TT_IDENT)#, float(num_str))
    

#######################################
# RUN
#######################################

def run(fn, text):
    lexer = LexicalAnalyzer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error