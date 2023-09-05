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

def direct_code_scanner(string):
    print("scanner.py: " + string)

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
