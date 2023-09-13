#!/usr/bin/python -u

import scanner
import rose_parser
import sys

COMMENT = "// ILOC Front End \n"

EOF_FLAG = False




def demand_parse_start(input_file, flag):
  # print("PUSSY")
  scan = scanner.Scanner(input_file)
  parse = rose_parser.RoseParser(scan)

  scan.mode_flag = flag
  # global linenum = 0
  # global line_idx = 0
  scan.cur_line = scan.convert_line_to_ascii_list(input_file.readline())
  scan.char_idx = -1

  # print(scan.cur_line)

  i = 0
  



  token = scan.get_token()
  # print(token)

  if (flag == '-s'):
    
    while (token[0] != scan.EOF):
      while (token[0] != scan.EOL and token[0] != scan.SCANNER_ERROR):
        i += 1
        token = scan.get_token()
        # print(str(scan.line_num) + ": bitch")
        # if (token[0] >= 0 and token[0] <= 10):
        #   # print(str(token))
        #   print(str(scan.line_num) + ": < " + str(scan.CATEGORIES[token[0]]) + ', "' + str(token[1]) + '" >')
      # if (token[0] == scan.EOL):
      #     print("its eol")
      #     print(str(scan.line_num) + ": < " + str(scan.CATEGORIES[token[0]]) + ', "' + str(token[1]) + '" >')
      # print("out")
      scan.cur_line = scan.convert_line_to_ascii_list(input_file.readline())
      token = scan.get_token()  
  else:

    while (token[0] != scan.EOF):
      i += 1
      if (token[0] == scan.MEMOP):
        if (parse.finish_memop(scan) == False):
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": MEMOP")
            
        scan.char_idx = -1
      elif (token[0] == scan.LOADI):
        if (parse.finish_loadI(scan) == False):
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": LOADI")
        scan.char_idx = -1
      elif (token[0] == scan.ARITHOP):
        if (parse.finish_arithop(scan) == False):
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": ARITHOP")
        scan.char_idx = -1
      elif (token[0] == scan.OUTPUT):
        if (parse.finish_output(scan) == False):
          print("cunt")
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": OUTPUT")
        scan.char_idx = -1
      elif (token[0] == scan.NOP):
        if (parse.finish_nop(scan) == False):
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": NOP")
        scan.char_idx = -1
      elif (token[0] == scan.EOL):
        # print("EOL BITCH")
        # print("[PARSE] " + str(scan.line_num) + ": EOL")
        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())

        # print(str(scan.cur_line))
        # scan.line_num += 1
        # scan.char_idx = -1
      elif (token[0] == scan.BLANK):
        token = scan.get_token()
        continue
      elif (token[0] == scan.SCANNER_ERROR):  # dont continue to parse if scanner error
        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
      else:
        sys.stderr.write("ERROR " + str(scan.line_num - 1) + ": no OPCODE - [PARSER]\n")
        # scan.line_num += 1
        # scan.char_idx = -1
        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
      token = scan.get_token()
    
    # print(str(len(parse.OPS)) + " valid ILOC operations: " + str(parse.OPS))
    if (parse.num_parser_errors == 0):
      print("Parse succeeded, finding " + str(parse.num_iloc_ops) + " ILOC operations.")
    # print(str(parse.num_iloc_ops) + " valid ILOC operations")
    print(str(parse.num_parser_errors) + " parser errors.")
  print(str(scan.num_scanner_errors) + " scanner errors.")
  if (parse.num_parser_errors == 0):
    print("SUCCESS")
    



    
  

    
      
  


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
      demand_parse_start(f, '-r')
      f.close()
  elif (sys.argv[1] == '-p'):
    # print("TODO: read the file, scan it and parse it, build the intermediate representation (IR) and report either success or report all the errors that it finds in the input file.")
    if (len(sys.argv) <= 2):
      print("Must specify a file name after the flag.")
    else:
      __file__ = sys.argv[2]
      # Reading a file
      f = open(__file__, 'r')
      # start(f, '-p')
      demand_parse_start(f, '-p')
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
      demand_parse_start(f, '-s')
      # while (token != ["ENDFILE", ""]): # NOTE: should i read the line by line here?
      #   scan_func(f)
      #   poo += 1
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