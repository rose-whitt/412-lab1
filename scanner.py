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


class Scanner:

    def __init__(self, file_name):
        self.BUF_SIZE = 0

        init all variables like buffer and shit


MEMOP = 0   # load, store
LOADI = 1   # loadI
ARITHOP = 2 # add, sub, mult, lshift, rshift
OUTPUT = 3  # output
NOP = 4     # nop
CONSTANT = 5    # a non-negative integer
REGISTER = 6    # 'r' followed by a constant
COMMA = 7   # ','
INTO = 8    # "=>"
EOF = 9     # input has been exhausted
EOL = 10    # end of current line ("\r\n" or "\n")


def main_scanner(string):
    i = 0
    c = string[i]
    # store (MEMOP) or sub (ARITHOP)
    if (c == 's'):
        # next char
        i += 1
        c = string[i]
        if (c == 't'):    # store (MEMOP)
            # next char
            i += 1
            c = string[i]
            if (c == 'o'):
                # next char
                i += 1
                c = string[i]
                if (c == 'r'):
                    # next char
                    i += 1
                    c = string[i]
                    if (c == 'e'):
                        return "store - MEMOP"
                    else:
                        return "stor ERROR"
                else:
                    return "sto ERROR"
            else:
                return "st ERROR"
        elif (c == 'u'):    # sub (ARITHOP)
            # next char
            i += 1
            c = string[i]
            if (c == 'b'):
                return "sub - ARITHOP"
            else:
                return "su ERROR"
        else:
            return "s ERROR"
    elif (c == 'l'):
        # next char
        i += 1
        c = string[i]
        if (c == 'o'):
            # next char
            i += 1
            c = string[i]
            if (c == 'a'):
                # next char
                i += 1
                c = string[i]
                if (c == 'd'):
                    # next char
                    i += 1
                    c = string[i]
                    if (c == 'I'): # loadI (LOADI)
                        return "loadI - LOADI"
                    elif (c == '\n' or c == '\r\n' or c == ' '):    # load (MEMOP)
                        return "load - MEMOP"
                    else:
                        return "load ERROR"  #NOTE- now that i think about it, they should all check tehre is a new line or sum to show end of word

                else:
                    return "loa ERROR"
            else:
                return "lo ERROR"
        else:
            return "l ERROR"
    elif (c == 'r'):    # rshift (ARITHOP) or register
        # next char
        i += 1
        c = string[i]
        if (c >= '0' and c <= '9'):
            print("possible register")
            return
        elif (c == 's'):
            print("possible rshift")
            return
        else:
            print("r ERROR")
            return
    elif (c == 'm'):    # mult (ARITHOP)
        print("possible mult")
        return
    elif (c == 'a'):    # add (ARITHOP)
        print("possible add")
        return
    elif (c == 'n'):    # nop (NOP)
        print("possible nop")
        return
    elif (c == 'o'):    # output (OUTPUT)
        print("possible output")
        return
    elif (c == '='):    # => (INTO)
        print("possible =>")
        return
    elif (c == '/'):    # COMMENT
        print("possible comment")
        # next char
        i += 1
        c = string[i]

        if (c == '/'):
            # next char
            i += 1
            c = string[i]

            # read rest of comment
            while (i < len(string) and c != '\n' and c != '\r\n'):
                print(c)
                # get next character
                i += 1
                c = string[i]
            # print(c)
            if (c == '\n' or c == '\r\n'):
                return "COMMENT"
        else:
            return "NOT A COMMENT"
    elif (c == ','):    # COMMA
        print("possible comma")
        return
    elif (c == '\n' and c == '\r\n'):   # EOL
        print("possible end of line")
        return
    elif (c >= '0' and c <= '9'):   #CONSTANT
        print("possible constant")
        return
    else:
        print("ERROR")
        return


        




def print_characters_until_eol(string):
  index = 0
  while index < len(string) and string[index] != '\n':
    print(string[index])
    index += 1

def direct_code_scanner(string):
    print("scanner.py: " + string)

    shit(string)

    index = 0
    c = string[index]
    # comments
    if (c == '/'):
        print(str(index) + ", " + c)

        index += 1
        c = string[index]
        if (c == '/'):
            while (index < len(string) and c != '\n' and c != '\r\n'):
                c = string[index]
                print(str(index) + ", " + c)
                index += 1
            if (c == '\n' and c == '\r\n'):
                return "COMMENT"
            else:
                return "ERROR"


def comment(string):
    i = 0
    c = string[i]
    if (c == '/'):
        # next char
        i += 1
        c = string[i]

        if (c == '/'):
            # next char
            i += 1
            c = string[i]

            # read rest of comment
            while (i < len(string) and c != '\n' and c != '\r\n'):
                print(c)
                # get next character
                i += 1
                c = string[i]
            # print(c)
            if (c == '\n' or c == '\r\n'):
                return "COMMENT"
        else:
            return "NOT A COMMENT"
    else:
        return "NOT A COMMENT"


def shit(string):
    print("in shit")
    i = 0
    c = string[i]
    while (i < len(string) and c != '\n' and c != '\r\n'):
        print(c)
        # get next character
        i += 1
        c = string[i]