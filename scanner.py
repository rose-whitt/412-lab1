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
CATEGORIES = ["MEMOP", "LOADI", "ARITHOP", "OUTPUT", "NOP", "CONSTANT", "REGISTER", "COMMA", "INTO", "ENDFILE", "NEWLINE"]


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

        
    def tokenize_func(cat, lex):
        """tokens should be a string like < cat, "lex" >"""
        pre = "< "
        mid = '", "'
        post = '" >'
        return pre + cat + mid + lex + post

    

    def main_scanner(self, string):
        i = 0
        c = string
        print(type(c))
        print("string: " + chr(string))
        # store (MEMOP) or sub (ARITHOP)
        if (c == ord('s')):
            # next char
            i += 1
            c = self.next_char()
            if (c == ord('t')):    # store (MEMOP)
                # next char
                i += 1
                c = self.next_char()
                if (c == ord('o')):
                    # next char
                    i += 1
                    c = self.next_char()
                    if (c == ord('r')):
                        # next char
                        i += 1
                        c = self.next_char()
                        if (c == ord('e')):
                            # temp = ["MEMOP", "store"]
                            return ["MEMOP", "store"]
                        else:
                            return "stor ERROR"
                    else:
                        return "sto ERROR"
                else:
                    return "st ERROR"
            elif (c == ord('u')):    # sub (ARITHOP)
                # next char
                i += 1
                c = self.next_char()
                if (c == ord('b')):
                    return ["ARITHOP", "sub"]
                else:
                    return "su ERROR"
            else:
                return "s ERROR"
        elif (c == ord('l')):
            # next char
            i += 1
            c = self.next_char()
            if (c == ord('o')):
                # next char
                i += 1
                c = self.next_char()
                if (c == ord('a')):
                    # next char
                    i += 1
                    c = self.next_char()
                    if (c == ord('d')):
                        # next char
                        i += 1
                        c = self.next_char()
                        if (c == ord('I')): # loadI (LOADI)
                            return ["LOADI", "loadI"]
                        else:
                            self.rollback()
                            return ["MEMOP", "load"]
                    else:
                        return "loa ERROR"
                else:
                    return "lo ERROR"
            else:
                return "l ERROR"
        elif (c == ord('r')):    # rshift (ARITHOP) or register
            # next char
            i += 1
            c = self.next_char()
            print(type(c))
            if (c >= ord('0') and c <= ord('9')):
                print("possible register")
                reg_num = 'r' + chr(c)
                c = self.next_char()
                while (c >= ord('0') and c <= ord('9')):  # get to end of number
                    reg_num = reg_num + chr(c)
                    c = self.next_char()  # TODO: this may cause adding a char we dont want
                self.rollback()
                return ["REG", reg_num]
            elif (c == ord('s')):
                print("possible rshift")
                i += 1
                c = self.next_char()
                if (c == ord('h')):
                    i += 1
                    c = self.next_char()
                    if (c == ord('i')):
                        i += 1
                        c = self.next_char()
                        if (c == ord('f')):
                            i += 1
                            c = self.next_char()
                            if (c == ord('t')):
                                return ["ARITHOP", "rshift"]
                            else:
                                return "rshif ERROR"
                        else:
                            return "rshi ERROR"
                    else:
                        return "rsh ERROR"

                else:
                    return "rs ERROR"
            else:
                return "r ERROR"
        elif (c == ord('m')):    # mult (ARITHOP)
            print("possible mult")
            i += 1
            c = self.next_char()
            if (c == ord('u')):
                i += 1
                c = self.next_char()
                if (c == ord('l')):
                    i += 1
                    c = self.next_char()
                    if (c == ord('t')):
                        return ["ARITHOP", "mult"]
                    else:
                        return "mul error"
                else:
                    return "mu error"
            else:
                return "m error"
        elif (c == ord('a')):    # add (ARITHOP)
            print("possible add")
            i += 1
            c = self.next_char()
            if (c == ord('d')):
                i += 1
                c = self.next_char()
                if (c == ord('d')):
                    return ["ARITHOP", "add"]
                else:
                    return "ad error"
            else:
                return "a error"
        elif (c == ord('n')):    # nop (NOP)
            print("possible nop")
            i += 1
            c = self.next_char()
            if (c == ord('o')):
                i += 1
                c = self.next_char()
                if (c == ord('p')):
                    return ["NOP", "nop"]
                else:
                    return "no error (as in nop error)"
            else:
                return "n error"
        elif (c == ord('o')):    # output (OUTPUT)
            print("possible output")
            i += 1
            c = self.next_char()
            if (c == ord('u')):
                i += 1
                c = self.next_char()
                if (c == ord('t')):
                    i += 1
                    c = self.next_char()
                    if (c == ord('p')):
                        i += 1
                        c = self.next_char()
                        if (c == ord('u')):
                            i += 1
                            c = self.next_char()
                            if (c == ord('t')):
                                return ["OUTPUT", "output"]
                            else:
                                return "outpu error"
                        else:
                            return "outp error"
                    else:
                        return "out error"
                else:
                    return "ou error"
            else:
                return "o error"
        elif (c == ord('=')):    # => (INTO)
            print("possible =>")
            i += 1
            c = self.next_char()
            print("next char after equal: " + chr(c))
            if (c == ord('>')):
                return ["INTO", "=>"]
            else:
                return "= error"
        elif (c == ord('/')):    # COMMENT
            print("possible comment")
            # next char
            i += 1
            c = self.next_char()
            print("c: " + chr(c))

            if (c == ord('/')):
                # next char
                i += 1
                c = self.next_char()
                print("in comment if, c is: " + chr(c))

                return ["NEWLINE", "//"]

                # # read rest of comment
                # while (True):
                #     if (c == ord('\n')):
                #         return ["NEWLINE", "\\n"]
                #     elif (c == ord('\r')):
                #         i += 1
                #         c = self.next_char()
                #         if (c == ord('\n')):
                #             return ["NEWLINE", "\\r\\n"]
                #     i += 1
                #     c = self.next_char()
            else:
                self.rollback()
                return "NOT A COMMENT"
        elif (c == ord(',')):    # COMMA
            return ["COMMA", ","]
        elif (c == ord('\n')):   # EOL
            print("new line")
            return ["NEWLINE", "\\n"]
        elif (c == ord('\r')):
            i += 1
            c = self.next_char()
            if (c == ord('\n')):
                print("one of the weird new lines")
                return ["NEWLINE", "\\r\\n"]
        elif (c >= ord('0') and c <= ord('9')):   #CONSTANT
            constant = chr(c)
            print("possible constant: " + chr(c) + ", " + str(c))
            i += 1
            c = self.next_char()
            while (c >= ord('0') and c <= ord('9')):  # get to end of number
                print("possible constant: " + chr(c) + ", " + str(c))
                constant = constant + chr(c)
                c = self.next_char()  # TODO: this may cause adding a char we dont want
            return ["CONST", constant]
        elif (c == 0):  # 0 is value of empty string
            return ["ENDFILE", ""]
        else:
            return ["UNKNOWN", chr(c)]
        
    
    def rollback(self):
        self.char_idx -= 1
        return ord(self.cur_line[self.char_idx])


    # TODO: ask harry about this, piazza said it should be two chars but shouldnt i be checking for it running out of space in buffer? ik i am reading a line into the buffer, but am i clearing it all after each line??
    def next_char(self):
        # character 10 is a line break
        # print("[next_char] (before) len, idx, char: " + str(len(self.cur_line)) + ", " + str(self.char_idx) + ", " + str(ord(self.cur_line[self.char_idx])))
        print("[next char] line in ascii: " + str(ord(self.cur_line[0])))
        print("[next_char] len: " + str(len(self.cur_line)))
        print("[next_char] char idx: " + str(len(self.cur_line)))
        if (self.char_idx < len(self.cur_line) and self.char_idx >= 0):
            print("[next_char] char: " + str(ord(self.cur_line[self.char_idx])))


        self.char_idx += 1

        return ord(self.cur_line[self.char_idx])
    

    
    # returns when it finds a token, return token
    def get_token(self):
        """ Get a line. Returns when it finds a word.
        Returns token < ENDFILE, "" >
        """
        
        #this is like the shit in main_scanner
        # ret_token = '< ENDFILE, "" >'   # this is so we dont get infinite loop cuz scan_func expects this EOF token
        # line_num += 1
        c = self.next_char()
        return self.main_scanner(c)