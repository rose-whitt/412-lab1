import sys
# Step 1) start off drawing out the big DFA
# Step 2) scanner is basically just a bunch of if else if statements with try catch blocks
# Step 3) pass the scanner simple strings

# Scanner reads the input stream character by character and aggregates characters into words in the ILOC language

# Scanner should read characters until it has a valid word, then it returns to parser as a <category, lexeme> pair

# Map strings into a compact set of integers. Represent strings as integers and convert to a string for output

# Assign a small integer to each category.
# Use an array of strings, statically initialized, to convert integer to a string for debugging or output


# For lab1, merge the big transition diagram with the ones for constants, registers, and comments.
# Then implement it with one of the schemes in 2.5


# ILOC categories. Use integer macros to index it.
CATEGORIES = ["MEMOP", "LOADI", "ARITHOP", "OUTPUT", "NOP", "CONST", "REG", "COMMA", "INTO", "ENDFILE", "NEWLINE"]


# category integer macros
MEMOP = 0   # load, store
LOADI = 1   # loadI
ARITHOP = 2 # add, sub, mult, lshift, rshift
OUTPUT = 3  # output, prints MEM(x) to stdout
NOP = 4     # nop, idle for one second
CONSTANT = 5    # a non-negative integer
REGISTER = 6    # 'r' followed by a constant
COMMA = 7   # ','
INTO = 8    # "=>"
EOF = 9     # input has been exhausted
EOL = 10    # end of current line ("\r\n" or "\n")
BLANK = 11     # not an opcode, but used to signal blank space or tab
SCANNER_ERROR = 12


# Double Buffer
BUF_SIZE = -1
point = -1
fence = -1
buffer = []


cur_line = ""
char_idx = -1
line_num = 1

