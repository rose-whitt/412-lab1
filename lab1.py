#!/usr/bin/python -u

import scanner
from IR_List import *
import sys
# import cProfile, pstats
# from io import StringIO

COMMENT = "// ILOC Front End \n"

EOF_FLAG = False


ir_list = LinkedList()








def demand_parse_start(input_file, flag):
  

  scan = scanner.Scanner(input_file)

  scan.mode_flag = flag
  scan.cur_line = scan.convert_line_to_ascii_list(input_file.readline())
  scan.char_idx = -1

  i = 0

  token = scan.get_token()

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
        memop_node = Node()
        memop_node.line = scan.line_num
        memop_node.opcode = token[1]

        MEM_OP_FLAG = False
        token = scan.get_token()
        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.REGISTER):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing first REGISTER in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            MEM_OP_FLAG = False
        else:
            memop_node.arg1.sr = token[1]  # first register
            token = scan.get_token()
            while (token[0] == scan.BLANK):
                token = scan.get_token()
            if (token[0] != scan.INTO):
                sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing INTO in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
                scan.num_parser_errors += 1
                MEM_OP_FLAG = False
            else:
              token = scan.get_token()
              while (token[0] == scan.BLANK):
                  token = scan.get_token()
              if (token[0] != scan.REGISTER): # register in scanner returns self.REGISTER, reg_num
                  sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing target (second) REGISTER in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
                  scan.num_parser_errors += 1
                  MEM_OP_FLAG = False
              else:
                  memop_node.arg3.sr = token[1]  # second register
                  
                  token = scan.get_token()
                  while (token[0] == scan.BLANK):
                      token = scan.get_token()
                  if (token[0] == scan.EOL):
                      # build IR
                      ir_list.append(memop_node)

                      scan.num_iloc_ops += 1
                      scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
                      
                      
                      MEM_OP_FLAG = True
                  elif (token[0] == scan.SCANNER_ERROR):
                      return False
                  else:
                      sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing EOL in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
                      scan.num_parser_errors += 1
                      MEM_OP_FLAG =  False
        if (MEM_OP_FLAG == False):  # error on line
          scan.num_error_lines += 1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())

        scan.char_idx = -1
      elif (token[0] == scan.LOADI):
        loadi_node = Node()
        loadi_node.line = scan.line_num
        loadi_node.opcode = token[1]
        LOADI_FLAG = False
        token = scan.get_token()
        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.CONSTANT):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing CONSTANT in LOADI; token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            LOADI_FLAG = False
        else:
            loadi_node.arg1.sr = token[1]  # first constant
            
            # temp_line.append(token)
            token = scan.get_token()
            while (token[0] == scan.BLANK):
                token = scan.get_token()
            if (token[0] != scan.INTO):
                sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing INTO in LOADI; token: ' + str(token[0]) +  ' - [PARSER]\n')
                scan.num_parser_errors += 1
                LOADI_FLAG = False
            else:
                # temp_line.append(token)
                token = scan.get_token()
                while (token[0] == scan.BLANK):
                    token = scan.get_token()
                if (token[0] != scan.REGISTER):
                    sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing REGISTER in LOADI; token: ' + str(token[0]) +  ' - [PARSER]\n')
                    scan.num_parser_errors += 1
                    LOADI_FLAG = False
                else:
                  loadi_node.arg3.sr = token[1]  # second register

                  token = scan.get_token()
                  while (token[0] == scan.BLANK):
                      token = scan.get_token()
                  if (token[0] == scan.EOL):
                      # build ir
                      ir_list.append(loadi_node)


                      scan.num_iloc_ops += 1
                      scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
                      LOADI_FLAG = True
                  elif (token[0] == scan.SCANNER_ERROR):
                      LOADI_FLAG = True
                  else:
                      sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing EOL in LOADI; token: ' + str(token[0]) +  ' - [PARSER]\n')
                      scan.num_parser_errors += 1
                      LOADI_FLAG = False
        if (LOADI_FLAG == False): # error on line
          scan.num_error_lines += 1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        scan.char_idx = -1
      elif (token[0] == scan.ARITHOP):
        ari_node = Node()
        ari_node.line = scan.line_num
        ari_node.opcode = token[1]

        ARITHOP_FLAG = False
        token = scan.get_token() 

        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.REGISTER):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing first REGISTER in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            ARITHOP_FLAG = False
        else:
            ari_node.arg1.sr = token[1]
            
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
                ari_node.arg2.sr = token[1]

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
                    ari_node.arg3.sr = token[1]
                    
                    token = scan.get_token()
                    while (token[0] == scan.BLANK):
                        token = scan.get_token()
                    if (token[0] == scan.EOL):
                        ir_list.append(ari_node)

                        scan.num_iloc_ops += 1
                        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
                        ARITHOP_FLAG = True
                    elif (token[0] == scan.SCANNER_ERROR):
                        ARITHOP_FLAG = False
                    else:
                        sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing EOL in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
                        scan.num_parser_errors += 1
                        ARITHOP_FLAG = False
       
        if (ARITHOP_FLAG == False):  # error on line
          scan.num_error_lines += 1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        scan.char_idx = -1
      elif (token[0] == scan.OUTPUT):
        output_node = Node()
        output_node.line = scan.line_num
        output_node.opcode = token[1]

        OUTPUT_FLAG = False
        token = scan.get_token()
        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.CONSTANT):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing CONSTANT in OUTPUT; token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            OUTPUT_FLAG = False
        else:
          # temp_line.append(token)
          output_node.arg1.sr = token[1]

          token = scan.get_token()
          while (token[0] == scan.BLANK):
              token = scan.get_token()
          if (token[0] == scan.EOL):

              ir_list.append(output_node)

              scan.num_iloc_ops += 1

              scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
              OUTPUT_FLAG = True
          elif (token[0] == scan.SCANNER_ERROR):
              OUTPUT_FLAG = False
          else:   # NOTE: i think that i should add a case to see if its a scanner error so then i woudlnt print it out, and if its soemthing else, then print out the char
              sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing EOL in OUTPUT; token: ' + str(token[0]) +  ' - [PARSER]\n')
              scan.num_parser_errors += 1
              OUTPUT_FLAG = False
        if (OUTPUT_FLAG == False):  # error on line
          scan.num_error_lines += 1
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

            scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
            NOP_FLAG = True
        if (NOP_FLAG == False): # error on line
          scan.num_error_lines += 1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        scan.char_idx = -1
      elif (token[0] == scan.EOL):
        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
      elif (token[0] == scan.BLANK):
        token = scan.get_token()
        continue
      elif (token[0] == scan.SCANNER_ERROR):  # dont continue to parse if scanner error
        scan.num_error_lines += 1
        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
      else:
        sys.stderr.write("ERROR " + str(scan.line_num - 1) + ": no OPCODE - [PARSER]\n")

        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
      token = scan.get_token()
    
    if ((scan.num_parser_errors + scan.num_scanner_errors) == 0):
      print("Parse succeeded, finding " + str(scan.num_iloc_ops) + " ILOC operations.")
    else:
      sys.stderr.write("Found " + str(scan.num_parser_errors + scan.num_scanner_errors) + " errors on " + str(scan.num_error_lines) + " lines\n")

  
    



    
  

    
      
  


def main():
  # pr = cProfile.Profile()
  # pr.enable()
  
  i = 1

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


      demand_parse_start(f, '-r')
      ir_list.print_list()
      f.close()
  elif (sys.argv[1] == '-p'):
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
     
      demand_parse_start(f, '-s')

      f.close()
  else: # p is default if no flag
    __file__ = sys.argv[1]  # no flag, so second arg should be a filename

    # open file
    try:
        f = open(__file__, 'r')
    except FileNotFoundError:  # FileNotFoundError in Python 3
        print(f"ERROR input file not found", file=sys.stderr)
        sys.exit()

    demand_parse_start(f, '-p')
    f.close()

  # pr.disable()
  # s = StringIO()
  # sortby = 'cumulative'
  # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
  # ps.print_stats()
  # sys.stdout.write(s.getvalue())




if __name__ == "__main__":
  main()