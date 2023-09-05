#!/usr/bin/python -u

import scanner
# def main():
#   print("Hello!")

# Step 1) start off drawing out the big DFA
# Step 2) scanner is basically just a bunch of if else if statements with try catch blocks
# Step 3) pass the scanner simple strings

# def scanner(string):
#     print("string" + string)

COMMENT = "// ILOC Front End \n"
def main():
    print("in lab1.py")
    # scanner("i need to work faster")
    print(scanner.direct_code_scanner(COMMENT))
    scanner.print_characters_until_eol("i love bela nelson!")

    print(scanner.comment(COMMENT))

# def my_function():
#   print("Hello from a function")

# my_function()


# def my_function():
#   print("Hello, world!")

# def main():
#     print("in lab1.py")
#     my_function()
#     # scanner("i need to work faster")



if __name__ == "__main__":
  main()
