#!/usr/bin/python -u

import scanner
import sys
# def main():
#   print("Hello!")

# Step 1) start off drawing out the big DFA
# Step 2) scanner is basically just a bunch of if else if statements with try catch blocks
# Step 3) pass the scanner simple strings

# def scanner(string):
#     print("string" + string)

COMMENT = "// ILOC Front End \n"
def main():

  command_line_args()

  print(scanner.main_scanner("store"))
  print(scanner.main_scanner("sub"))
  # print(scanner.main_scanner("su")) # currently index out of range
  print(scanner.main_scanner("add"))
  print(scanner.main_scanner("adfhkljsdf"))
  print(scanner.main_scanner("out"))




  # print("arguments: ")
  # print(sys.argv)

  # print("---")

  # print("in lab1.py")
  # print("---")

  # # scanner("i need to work faster")
  # print(scanner.direct_code_scanner(COMMENT))
  # print("---")
  # scanner.print_characters_until_eol("i love bela nelson!")

  # print("---")


  # print(scanner.comment(COMMENT))


def command_line_args():
  args = sys.argv # lab1.py will always be first
  print(args)
  for i in range(len(args)):
    print(args[i])
  
  if (len(args) >= 2):
    if (args[1] == '-h'):
      print("-h flag indicated. this will produce valid command line args")
    elif (args[1] == '-r'):
      if (len(args) >= 3):
        print("-r flag indicated with name" + args[2] +"  this will read file and report ucceses")
      else:
        print("-r error, no name speciifed")
    elif (args[1] == '-p'):
      if (len(args) >= 3):
        print("-p flag indicated with name" + args[2] +"  this will read file and print IR")
      else:
        print("-p error, no name speciifed")
    elif (args[1] == '-s'):
      if (len(args) >= 3):
        print("-s flag indicated with name" + args[2] + "  this will read file and print tokens")
      else:
        print("-s error, no name speciifed")

if __name__ == "__main__":
  main()
