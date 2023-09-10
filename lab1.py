#!/usr/bin/python -u

import scanner
import rose_parser
import sys

COMMENT = "// ILOC Front End \n"

EOF_FLAG = False



def start(input_file, flag):
  scan = scanner.Scanner(input_file)
  parse = rose_parser.RoseParser(scan)
  # print("in scan_func in lab1.py, starting start_scan in scanner.py")
  # token = scan.get_token()
  # print(str(scanner.line_num) + ": " + token)

  # tokens should be a string like < cat, "lex" >
  pre = "< "
  mid = ', "'
  post = '" >'
  EOF_TOKEN = [scan.EOF, ""]
  

  
  

  # while not at end of line (char idx < length of line)
  #   get token

  # first line to start it
  # scan.cur_line = scan.input_file.readline()
  # get first token
  # token = scan.get_token()
  # While not the end of file token; EOF = empty string

  # THIS IS ACTUALLY THE PARSER
  # while (token != EOF_TOKEN):
    # call start_scan, which returns token
    # scan.cur_line = input_file.readline() # returns empty string when at end of line
    # read line by line into buffer
  scan.cur_line = scan.input_file.readline()
  token = ["", ""]
  shit = 0
  i = 0
  j = 0
  while (scan.cur_line != ""):
    # print("[scan_func] token[0]: " + str(token[0]))
    # print("[scan_func, outer while] char idx: " + str(scan.char_idx))

    i += 1
    while (token[0] != scan.EOL and scan.cur_line != "" and token[0] != 'ERROR'):
      j += 1
      # print(str(scan.line_num) + ': ' + scan.cur_line)

      # SCAN (GET A TOKEN)
      # print("🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸SCAN-START🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸")
      token = scan.get_token()
      # print("🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸SCAN-END🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸")

      if (token[0] != scan.BLANK):  # ignore whitespace
        scan.token_list.append(token) # need white space to check operations in parser
      # if error, go to next line
      if (token[0] == "SCANNER_ERROR"):
        new_line = [scan.EOL, "\n"]
        scan.token_list.append(new_line)
        token = new_line  # should make the while look break and then go to next line

      if (token[0] != "SCANNER_ERROR" and token[0] >= 0 and token[0] <= 10):  # only print opcodes
        print(str(scan.line_num) + ': < ' + str(scan.CATEGORIES[token[0]]) + ', "' + str(token[1]) + '" >')
    
    # print("after while------------------------")
    
    # print(scan.token_list)

    
    scan.file_token_lists.append(scan.token_list) # add token list to line list


    # ------------------PARSE-----------------
    
    # print("🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲PARSE-START🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲")
    
    if (flag == '-p' or flag == 'r'):
      parse.parse_line(scan.token_list, scan.line_num)
    # print("🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲PARSE-END🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲🐲")




    # RESET
    scan.char_idx = -1
    token = ["", ""]
    scan.token_list = []  # new line, new list


    # INCREMENT
    scan.cur_line = scan.input_file.readline()
    scan.line_num+=1
    shit += 1
    # print("new line: " + scan.cur_line)
    # print("shit toje: " + str(token))
  
  print(str(scan.line_num) + ': < ' + str(scan.CATEGORIES[EOF_TOKEN[0]]) + ', "' + str(EOF_TOKEN[1]) + '" >')
  
  scan.file_token_lists.append(EOF_TOKEN)
  
  # print("i: "  + str(i))
  # print("j: "  + str(i))

  # print("token list len: " +  str(len(scan.token_list)))
  # print("token list len: " +  str(len(scan.file_token_lists)))

  boob = 0
  num_tokens = 0
  # for i in scan.file_token_lists:
  #   temp = len(scan.file_token_lists[boob])
  #   num_tokens += len(scan.file_token_lists[boob])
    
  #   # print(scan)
  #   print(scan.file_token_lists[boob])
  #   # print(str(boob) + ": " + str(temp))
  #   boob += 1

  # print("total num tokens: " + str(num_tokens))
  


  
  #   print("eof token: " + EOF_TOKEN)
  #   # print token
  #   print(str(scan.line_num) + ": " + str(token))
  #   # break
  #   # dont need to remove from buffer here bc buffer leaves chars until clearing necessary (full)
  # EOF_FLAG = True;
  # for i in scan.file_token_lists:
  #   print(str(i))
  # print(scan.file_token_lists)
  return EOF_TOKEN


