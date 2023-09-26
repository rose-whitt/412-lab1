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
        self.cur_line_len = len(self.cur_line)
        self.char_idx = char_idx
        self.cur_line_len = 0
        self.line_num = 0
        self.num_scanner_errors = 0
        self.END_OF_FILE = False

        self.num_iloc_ops = 0
        self.num_parser_errors = 0

        self.num_error_lines = 0

      
        self.CATEGORIES = CATEGORIES
        self.opcodes = ["load", "store", "loadI", "add", "sub", "mult", "lshift", "rshift", "output", "nop"]
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
        
        self.line_num += 1
        self.char_idx = -1


        self.cur_line_len = i


        if (self.cur_line_len == 0 and newline_flag != True):
            self.END_OF_FILE = True
            buf.append("")
            self.cur_line_len += 1
        else:
            # print("[CONVERSION] new line flag: " + str(newline_flag))
            buf.append(32)    # add blank
            buf.append(10)   # add new line
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
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            # return self.main_scanner(c)
        else:
            # print("end of file")
            c = 0
            # return self.main_scanner(c)
        

        if (c == 115):
            # next char
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            if (c == 116):    # t ; store (MEMOP)
                # next char
                i += 1
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                if (c == 111):  # o
                    # next char
                    i += 1
                    self.char_idx += 1
                    c = self.cur_line[self.char_idx]
                    if (c == 114):  # r
                        # next char
                        i += 1
                        self.char_idx += 1
                        c = self.cur_line[self.char_idx]
                        if (c == 101):  # e
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
            elif (c == 117):    # u ; sub (ARITHOP)
                # next char
                i += 1
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                if (c == 98):   # b
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
        elif (c == 108):
            # next char
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            if (c == 115):
                # print("possible lshift")
                i += 1
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                if (c == 104):
                    i += 1
                    self.char_idx += 1
                    c = self.cur_line[self.char_idx]
                    if (c == 105):  # i
                        i += 1
                        self.char_idx += 1
                        c = self.cur_line[self.char_idx]
                        if (c == 102):  # f
                            i += 1
                            self.char_idx += 1
                            c = self.cur_line[self.char_idx]
                            if (c == 116):
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
            elif (c == 111):
                # next char
                i += 1
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                if (c == 97):
                    # next char
                    i += 1
                    self.char_idx += 1
                    c = self.cur_line[self.char_idx]
                    if (c == 100):
                        # next char
                        i += 1
                        self.char_idx += 1
                        c = self.cur_line[self.char_idx]
                        if (c == 73): # I ; loadI (LOADI)
                            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.LOADI]) + ', "' + "loadI" + '" >')
                            opcode = self.opcodes.index("loadI")

                            return self.LOADI, opcode
                        else:
                            self.char_idx -= 1  # rollback
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
        elif (c == 114):    # r ; rshift (ARITHOP) or register
            # next char
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            # print(type(c))
            if (c >= 48 and c <= 57):
                # print("possible register")
                # reg_num = 'r' + chr(c)
                reg_num = 0
                reg_num = reg_num * 10 + c - 48
                
                # print("first regnum: " + str(reg_num))
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                while (c >= 48 and c <= 57):  # get to end of number
                    reg_num = reg_num * 10 + c - 48
                    self.char_idx += 1
                    c = self.cur_line[self.char_idx]
                self.char_idx -= 1  # rollback
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.REGISTER]) + ', "r' + str(int(reg_num)) + '" >')

                return self.REGISTER, reg_num # not an opcode
            elif (c == 115):    # s
                # print("possible rshift")
                i += 1
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                if (c == 104):  # h
                    i += 1
                    self.char_idx += 1
                    c = self.cur_line[self.char_idx]
                    if (c == 105):  # i
                        i += 1
                        self.char_idx += 1
                        c = self.cur_line[self.char_idx]
                        if (c == 102):  # f
                            i += 1
                            self.char_idx += 1
                            c = self.cur_line[self.char_idx]
                            if (c == 116):  # t
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
        elif (c == 109):    # mult (ARITHOP)
            # print("possible mult")
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            if (c == 117):
                i += 1
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                if (c == 108):  # l
                    i += 1
                    self.char_idx += 1
                    c = self.cur_line[self.char_idx]
                    if (c == 116):
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
        elif (c == 97):    # add (ARITHOP)
            # print("possible add")
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            if (c == 100):
                i += 1
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                if (c == 100):
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
        elif (c == 110):    # nop (NOP)
            # print("possible nop")
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            if (c == 111):
                i += 1
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                if (c == 112): # p
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
        elif (c == 111):    # o ; output (OUTPUT)
            # print("possible output")
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            if (c == 117):  # u
                i += 1
                self.char_idx += 1
                c = self.cur_line[self.char_idx]
                if (c == 116):  # t
                    i += 1
                    self.char_idx += 1
                    c = self.cur_line[self.char_idx]
                    if (c == 112):  # p
                        i += 1
                        self.char_idx += 1
                        c = self.cur_line[self.char_idx]
                        if (c == 117):  # u
                            i += 1
                            self.char_idx += 1
                            c = self.cur_line[self.char_idx]
                            if (c == 116):  # t
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
        elif (c == 61):    # => (INTO)
            # print("possible =>")
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            # print("next char after equal: " + chr(c))
            if (c == 62):
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.INTO]) + ', "' + "=>" + '" >')
                

                return self.INTO, -1    # not an opcode but a valid category
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "=" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c == 47):    # COMMENT
            # print("possible comment")
            # next char
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            # print("c: " + chr(c))

            if (c == 47): # /
                self.char_idx = -1
                # print("ITS A COMMENT CUNT")
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                # not an opcode but a valid category
                return self.EOL, -1 # ignore comments, just treat EOL
            else:
                self.char_idx -= 1
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "/" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c == 44):    # COMMA
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.COMMA]) + ', "' + "," + '" >')

            return self.COMMA, -1   # not an opcode but a valid category
        elif (c == 10):   # EOL, Line Feed (LF) is used as a new line character in linux, ascii value is 10
            # print("new line")
            self.char_idx = -1
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')

            return self.EOL, -1   # not an opcode but a valid category
        elif (c == 13): # \r
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            if (c == 10):
                # print("one of the weird new lines")
                self.char_idx = -1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')

                return self.EOL, -1   # not an opcode but a valid category
            else:
                sys.stderr.write("ERROR " + str(self.line_num) + ':               "\r" is not a valid word - [SCANNER]\n')
                self.num_scanner_errors += 1
                if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
                return self.SCANNER_ERROR, -1
        elif (c >= 48 and c <= 57):   #CONSTANT, 48 to 57

            # we get it as an ascii value (integer)
            constant = 0
            # print("possible constant: " + chr(c) + ", " + str(c))
            constant = constant * 10 + c - 48
            # print("first constant: " + str(constant))
            i += 1
            self.char_idx += 1
            c = self.cur_line[self.char_idx]
            while (c >= 48 and c <= 57):  # get to end of number
                # print("possible constant: " + chr(c) + ", " + str(c))
                constant = constant * 10 + c - 48
                # print("constant: " + str(constant))
                self.char_idx += 1
                c = self.cur_line[self.char_idx]  # TODO: this may cause adding a char we dont want
            self.char_idx -= 1
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.CONSTANT]) + ', "' + str(int(constant)) + '" >')

            return self.CONSTANT, constant  # not an opcode
        elif (c == 0):  # 0 is value of empty string
            # TODO: is this always the last line of the file??
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOF]) + ', "' + '' + '" >')
            
            return self.EOF, -1 # not an opcode
        elif (c == 32 or c == 9):   # blank or tab
            return self.BLANK, -1   # not an opcode
        else:
            sys.stderr.write("ERROR " + str(self.line_num) + ':               ' + chr(c) + ' is not a valid word - [SCANNER]\n')
            self.num_scanner_errors += 1
            if (self.mode_flag == '-s'): print(str(self.line_num) + ": < " + str(self.CATEGORIES[self.EOL]) + ', "' + "\\n" + '" >')
            return self.SCANNER_ERROR, -1
