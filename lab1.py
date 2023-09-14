#!/usr/bin/python -u

import scanner
# import rose_parser
import sys
import cProfile, pstats
from io import StringIO

COMMENT = "// ILOC Front End \n"

EOF_FLAG = False




def demand_parse_start(input_file, flag):
  # print("PUSSY")
  scan = scanner.Scanner(input_file)
  # parse = rose_parser.RoseParser(scan)

  scan.mode_flag = flag
  # global linenum = 0
  # global line_idx = 0
  scan.cur_line = scan.convert_line_to_ascii_list(input_file.readline())
  scan.char_idx = -1

  # print(scan.cur_line)

  i = 0
  



  token = scan.get_token()
  # print("type of token: " + str(type(token)))
  # print(token)

  if (flag == '-s'):
    
    while (token[0] != scan.EOF):
      while (token[0] != scan.EOL and token[0] != scan.SCANNER_ERROR):
        i += 1
        token = scan.get_token()
      scan.cur_line = scan.convert_line_to_ascii_list(input_file.readline())
      token = scan.get_token()  
  else:

    while (token[0] != scan.EOF):
      i += 1
      if (token[0] == scan.MEMOP):
        MEM_OP_FLAG = False
        token = scan.get_token()
        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.REGISTER):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing first REGISTER in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            MEM_OP_FLAG = False
        else:
            token = scan.get_token()
            while (token[0] == scan.BLANK):
                token = scan.get_token()
            if (token[0] != scan.INTO):
                sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing INTO in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
                scan.num_parser_errors += 1
                MEM_OP_FLAG = False
            token = scan.get_token()
            while (token[0] == scan.BLANK):
                token = scan.get_token()
            if (token[0] != scan.REGISTER):
                sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing target (second) REGISTER in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
                scan.num_parser_errors += 1
                MEM_OP_FLAG = False
            else:
                token = scan.get_token()
                while (token[0] == scan.BLANK):
                    token = scan.get_token()
                if (token[0] == scan.EOL):
                    # print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                    # TODO: build IR for this OP, add IR to list of OPS
                    scan.num_iloc_ops += 1
                    # scan.line_num += 1
                    # scan.char_idx = -1
                    scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
                    MEM_OP_FLAG = True
                elif (token[0] == scan.SCANNER_ERROR):
                    return False
                else:
                    sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing EOL in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
                    scan.num_parser_errors += 1
                    MEM_OP_FLAG =  False

        if (MEM_OP_FLAG == False):
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": MEMOP")
            
        scan.char_idx = -1
      elif (token[0] == scan.LOADI):
        LOADI_FLAG = False
        token = scan.get_token()
        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.CONSTANT):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing CONSTANT in LOADI; token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            LOADI_FLAG = False
        else:
            token = scan.get_token()
            while (token[0] == scan.BLANK):
                token = scan.get_token()
            if (token[0] != scan.INTO):
                sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing INTO in LOADI; token: ' + str(token[0]) +  ' - [PARSER]\n')
                scan.num_parser_errors += 1
                LOADI_FLAG = False
            else:
                token = scan.get_token()
                while (token[0] == scan.BLANK):
                    token = scan.get_token()
                if (token[0] != scan.REGISTER):
                    sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing REGISTER in LOADI; token: ' + str(token[0]) +  ' - [PARSER]\n')
                    scan.num_parser_errors += 1
                    LOADI_FLAG = False
                else:
                  token = scan.get_token()
                  while (token[0] == scan.BLANK):
                      token = scan.get_token()
                  if (token[0] == scan.EOL):
                      scan.num_iloc_ops += 1
                      # scan.line_num += 1
                      # scan.char_idx = -1
                      scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
                      LOADI_FLAG = True
                  elif (token[0] == scan.SCANNER_ERROR):
                      LOADI_FLAG = True
                  else:
                      sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing EOL in LOADI; token: ' + str(token[0]) +  ' - [PARSER]\n')
                      scan.num_parser_errors += 1
                      LOADI_FLAG = False
        if (LOADI_FLAG == False):
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": LOADI")
        scan.char_idx = -1
      elif (token[0] == scan.ARITHOP):
        ARITHOP_FLAG = False
        token = scan.get_token() 

        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.REGISTER):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing first REGISTER in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            ARITHOP_FLAG = False
        else:
            token = scan.get_token()
            while (token[0] == scan.BLANK):
                token = scan.get_token()
            if (token[0] != scan.COMMA):
              sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing COMMA in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
              scan.num_parser_errors += 1
              ARITHOP_FLAG = False
            else:
              token = scan.get_token()
              while (token[0] == scan.BLANK):
                  token = scan.get_token()
              # ARITHOP REG COMMA 
              if (token[0] != scan.REGISTER):
                  sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing second REGISTER in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
                  scan.num_parser_errors += 1
                  ARITHOP_FLAG = False
              else:
                token = scan.get_token()
                while (token[0] == scan.BLANK):
                    token = scan.get_token()
                if (token[0] != scan.INTO):
                    sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing INTO in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
                    scan.num_parser_errors += 1
                    ARITHOP_FLAG = False
                else:
                  token = scan.get_token()
                  while (token[0] == scan.BLANK):
                      token = scan.get_token()
                  if (token[0] != scan.REGISTER):
                      sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing target (third) REGISTER in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
                      scan.num_parser_errors += 1
                      ARITHOP_FLAG = False
                  else:
                    token = scan.get_token()
                    while (token[0] == scan.BLANK):
                        token = scan.get_token()
                    if (token[0] == scan.EOL):
                        scan.num_iloc_ops += 1
                        # scan.line_num += 1
                        # scan.char_idx = -1
                        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
                        ARITHOP_FLAG = True
                    elif (token[0] == scan.SCANNER_ERROR):
                        ARITHOP_FLAG = False
                    else:
                        sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing EOL in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
                        scan.num_parser_errors += 1
                        ARITHOP_FLAG = False
       
        if (ARITHOP_FLAG == False):
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": ARITHOP")
        scan.char_idx = -1
      elif (token[0] == scan.OUTPUT):
        OUTPUT_FLAG = False
        token = scan.get_token()
        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.CONSTANT):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing CONSTANT in OUTPUT; token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            OUTPUT_FLAG = False
        else:
          token = scan.get_token()
          while (token[0] == scan.BLANK):
              token = scan.get_token()
          if (token[0] == scan.EOL):
              scan.num_iloc_ops += 1
              # scan.line_num += 1
              # scan.char_idx = -1
              scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
              OUTPUT_FLAG = True
          elif (token[0] == scan.SCANNER_ERROR):
              OUTPUT_FLAG = False
          else:   # NOTE: i think that i should add a case to see if its a scanner error so then i woudlnt print it out, and if its soemthing else, then print out the char
              sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing EOL in OUTPUT; token: ' + str(token[0]) +  ' - [PARSER]\n')
              scan.num_parser_errors += 1
              OUTPUT_FLAG = False
        if (OUTPUT_FLAG == False):
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        scan.char_idx = -1
      elif (token[0] == scan.NOP):
        NOP_FLAG = False
        token = scan.get_token()
        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] == scan.SCANNER_ERROR):
            NOP_FLAG = False
        elif (token[0] != scan.EOL and token[0] != scan.EOF):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               wrong thing after NOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            NOP_FLAG = False
        else:
            scan.num_iloc_ops += 1
            # scan.line_num += 1
            # scan.char_idx = -1
            scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
            NOP_FLAG = True
        if (NOP_FLAG == False):
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        scan.char_idx = -1
      elif (token[0] == scan.EOL):
        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
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
    
    # print(str(len(scan.OPS)) + " valid ILOC operations: " + str(scan.OPS))
    if ((scan.num_parser_errors + scan.num_scanner_errors) == 0):
      print("Parse succeeded, finding " + str(scan.num_iloc_ops) + " ILOC operations.")
    else:
      sys.stderr.write("Found " + str(scan.num_parser_errors + scan.num_scanner_errors) + " errors on x lines\n")
    # print(str(scan.num_iloc_ops) + " valid ILOC operations")
  #   print(str(scan.num_parser_errors) + " parser errors.")
  # print(str(scan.num_scanner_errors) + " scanner errors.")
  
    



    
  

    
      
  