def demand_parse_start(input_file):
  scan = scanner.Scanner(input_file)
  parse = rose_parser.RoseParser(scan)
  # global linenum = 0
  # global line_idx = 0
  scan.cur_line = scan.convert_line_to_ascii_list(input_file.readline())
  print(scan.cur_line)
  # token = scan.get_token()
  # while (token != [scan.EOF, ""]):
  #   if (token[0] == scan.MEMOP):
  #     finish_memop(scan)
  #     break
  #   elif (token[0] == scan.LOADI):
  #     break
  #   elif (token[0] == scan.ARITHOP):
  #     break
  #   elif (token[0] == scan.OUTPUT):
  #     break
  #   elif (token[0] == scan.NOP):
  #     break
  #   else:
  #     sys.stderr.write("ERROR: no OPCODE\n")
  #     break
  

  def finish_memop(scan):
    token = scan.get_token()
    
      
  


def main():
  # call scan function  
  #   make scanner object by calling class with input fileand then my start scanning func in scanner.py
  #   while not the end of the license
  #     the if statements




  #read()
  # text = f.read(10)
  i = 1

  if (sys.argv[1] == '-h'):
    print("\n")
    print("Command Syntax:")
    print("     ./412fe [flags] filename")
    print("\n")
    print("Required arguments:")
    print("     filename is the pathname (absolute or relative) to the input file. When the flag is '-h', no filename should be specified and nothing after the flag is processed.")
    print("\n")
    print("Optional flags:")
    print("     -h      prints this message")
    print("\n")
    print("At most one of the following three flags:")
    print("     -s      prints tokens in token stream, only invokes scanner")
    print("     -p      invokes parser and resports on success or failure, invokes scanner and parser")
    print("     -r      prints the human readable version of parser's IR")
    print("If none is specified, the default action is '-p'.")
    
  elif (sys.argv[1] == '-r'):
    # print("TODO: read the file, parse it, build the intermediate representation (IR), and print out the information in the intermediate representaiton (in an appropriately human readable format)")
    if (len(sys.argv) <= 2):
      print("Must specify a file name after the flag.")
    else:
      __file__ = sys.argv[2]
      # Reading a file
      f = open(__file__, 'r')
      start(f, '-r')
      f.close()
  elif (sys.argv[1] == '-p'):
    # print("TODO: read the file, scan it and parse it, build the intermediate representation (IR) and report either success or report all the errors that it finds in the input file.")
    if (len(sys.argv) <= 2):
      print("Must specify a file name after the flag.")
    else:
      __file__ = sys.argv[2]
      # Reading a file
      f = open(__file__, 'r')
      start(f, '-p')
      f.close()
  elif (sys.argv[1] == '-s'):
    # print("TODO: read file and print to stdout a list of tokens that the scanner found. for each, print line number, tokens type (or syntactic category) and its spelling (or lexeme)")
    if (len(sys.argv) <= 2):
      print("Must specify a file name after the flag.")
    else:
      __file__ = sys.argv[2]
      # Reading a file
      poo = 0
      f = open(__file__, 'r')
      start(f, '-s')
      # while (token != ["ENDFILE", ""]): # NOTE: should i read the line by line here?
      #   scan_func(f)
      #   poo += 1
      print("closing.- " + str(poo))
      f.close()
  elif (sys.argv[1] == '-z'): # flag for me testing changing my impl
    if (len(sys.argv) <= 2):
      print("Must specify a file name after the flag.")
    else:
      __file__ = sys.argv[2]
      # Reading a file
      poo = 0
      f = open(__file__, 'r')
      demand_parse_start(f)
      # while (token != ["ENDFILE", ""]): # NOTE: should i read the line by line here?
      #   scan_func(f)
      #   poo += 1
      print("closing.- " + str(poo))
      f.close()





  # input_file = sys.argv[1]

  # myline = f.readline() #returns empty string when at end of file
  # while myline:
  #   print(str(i) + ": " + myline)
  #   print(scanner.main_scanner(myline))
  #   i = 0
  #   while (i < len(myline)):
  #     add_char_to_buf(myline[i])

  #   myline = f.readline()
  #   i+=1

  # print(str(Buffer)[1:-1])




if __name__ == "__main__":
  main()