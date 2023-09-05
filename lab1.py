#!/usr/bin/python -u

import scanner
import sys

# INITIALIZE DOUBLE BUFFER
BUF_SIZE = 2048
input = 0
Fence = 0

# Create a buffer of size n
Buffer = [0] *  BUF_SIZE

# Fill the buffer with zeros


COMMENT = "// ILOC Front End \n"

def main():
  reset_buffer()

  # call scan function  
  #   make scanner object by calling class and then my start scanning func in scanner.py
  #   while not the end of the license
  #     the if statements
  # command_line_args()

  tempArgs = sys.argv # lab1.py will always be first
  __file__ = tempArgs[1]
  # Reading a file
  f = open(__file__, 'r')
    
  #read()
  # text = f.read(10)
  i = 1

  myline = f.readline() #returns empty string when at end of file
  while myline:
    print(str(i) + ": " + myline)
    print(scanner.main_scanner(myline))
    i = 0
    while (i < len(myline)):
      add_char_to_buf(myline[i])

    myline = f.readline()
    i+=1
    
  print(str(Buffer)[1:-1])

  f.close()


  # print(scanner.main_scanner("store"))
  # print(scanner.main_scanner("sub"))
  # # print(scanner.main_scanner("su")) # currently index out of range
  # print(scanner.main_scanner("add"))
  # print(scanner.main_scanner("adfhkljsdf"))
  # print(scanner.main_scanner("out"))




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

def add_char_to_buf(c):
  Buffer[input] = c
  input = (input + 1) % (2 * BUF_SIZE)

def rollback():
  if (input == Fence):
    raise RuntimeError("Rollback error!")
  input = (input - 1) % (2 * BUF_SIZE)

def get_next_char():
  """Gets the character at the specified input index.

  Args:
    buffer: The buffer.
    input: The input index.
    n: The size of the buffer.

  Returns:
    The character at the specified input index.
  """

  char = Buffer[input]
  input = (input + 1) % (2 * BUF_SIZE)

  if input % BUF_SIZE == 0:
    reset_buffer()
    Fence = (input + BUF_SIZE) % (2 * BUF_SIZE)

  return char

def reset_buffer():
  """Fills the buffer with zeros.

  Args:
    buffer: The buffer.
    input: The starting index of the buffer to fill.
    n: The size of the buffer.
  """
  print("reset buf")
  for i in range(input, input + BUF_SIZE):
    Buffer[i] = 0




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