def main():
  pr = cProfile.Profile()
  pr.enable()
  # call scan function  
  #   make scanner object by calling class with input fileand then my start scanning func in scanner.py
  #   while not the end of the license
  #     the if statements




  #read()
  # text = f.read(10)
  i = 1
  # print("POO POOO POO")

  arg_len = len(sys.argv)

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
    if (arg_len <= 2):
      print("Must specify a file name after the flag.")
    else:
      __file__ = sys.argv[2]

      # open file
      try:
          f = open(__file__, 'r')
      except FileNotFoundError:  # FileNotFoundError in Python 3
          print(f"ERROR input file not found", file=sys.stderr)
          sys.exit()
      # Reading a file
      # f = open(__file__, 'r')
      demand_parse_start(f, '-r')
      f.close()
  elif (sys.argv[1] == '-p'):
    # print("TODO: read the file, scan it and parse it, build the intermediate representation (IR) and report either success or report all the errors that it finds in the input file.")
    if (arg_len <= 2):
      print("Must specify a file name after the flag.")
    else:
      __file__ = sys.argv[2]

      # open file
      try:
          f = open(__file__, 'r')
      except FileNotFoundError:  # FileNotFoundError in Python 3
          print(f"ERROR input file not found", file=sys.stderr)
          sys.exit()

      # __file__ = sys.argv[2]
      # Reading a file
      # f = open(__file__, 'r')
      # start(f, '-p')
      demand_parse_start(f, '-p')
      f.close()
  elif (sys.argv[1] == '-s'):
    # print("TODO: read file and print to stdout a list of tokens that the scanner found. for each, print line number, tokens type (or syntactic category) and its spelling (or lexeme)")
    if (arg_len <= 2):
      print("Must specify a file name after the flag.")
    else:

      __file__ = sys.argv[2]

      # open file
      try:
          f = open(__file__, 'r')
      except FileNotFoundError:  # FileNotFoundError in Python 3
          print(f"ERROR input file not found", file=sys.stderr)
          sys.exit()
      # __file__ = sys.argv[2]
      # # Reading a file
      # poo = 0
      # f = open(__file__, 'r')
      demand_parse_start(f, '-s')
      # while (token != ["ENDFILE", ""]): # NOTE: should i read the line by line here?
      #   scan_func(f)
      #   poo += 1
      f.close()
  else: # p is default if no flag
    __file__ = sys.argv[1]  # no flag, so second arg should be a filename

    # open file
    try:
        f = open(__file__, 'r')
    except FileNotFoundError:  # FileNotFoundError in Python 3
        print(f"ERROR input file not found", file=sys.stderr)
        sys.exit()
    # __file__ = sys.argv[2]
    # Reading a file
    # f = open(__file__, 'r')
    # start(f, '-p')
    demand_parse_start(f, '-p')
    f.close()
  s = StringIO()
  sortby = 'cumulative'
  ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
  ps.print_stats()
  sys.stdout.write(s.getvalue())




if __name__ == "__main__":
  main()