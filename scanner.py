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

line_num = 1

class Scanner:

    def __init__(self, input_file):
        # init all variables like buffer and shit
        self.input_file = input_file
        self.BUF_SIZE = 10
        self.point = 0
        self.fence = 0
        self.buffer = [0] * self.BUF_SIZE
        self.line_num = 1
        self.CATEGORIES = CATEGORIES

        
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
        # store (MEMOP) or sub (ARITHOP)
        if (c == 's'):
            # next char
            i += 1
            c = self.next_char
            if (c == 't'):    # store (MEMOP)
                # next char
                i += 1
                c = self.next_char
                if (c == 'o'):
                    # next char
                    i += 1
                    c = self.next_char
                    if (c == 'r'):
                        # next char
                        i += 1
                        c = self.next_char
                        if (c == 'e'):
                            return '< MEMOP, "store" >'
                        else:
                            return "stor ERROR"
                    else:
                        return "sto ERROR"
                else:
                    return "st ERROR"
            elif (c == 'u'):    # sub (ARITHOP)
                # next char
                i += 1
                c = self.next_char
                if (c == 'b'):
                    return '< ARITHOP, "sub" >'
                else:
                    return "su ERROR"
            else:
                return "s ERROR"
        elif (c == 'l'):
            # next char
            i += 1
            c = self.next_char
            if (c == 'o'):
                # next char
                i += 1
                c = self.next_char
                if (c == 'a'):
                    # next char
                    i += 1
                    c = self.next_char
                    if (c == 'd'):
                        # next char
                        i += 1
                        c = self.next_char
                        if (c == 'I'): # loadI (LOADI)
                            return '< LOADI, "loadI" >'
                        elif (c == '\n' or c == '\r\n' or c == ' '):    # load (MEMOP)
                            # TODO: rollback
                            return '< MEMOP, "load" >'
                        else:
                            return "load ERROR"  #TODO- now that i think about it, they should all check tehre is a new line or sum to show end of word

                    else:
                        return "loa ERROR"
                else:
                    return "lo ERROR"
            else:
                return "l ERROR"
        elif (c == 'r'):    # rshift (ARITHOP) or register
            # next char
            i += 1
            c = self.next_char
            print(type(c))
            if (c >= 0 and c <= 9):
                print("possible register")
                reg_num = 'r' + c
                c = self.next_char
                while (c >= '0' and c <= '9'):  # get to end of number
                    reg_num = reg_num + c
                    c = self.next_char  # TODO: this may cause adding a char we dont want
                return '< REG, "' + reg_num + " >"
            elif (c == 's'):
                print("possible rshift")
                i += 1
                c = self.next_char
                if (c == 'h'):
                    i += 1
                    c = self.next_char
                    if (c == 'i'):
                        i += 1
                        c = self.next_char
                        if (c == 'f'):
                            i += 1
                            c = self.next_char
                            if (c == 't'):
                                return '< ARITHOP, "rshift" >'
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
        elif (c == 'm'):    # mult (ARITHOP)
            print("possible mult")
            i += 1
            c = self.next_char
            if (c == 'u'):
                i += 1
                c = self.next_char
                if (c == 'l'):
                    i += 1
                    c = self.next_char
                    if (c == 't'):
                        return '< ARITHOP, "mult" >'
                    else:
                        return "mul error"
                else:
                    return "mu error"
            else:
                return "m error"
        elif (c == 'a'):    # add (ARITHOP)
            print("possible add")
            if (c == 'd'):
                i += 1
                c = self.next_char
                if (c == 'd'):
                    return '< ARITHOP, "add" >'
                else:
                    return "ad error"
            else:
                return "a error"
        elif (c == 'n'):    # nop (NOP)
            print("possible nop")
            i += 1
            c = self.next_char
            if (c == 'o'):
                i += 1
                c = self.next_char
                if (c == 'p'):
                    return '< NOP, "nop" >'
                else:
                    return "no error (as in nop error)"
            else:
                return "n error"
        elif (c == 'o'):    # output (OUTPUT)
            print("possible output")
            i += 1
            c = self.next_char
            if (c == 'u'):
                i += 1
                c = self.next_char
                if (c == 't'):
                    i += 1
                    c = self.next_char
                    if (c == 'p'):
                        i += 1
                        c = self.next_char
                        if (c == 'u'):
                            i += 1
                            c = self.next_char
                            if (c == 't'):
                                return '< OUTPUT, "output" >'
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
        elif (c == '='):    # => (INTO)
            print("possible =>")
            i += 1
            c = self.next_char
            if (c == '>'):
                return '< INTO, "=>" >'
            else:
                return "= error"
        elif (c == '/'):    # COMMENT
            print("possible comment")
            # next char
            i += 1
            c = self.next_char

            if (c == '/'):
                # next char
                i += 1
                c = self.next_char
                print("in comment if, c is: " + str(c))

                # read rest of comment
                while (i < len(string) and c != '\n' and c != '\r\n'):
                    print(c)
                    # get next character
                    i += 1
                    c = self.next_char
                # print(c)
                if (c == '\n' or c == '\r\n'):
                    return '< NEWLINE, "\n" >'
            else:
                print("returning not a comment")
                return "NOT A COMMENT"
        elif (c == ','):    # COMMA
            print("possible comma")
            return '< COMMA, "," >'
        elif (c == '\n' and c == '\r\n'):   # EOL
            print("possible end of line")
            return '< NEWLINE, "\n" >'
        elif (c >= 0 and c <= 9):   #CONSTANT
            print("possible constant")
            constant = str(c)
            i += 1
            c = self.next_char
            while (c >= 0 and c <= 9):  # get to end of number
                constant = constant + str(c)
                c = self.next_char  # TODO: this may cause adding a char we dont want
            return '< CONST, "' + constant + " >"
        elif (c == ''):
            return '< ENDFILE, "" >'
        else:
            print("ERROR - idk what that is!")
            return "error!"
    
    def rollback(self):
        if (self.point == self.fence):
            raise RuntimeError("Rollback error!")
        self.point = (self.point - 1) % (2 * self.BUF_SIZE)


    # TODO: ask harry about this, piazza said it should be two chars but shouldnt i be checking for it running out of space in buffer? ik i am reading a line into the buffer, but am i clearing it all after each line??
    def next_char(self):
        """Gets the character at the specified index from the buffer.

        Args:
            buffer: The buffer.
            point: The point index.
            n: The size of the buffer.

        Returns:
            The character at the specified input index.
        """

        # print("buffer: " + str(self.buffer) + "\n" + "point: " + str(self.point) + "\n fence: " + str(self.fence) + "\n  + buf size: " + str(self.BUF_SIZE) + "\n char at point: " + str(self.buffer[self.point]))
        char = self.buffer[self.point]
        # moves pointer up
        self.point = (self.point + 1) % (2 * self.BUF_SIZE)

        if (self.point % self.BUF_SIZE == 0):
            for i in range(self.point, self.point + self.BUF_SIZE):
                self.buffer[i] = 0
            self.fence = (self.point + self.BUF_SIZE) % (2 * self.BUF_SIZE)

        return char
    

    
    # returns when it finds a token, return token
    def get_token(self):
        """ Get a line. Returns when it finds a word.
        Returns token < ENDFILE, "" >
        """
        # c = get_next_char(self)
        # print("in start_scan, about to call get_next_char")

        # c = self.next_char()
        # print("in start_scan, get_next_char result: " + str(c) + "\n going to while loop now")


        # i = 0
        # while (i < BUF_SIZE):
        #     print(self.main_scanner(c[i]))
        #     i += 1
        

        # print("in start_scan, after while")

        # # get next character
        # char = self.buffer[self.point]
        # # moves pointer up
        # self.point = (self.point + 1) % (2 * self.BUF_SIZE)

        # if (self.point % self.BUF_SIZE == 0):
        #     for i in range(self.point, self.point + self.BUF_SIZE):
        #         self.buffer[i] = 0
        #     self.fence = (self.point + self.BUF_SIZE) % (2 * self.BUF_SIZE)

        

        # in while loop, have it start on the current line num (?)
        # myline = self.input_file.readline() #returns empty string when at end of file
        # # read line by line into buffer
        # while myline:
        #     print(str(self.line_num) + ': < line, "' + myline + '" >')
        #     myline = self.input_file.readline()

        #     # TODO: add characters to buffer: check size, refill if full, add otherwise
        #     self.line_num+=1

        #this is like the shit in main_scanner
        # ret_token = '< ENDFILE, "" >'   # this is so we dont get infinite loop cuz scan_func expects this EOF token
        # line_num += 1
        c = self.next_char()
        return self.main_scanner(c)