class Scanner:

    def __init__(self, input_file):
        # init all variables like buffer and shit
        self.input_file = input_file
        self.cur_line = cur_line
        self.char_idx = char_idx
        self.line_num = 1
        self.num_scanner_errors = 0
        self.num_iloc_ops = 0

        self.token_list = []
        self.file_token_lists = []
        self.CATEGORIES = CATEGORIES
        self.MEMOP = 0   # load, store
        self.LOADI = 1   # loadI
        self.ARITHOP = 2 # add, sub, mult, lshift, rshift
        self.OUTPUT = 3  # output, prints MEM(x) to stdout
        self.NOP = 4     # nop, idle for one second
        self.CONSTANT = 5    # a non-negative integer
        self.REGISTER = 6    # 'r' followed by a constant
        self.COMMA = 7   # ','
        self.INTO = 8    # "=>"
        self.EOF = 9     # input has been exhausted
        self.EOL = 10    # end of current line ("\r\n" or "\n")
        self.BLANK = 11     # not an opcode, but used to signal blank space or tab
        self.SCANNER_ERROR = 12 # not an opcode, used to signify error in scanner (lexical/spelling error)

        
    def tokenize_func(cat, lex):
        """tokens should be a string like < cat, "lex" >"""
        pre = "< "
        mid = '", "'
        post = '" >'
        return pre + cat + mid + lex + post

    

    def main_scanner(self, string):
        i = 0
        c = string
        print("[MAIN SCANNER]: char idx: " + str(self.char_idx))
        # print(type(c))
        # print("string: " + chr(string))
        # store (MEMOP) or sub (ARITHOP)
        if (c == ord('s')):
            # next char
            i += 1
            c = self.next_ascii_char()
            if (c == ord('t')):    # store (MEMOP)
                # next char
                i += 1
                c = self.next_ascii_char()
                if (c == ord('o')):
                    # next char
                    i += 1
                    c = self.next_ascii_char()
                    if (c == ord('r')):
                        # next char
                        i += 1
                        c = self.next_ascii_char()
                        if (c == ord('e')):
                            return [self.MEMOP, "store"]
                        else:
                            sys.stderr.write("ERROR " + str(self.line_num) + ':               "stor" is not a valid word - [SCANNER]\n')
                            return [self.SCANNER_ERROR, "stor"]
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "sto" is not a valid word - [SCANNER]\n')
                        return [self.SCANNER_ERROR, "sto"]
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "st" is not a valid word - [SCANNER]\n')
                    return [self.SCANNER_ERROR, "stor"]
            elif (c == ord('u')):    # sub (ARITHOP)
                # next char
                i += 1
                c = self.next_ascii_char()
                if (c == ord('b')):
                    return [self.ARITHOP, "sub"]

                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "su" is not a valid word - [SCANNER]\n')
                    return [self.SCANNER_ERROR, "su"]
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "s" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "s"]
        elif (c == ord('l')):
            # next char
            i += 1
            c = self.next_ascii_char()
            if (c == ord('s')):
                # print("possible lshift")
                i += 1
                c = self.next_ascii_char()
                if (c == ord('h')):
                    i += 1
                    c = self.next_ascii_char()
                    if (c == ord('i')):
                        i += 1
                        c = self.next_ascii_char()
                        if (c == ord('f')):
                            i += 1
                            c = self.next_ascii_char()
                            if (c == ord('t')):
                                return [self.ARITHOP, "lshift"]
                            else:
                                sys.stderr.write("ERROR " + str(self.line_num) + ':               "lshif" is not a valid word - [SCANNER]\n')
                                return [self.SCANNER_ERROR, "lshif"]
                        else:
                                sys.stderr.write("ERROR " + str(self.line_num) + ':               "lshi" is not a valid word - [SCANNER]\n')
                                return [self.SCANNER_ERROR, "lshi"]
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "lsh" is not a valid word - [SCANNER]\n')
                        return [self.SCANNER_ERROR, "lsh"]
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "ls" is not a valid word - [SCANNER]\n')
                    return [self.SCANNER_ERROR, "ls"]                   
            elif (c == ord('o')):
                # next char
                i += 1
                c = self.next_ascii_char()
                if (c == ord('a')):
                    # next char
                    i += 1
                    c = self.next_ascii_char()
                    if (c == ord('d')):
                        # next char
                        i += 1
                        c = self.next_ascii_char()
                        if (c == ord('I')): # loadI (LOADI)
                            return [self.LOADI, "loadI"]
                        else:
                            self.rollback_ascii()
                            return [self.MEMOP, "load"]
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "loa" is not a valid word - [SCANNER]\n')
                        return [self.SCANNER_ERROR, "loa"]
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "lo" is not a valid word - [SCANNER]\n')
                    return [self.SCANNER_ERROR, "lo"]
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "l" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "l"]
        elif (c == ord('r')):    # rshift (ARITHOP) or register
            # next char
            i += 1
            c = self.next_ascii_char()
            # print(type(c))
            if (c >= ord('0') and c <= ord('9')):
                # print("possible register")
                reg_num = 'r' + chr(c)
                c = self.next_ascii_char()
                while (c >= ord('0') and c <= ord('9')):  # get to end of number
                    reg_num = reg_num + chr(c)
                    c = self.next_ascii_char()  # TODO: this may cause adding a char we dont want
                self.rollback_ascii()
                return [self.REGISTER, reg_num] # no space after necessary bc not an opcode
            elif (c == ord('s')):
                # print("possible rshift")
                i += 1
                c = self.next_ascii_char()
                if (c == ord('h')):
                    i += 1
                    c = self.next_ascii_char()
                    if (c == ord('i')):
                        i += 1
                        c = self.next_ascii_char()
                        if (c == ord('f')):
                            i += 1
                            c = self.next_ascii_char()
                            if (c == ord('t')):
                                return [self.ARITHOP, "rshift"]
                            else:
                                sys.stderr.write("ERROR " + str(self.line_num) + ':               "rshif" is not a valid word - [SCANNER]\n')
                                return [self.SCANNER_ERROR, "rshif"]
                        else:
                            sys.stderr.write("ERROR " + str(self.line_num) + ':               "rshi" is not a valid word - [SCANNER]\n')
                            return [self.SCANNER_ERROR, "rshi"]
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "rsh" is not a valid word - [SCANNER]\n')
                        return [self.SCANNER_ERROR, "rsh"]

                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "rs" is not a valid word - [SCANNER]\n')
                    return [self.SCANNER_ERROR, "rs"]
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "r" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "r"]
        elif (c == ord('m')):    # mult (ARITHOP)
            # print("possible mult")
            i += 1
            c = self.next_ascii_char()
            if (c == ord('u')):
                i += 1
                c = self.next_ascii_char()
                if (c == ord('l')):
                    i += 1
                    c = self.next_ascii_char()
                    if (c == ord('t')):
                        return [self.ARITHOP, "mult"]
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "mul" is not a valid word - [SCANNER]\n')
                        return [self.SCANNER_ERROR, "mul"]
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "mu" is not a valid word - [SCANNER]\n')
                    return [self.SCANNER_ERROR, "mu"]
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "m" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "m"]
        elif (c == ord('a')):    # add (ARITHOP)
            # print("possible add")
            i += 1
            c = self.next_ascii_char()
            if (c == ord('d')):
                i += 1
                c = self.next_ascii_char()
                if (c == ord('d')):
                    return [self.ARITHOP, "add"]
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "ad" is not a valid word - [SCANNER]\n')
                    return [self.SCANNER_ERROR, "ad"]
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "a" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "a"]
        elif (c == ord('n')):    # nop (NOP)
            # print("possible nop")
            i += 1
            c = self.next_ascii_char()
            if (c == ord('o')):
                i += 1
                c = self.next_ascii_char()
                if (c == ord('p')):
                    return [self.NOP, "nop"]    # opcode, but doesnt need a space after it
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "no" is not a valid word - [SCANNER]\n')
                    return [self.SCANNER_ERROR, "no"]
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "n" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "n"]
        elif (c == ord('o')):    # output (OUTPUT)
            # print("possible output")
            i += 1
            c = self.next_ascii_char()
            if (c == ord('u')):
                i += 1
                c = self.next_ascii_char()
                if (c == ord('t')):
                    i += 1
                    c = self.next_ascii_char()
                    if (c == ord('p')):
                        i += 1
                        c = self.next_ascii_char()
                        if (c == ord('u')):
                            i += 1
                            c = self.next_ascii_char()
                            if (c == ord('t')):
                                return [self.OUTPUT, "output"]
                            else:
                                sys.stderr.write("ERROR " + str(self.line_num) + ':               "outpu" is not a valid word - [SCANNER]\n')
                                return [self.SCANNER_ERROR, "outpu"]
                        else:
                            sys.stderr.write("ERROR " + str(self.line_num) + ':               "outp" is not a valid word - [SCANNER]\n')
                            return [self.SCANNER_ERROR, "outp"]
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "out" is not a valid word - [SCANNER]\n')
                        return [self.SCANNER_ERROR, "out"]
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "ou" is not a valid word - [SCANNER]\n')
                    return [self.SCANNER_ERROR, "ou"]
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "o" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "o"]
        elif (c == ord('=')):    # => (INTO)
            # print("possible =>")
            i += 1
            c = self.next_ascii_char()
            # print("next char after equal: " + chr(c))
            if (c == ord('>')):
                return [self.INTO, "=>"]
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "=" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "="]
        elif (c == ord('/')):    # COMMENT
            print("possible comment")
            # next char
            i += 1
            c = self.next_ascii_char()
            print("c: " + chr(c))

            if (c == ord('/')):
                # next char
                # i += 1
                # c = self.next_ascii_char()
                self.char_idx = -1
                return [self.EOL, "\\n"] # ignore comments, just treat EOL

            else:
                self.rollback_ascii()
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "/" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "/"]
        elif (c == ord(',')):    # COMMA
            return [self.COMMA, ","]
        elif (c == ord('\n') or c == 10):   # EOL, Line Feed (LF) is used as a new line character in linux, ascii value is 10
            # print("new line")
            self.char_idx = -1
            return [self.EOL, "\\n"]
        elif (c == ord('\r')):
            i += 1
            c = self.next_ascii_char()
            if (c == ord('\n')):
                # print("one of the weird new lines")
                self.char_idx = -1
                return [self.EOL, "\\r\\n"]
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "\r" is not a valid word - [SCANNER]\n')
                return [self.SCANNER_ERROR, "\r"]
        elif (c >= ord('0') and c <= ord('9')):   #CONSTANT
            constant = chr(c)
            # print("possible constant: " + chr(c) + ", " + str(c))
            i += 1
            c = self.next_ascii_char()
            while (c >= ord('0') and c <= ord('9')):  # get to end of number
                # print("possible constant: " + chr(c) + ", " + str(c))
                constant = constant + chr(c)
                c = self.next_ascii_char()  # TODO: this may cause adding a char we dont want
            self.rollback_ascii()
            return [self.CONSTANT, constant]
        elif (c == 0):  # 0 is value of empty string
            # TODO: is this always the last line of the file??
            
            return [self.EOF, ""]
        elif (c == ord(' ') or c == ord('\t')):
            # TODO: or should i just do get next char and return
            return [self.BLANK, " "]
        else:
            sys.stderr.write("ERROR " + str(self.line_num) + ':               ' + chr(c) + ' is not a valid word - [SCANNER]\n')
            return [self.SCANNER_ERROR, chr(c)]
    

    

    def rollback_ascii(self):
        self.char_idx -= 1
        return self.cur_line[self.char_idx]
    
    def next_ascii_char(self):
        print("cur idx: " + str(self.char_idx))
        # print(self.cur_line)
        if (self.char_idx >= len(self.cur_line)):
            self.cur_line = self.convert_line_to_ascii_list(self.input_file.readline())

            return ord('\n')
        elif (len(self.cur_line) == 0):
            return 0
        else:
            self.char_idx += 1
            return self.cur_line[self.char_idx]
    

    def convert_line_to_ascii_list(self, line):
        buf = []
        for char in line:
            buf.append(ord(char))
        
        return buf

    
    # returns when it finds a token, return token
    def get_token(self):
        """ Get a line. Returns when it finds a word.
        Returns token < ENDFILE, "" >
        """
        
        #this is like the shit in main_scanner
        # ret_token = '< ENDFILE, "" >'   # this is so we dont get infinite loop cuz scan_func expects this EOF token
        # line_num += 1
        c = self.next_ascii_char()
        return self.main_scanner(c)