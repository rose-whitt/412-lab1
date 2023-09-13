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
line_num = 0

class Scanner:

    def __init__(self, input_file):
        # init all variables like buffer and shit
        self.input_file = input_file
        self.mode_flag = ''
        self.cur_line = cur_line
        self.char_idx = char_idx
        self.cur_line_len = 0
        self.line_num = 0
        self.num_scanner_errors = 0
        self.END_OF_FILE = False

        self.num_iloc_ops = 0
        self.num_parser_errors = 0

      
        self.CATEGORIES = CATEGORIES
        self.opcodes = ["load", "store", "loadI", "add", "sub", "mult", "lshift", "rshift", "output", "nop"]
        self.opcodes_to_categories = {"load": 0, "store": 0, "loadI": 1, "add": 2, "sub": 2, "mult": 2, "lshift": 2, "rshift": 2, "output": 3, "nop": 4, ",": 7, "=>": 8}
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


    

    

    def rollback_ascii(self):
        self.char_idx -= 1
        return self.cur_line[self.char_idx]
    
    def next_ascii_char(self):
        self.char_idx += 1
        return self.cur_line[self.char_idx]
    

    def convert_line_to_ascii_list(self, line):
        
        buf = []
        newline_flag = False
        i = 0
        for char in line:
            if (char != '\n'):
                buf.append(ord(char))
            else:   # do not add new line to buf
                newline_flag = True
                break
            i += 1
        
        # print("i: " + str(i) + ", len: " + str(len(buf)))
        self.line_num += 1
        self.char_idx = -1
        # print("new line flag: " + str(newline_flag))

        self.cur_line_len = len(buf)
        if (self.cur_line_len == 0 and newline_flag != True):
            self.END_OF_FILE = True
            buf.append("")
            self.cur_line_len += 1
        else:
            # print("[CONVERSION] new line flag: " + str(newline_flag))
            buf.append(ord(' '))    # add blank
            buf.append(ord('\n'))   # add new line
            self.cur_line_len += 2
        

        # print("[CONVERSION] buf: " + str(buf))

        
        return buf

    
    # returns when it finds a token, return token
    def get_token(self):
        """
        Scans a line and returns token

        Input: 
        - line: current line being scanned
        - pos: index position of the word in the line
        - line_num: line number of the current line

        Output: token: category index (int), opcode index (int)
        """
        
        #this is like the shit in main_scanner
        # ret_token = '< ENDFILE, "" >'   # this is so we dont get infinite loop cuz scan_func expects this EOF token
        # line_num += 1
        # print("in get token")
        i = 0

        # c = -1
        if (self.END_OF_FILE != True):
            # print("not end of file")
            c = self.next_ascii_char()
            # return self.main_scanner(c)
        else:
            # print("end of file")
            c = 0
            # return self.main_scanner(c)
        

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
                            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.MEMOP]) + ', "' + "store" + '" >')
                            opcode = self.opcodes.index("store")
                            # return [self.MEMOP, "store"]
                            return self.MEMOP, opcode
                        else:
                            sys.stderr.write("ERROR " + str(self.line_num) + ':               "stor" is not a valid word - [SCANNER]\n')
                            self.num_scanner_errors += 1
                            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                            return self.SCANNER_ERROR, -1
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "sto" is not a valid word - [SCANNER]\n')
                        self.num_scanner_errors += 1
                        if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                        return self.SCANNER_ERROR, -1
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "st" is not a valid word - [SCANNER]\n')
                    self.num_scanner_errors += 1
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                    return self.SCANNER_ERROR, -1
            elif (c == ord('u')):    # sub (ARITHOP)
                # next char
                i += 1
                c = self.next_ascii_char()
                if (c == ord('b')):
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.ARITHOP]) + ', "' + "sub" + '" >')
                    opcode = self.opcodes.index("sub")
                    
                    return self.ARITHOP, opcode

                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "su" is not a valid word - [SCANNER]\n')
                    self.num_scanner_errors += 1
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                    return self.SCANNER_ERROR, -1
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "s" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
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
                                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.ARITHOP]) + ', "' + "lshift" + '" >')
                                opcode = self.opcodes.index("lshift")

                                return self.ARITHOP, opcode
                            else:
                                sys.stderr.write("ERROR " + str(self.line_num) + ':               "lshif" is not a valid word - [SCANNER]\n')
                                self.num_scanner_errors += 1
                                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                                return self.SCANNER_ERROR, -1
                        else:
                                sys.stderr.write("ERROR " + str(self.line_num) + ':               "lshi" is not a valid word - [SCANNER]\n')
                                self.num_scanner_errors += 1
                                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                                return self.SCANNER_ERROR, -1
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "lsh" is not a valid word - [SCANNER]\n')
                        self.num_scanner_errors += 1
                        if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                        return self.SCANNER_ERROR, -1
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "ls" is not a valid word - [SCANNER]\n')
                    self.num_scanner_errors += 1
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                    return self.SCANNER_ERROR, -1                  
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
                            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.LOADI]) + ', "' + "loadI" + '" >')
                            opcode = self.opcodes.index("loadI")

                            return self.LOADI, opcode
                        else:
                            self.rollback_ascii()
                            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.MEMOP]) + ', "' + "load" + '" >')
                            opcode = self.opcodes.index("load")

                            return self.MEMOP, opcode
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "loa" is not a valid word - [SCANNER]\n')
                        self.num_scanner_errors += 1
                        if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                        return self.SCANNER_ERROR, -1
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "lo" is not a valid word - [SCANNER]\n')
                    self.num_scanner_errors += 1
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                    return self.SCANNER_ERROR, -1
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "l" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c == ord('r')):    # rshift (ARITHOP) or register
            # next char
            i += 1
            c = self.next_ascii_char()
            # print(type(c))
            if (c >= ord('0') and c <= ord('9')):
                # print("possible register")
                # reg_num = 'r' + chr(c)
                reg_num = 0
                reg_num = reg_num * 10 + c - ord('0')
                
                # print("first regnum: " + str(reg_num))
                c = self.next_ascii_char()
                while (c >= ord('0') and c <= ord('9')):  # get to end of number
                    reg_num = reg_num * 10 + c - ord('0')
                    # print("regnum: " + str(reg_num))
                    c = self.next_ascii_char()  # TODO: this may cause adding a char we dont want
                self.rollback_ascii()
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.REGISTER]) + ', "r' + str(int(reg_num)) + '" >')

                return self.REGISTER, reg_num # not an opcode
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
                                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.ARITHOP]) + ', "' + "rshift" + '" >')
                                opcode = self.opcodes.index("rshift")

                                return self.ARITHOP, opcode
                            else:
                                sys.stderr.write("ERROR " + str(self.line_num) + ':               "rshif" is not a valid word - [SCANNER]\n')
                                self.num_scanner_errors += 1
                                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                                return self.SCANNER_ERROR, -1
                        else:
                            sys.stderr.write("ERROR " + str(self.line_num) + ':               "rshi" is not a valid word - [SCANNER]\n')
                            self.num_scanner_errors += 1
                            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                            return self.SCANNER_ERROR, -1
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "rsh" is not a valid word - [SCANNER]\n')
                        self.num_scanner_errors += 1
                        if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                        return self.SCANNER_ERROR, -1

                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "rs" is not a valid word - [SCANNER]\n')
                    self.num_scanner_errors += 1
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                    return self.SCANNER_ERROR, -1
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "r" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
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
                        if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.ARITHOP]) + ', "' + "mult" + '" >')
                        opcode = self.opcodes.index("mult")

                        return self.ARITHOP, opcode
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "mul" is not a valid word - [SCANNER]\n')
                        self.num_scanner_errors += 1
                        if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                        return self.SCANNER_ERROR, -1
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "mu" is not a valid word - [SCANNER]\n')
                    self.num_scanner_errors += 1
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                    return self.SCANNER_ERROR, -1
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "m" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c == ord('a')):    # add (ARITHOP)
            # print("possible add")
            i += 1
            c = self.next_ascii_char()
            if (c == ord('d')):
                i += 1
                c = self.next_ascii_char()
                if (c == ord('d')):
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.ARITHOP]) + ', "' + "add" + '" >')
                    opcode = self.opcodes.index("add")

                    return self.ARITHOP, opcode
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "ad" is not a valid word - [SCANNER]\n')
                    self.num_scanner_errors += 1
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                    return self.SCANNER_ERROR, -1
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "a" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c == ord('n')):    # nop (NOP)
            # print("possible nop")
            i += 1
            c = self.next_ascii_char()
            if (c == ord('o')):
                i += 1
                c = self.next_ascii_char()
                if (c == ord('p')):
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.NOP]) + ', "' + "nop" + '" >')
                    opcode = self.opcodes.index("nop")

                    return self.NOP, opcode   # opcode, but doesnt need a space after it
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "no" is not a valid word - [SCANNER]\n')
                    self.num_scanner_errors += 1
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                    return self.SCANNER_ERROR, -1
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "n" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
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
                                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.OUTPUT]) + ', "' + "output" + '" >')
                                opcode = self.opcodes.index("output")
                                
                                return self.OUTPUT, opcode
                            else:
                                sys.stderr.write("ERROR " + str(self.line_num) + ':               "outpu" is not a valid word - [SCANNER]\n')
                                self.num_scanner_errors += 1
                                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                                return self.SCANNER_ERROR, -1
                        else:
                            sys.stderr.write("ERROR " + str(self.line_num) + ':               "outp" is not a valid word - [SCANNER]\n')
                            self.num_scanner_errors += 1
                            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                            return self.SCANNER_ERROR, -1
                    else:
                        sys.stderr.write("ERROR " + str(self.line_num) + ':               "out" is not a valid word - [SCANNER]\n')
                        self.num_scanner_errors += 1
                        if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                        return self.SCANNER_ERROR, -1
                else:
                    sys.stderr.write("ERROR " + str(self.line_num) + ':               "ou" is not a valid word - [SCANNER]\n')
                    self.num_scanner_errors += 1
                    if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                    return self.SCANNER_ERROR, -1
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "o" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c == ord('=')):    # => (INTO)
            # print("possible =>")
            i += 1
            c = self.next_ascii_char()
            # print("next char after equal: " + chr(c))
            if (c == ord('>')):
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.INTO]) + ', "' + "=>" + '" >')
                

                return self.INTO, -1    # not an opcode but a valid category
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "=" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c == ord('/')):    # COMMENT
            # print("possible comment")
            # next char
            i += 1
            c = self.next_ascii_char()
            # print("c: " + chr(c))

            if (c == ord('/')):
                # next char
                # i += 1
                # c = self.next_ascii_char()
                self.char_idx = -1
                # print("ITS A COMMENT CUNT")
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                # not an opcode but a valid category
                return self.EOL, -1 # ignore comments, just treat EOL
            else:
                self.rollback_ascii()
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "/" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c == ord(',')):    # COMMA
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.COMMA]) + ', "' + "," + '" >')

            return self.COMMA, -1   # not an opcode but a valid category
        elif (c == ord('\n') or c == 10):   # EOL, Line Feed (LF) is used as a new line character in linux, ascii value is 10
            # print("new line")
            self.char_idx = -1
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')

            return self.EOL, -1   # not an opcode but a valid category
        elif (c == ord('\r')):
            i += 1
            c = self.next_ascii_char()
            if (c == ord('\n')):
                # print("one of the weird new lines")
                self.char_idx = -1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')

                return self.EOL, -1   # not an opcode but a valid category
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "\r" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c >= ord('0') and c <= ord('9')):   #CONSTANT, 48 to 57

            # we get it as an ascii value (integer)
            constant = 0
            # print("possible constant: " + chr(c) + ", " + str(c))
            constant = constant * 10 + c - ord('0')
            # print("first constant: " + str(constant))
            i += 1
            c = self.next_ascii_char()
            while (c >= ord('0') and c <= ord('9')):  # get to end of number
                # print("possible constant: " + chr(c) + ", " + str(c))
                constant = constant * 10 + c - ord('0')
                # print("constant: " + str(constant))
                c = self.next_ascii_char()  # TODO: this may cause adding a char we dont want
            self.rollback_ascii()
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.CONSTANT]) + ', "' + str(int(constant)) + '" >')

            return self.CONSTANT, constant  # not an opcode
        elif (c == 0):  # 0 is value of empty string
            # TODO: is this always the last line of the file??
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOF]) + ', "' + '' + '" >')
            
            return self.EOF, -1 # not an opcode
        elif (c == ord(' ') or c == ord('\t')):
            # TODO: or should i just do get next char and return
            return self.BLANK, -1   # not an opcode
        else:
            sys.stderr.write("ERROR " + str(self.line_num) + ':               ' + chr(c) + ' is not a valid word - [SCANNER]\n')
            self.num_scanner_errors += 1
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
            return self.SCANNER_ERROR, -1
