#!/usr/bin/python -u

import scanner
from IR_List import *
import sys
# import cProfile, pstats
# from io import StringIO

COMMENT = "// ILOC Front End \n"

EOF_FLAG = False


ir_list = LinkedList()




def add_ir_block(scan, line_num, parsed_line):
  """
  Builds a node to be added to IR block

  Input:
    - scan: scanner object
    - line_num: line number of the parsed line
    - parsed_line: list of tokens in the parsed line, each element in form (category, opcode)

  Result:
    Appends node to IR list
  """
  # ex: store => r5     [(0, 1), (8, -1), (6, 5)]
  node = Node()
  opcode = parsed_line[0][1]
  category = parsed_line[0][0]

  node.value[0] = line_num
  node.value[1] = opcode
  

  # MEMOP or LOADI categories
  if (category == scan.MEMOP or category == scan.LOADI):
    # print("MEMOP OR LOADI")
    node.value[2][0] = parsed_line[1][1]  # first register
    node.value[4][0] = parsed_line[3][1]  # second register
  
  # ARITHOP category
  elif (category == scan.ARITHOP):

    node.value[2][0] = parsed_line[1][1]
    node.value[3][0] = parsed_line[3][1]
    node.value[4][0] = parsed_line[5][1]
    # print("line " + str(line_num) + ": " + str(node.value))


  # OUTPUT category
  elif (category == scan.OUTPUT):
    node.value[2][0] = parsed_line[1][1]

  ir_list.append(node)
  return
  
  





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
        memop_node = Node()
        memop_node.value[0] = scan.line_num
        memop_node.value[1] = token[1]

        # temp_line = []
        # temp_line.append(token) # append MEMOP, building line for IR to process

        MEM_OP_FLAG = False
        token = scan.get_token()
        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.REGISTER):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing first REGISTER in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            MEM_OP_FLAG = False
        else:
            memop_node.value[2][0] = token[1]  # first register
            # temp_line.append(token) # append register
            token = scan.get_token()
            while (token[0] == scan.BLANK):
                token = scan.get_token()
            if (token[0] != scan.INTO):
                sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing INTO in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
                scan.num_parser_errors += 1
                MEM_OP_FLAG = False
            else:
              # temp_line.append(token) # append into
              token = scan.get_token()
              while (token[0] == scan.BLANK):
                  token = scan.get_token()
              if (token[0] != scan.REGISTER): # register in scanner returns self.REGISTER, reg_num
                  sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing target (second) REGISTER in MEMOP (load or store); token: ' + str(token[0]) +  ' - [PARSER]\n')
                  scan.num_parser_errors += 1
                  MEM_OP_FLAG = False
              else:
                  memop_node.value[4][0] = token[1]  # second register
                  
                  # temp_line.append(token) # append register
                  token = scan.get_token()
                  while (token[0] == scan.BLANK):
                      token = scan.get_token()
                  if (token[0] == scan.EOL):
                      # build IR
                      # TODO: should i only build it with the -r flag or only print it with the -r flag
                      # add_ir_block(scan, scan.line_num, temp_line)
                      # memop_node = Node()
                      # memop_node.value[0] = scan.line_num
                      # memop_node.value[1] = temp_line[0][1]
                      # memop_node.value[2][0] = temp_line[1][1]  # first register
                      # memop_node.value[4][0] = temp_line[3][1]  # second register
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
        loadi_node.value[0] = scan.line_num
        loadi_node.value[1] = token[1]
        # temp_line = []
        # temp_line.append(token)
        LOADI_FLAG = False
        token = scan.get_token()
        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.CONSTANT):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing CONSTANT in LOADI; token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            LOADI_FLAG = False
        else:
            loadi_node.value[2][0] = token[1]  # first constant
            
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
                  loadi_node.value[4][0] = token[1]  # second register

                  # temp_line.append(token)
                  token = scan.get_token()
                  while (token[0] == scan.BLANK):
                      token = scan.get_token()
                  if (token[0] == scan.EOL):
                      # build ir
                      # add_ir_block(scan, scan.line_num, temp_line)
                      # loadi_node = Node()
                      # loadi_node.value[0] = scan.line_num
                      # loadi_node.value[1] = temp_line[0][1]
                      # loadi_node.value[2][0] = temp_line[1][1]  # first register
                      # loadi_node.value[4][0] = temp_line[3][1]  # second register
                      ir_list.append(loadi_node)


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
        if (LOADI_FLAG == False): # error on line
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.num_error_lines += 1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": LOADI")
        scan.char_idx = -1
      elif (token[0] == scan.ARITHOP):
        ari_node = Node()
        ari_node.value[0] = scan.line_num
        ari_node.value[1] = token[1]
        # temp_line = []
        # temp_line.append(token)
        ARITHOP_FLAG = False
        token = scan.get_token() 

        while (token[0] == scan.BLANK):
            token = scan.get_token()
        if (token[0] != scan.REGISTER):
            sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing first REGISTER in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
            scan.num_parser_errors += 1
            ARITHOP_FLAG = False
        else:
            ari_node.value[2][0] = token[1]
            
            # temp_line.append(token)
            token = scan.get_token()
            while (token[0] == scan.BLANK):
                token = scan.get_token()
            if (token[0] != scan.COMMA):
              sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing COMMA in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
              scan.num_parser_errors += 1
              ARITHOP_FLAG = False
            else:
              # temp_line.append(token)
              token = scan.get_token()
              while (token[0] == scan.BLANK):
                  token = scan.get_token()
              # ARITHOP REG COMMA 
              if (token[0] != scan.REGISTER):
                  sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing second REGISTER in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
                  scan.num_parser_errors += 1
                  ARITHOP_FLAG = False
              else:
                ari_node.value[3][0] = token[1]

                # temp_line.append(token)
                token = scan.get_token()
                while (token[0] == scan.BLANK):
                    token = scan.get_token()
                if (token[0] != scan.INTO):
                    sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing INTO in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
                    scan.num_parser_errors += 1
                    ARITHOP_FLAG = False
                else:
                  # temp_line.append(token)
                  token = scan.get_token()
                  while (token[0] == scan.BLANK):
                      token = scan.get_token()
                  if (token[0] != scan.REGISTER):
                      sys.stderr.write("ERROR " + str(scan.line_num) + ':               Missing target (third) REGISTER in ARITHOP; token: ' + str(token[0]) +  ' - [PARSER]\n')
                      scan.num_parser_errors += 1
                      ARITHOP_FLAG = False
                  else:
                    ari_node.value[4][0] = token[1]
                    
                    # temp_line.append(token)
                    token = scan.get_token()
                    while (token[0] == scan.BLANK):
                        token = scan.get_token()
                    if (token[0] == scan.EOL):
                        # add_ir_block(scan, scan.line_num, temp_line)
                        # ari_node = Node()
                        # ari_node.value[0] = scan.line_num
                        # ari_node.value[1] = temp_line[0][1]
                        # ari_node.value[2][0] = temp_line[1][1]
                        # ari_node.value[3][0] = temp_line[3][1]
                        # ari_node.value[4][0] = temp_line[5][1]
                        ir_list.append(ari_node)

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
       
        if (ARITHOP_FLAG == False):  # error on line
          # scan.line_num += 1
          # scan.char_idx = -1
          scan.num_error_lines += 1
          scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
        # else:
        #   print("[PARSE] " + str(scan.line_num - 1) + ": ARITHOP")
        scan.char_idx = -1
      elif (token[0] == scan.OUTPUT):
        output_node = Node()
        output_node.value[0] = scan.line_num
        output_node.value[1] = token[1]
        # temp_line = []
        # temp_line.append(token)
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
          output_node.value[2][0] = token[1]

          token = scan.get_token()
          while (token[0] == scan.BLANK):
              token = scan.get_token()
          if (token[0] == scan.EOL):
              # add_ir_block(scan, scan.line_num, temp_line)
              # output_node = Node()

              # output_node.value[0] = scan.line_num
              # output_node.value[1] = temp_line[0][1]
              # output_node.value[2][0] = temp_line[1][1]
              ir_list.append(output_node)

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
            # scan.line_num += 1
            # scan.char_idx = -1
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
        # scan.line_num += 1
        # scan.char_idx = -1
        scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
      token = scan.get_token()
    
    # print(str(len(scan.OPS)) + " valid ILOC operations: " + str(scan.OPS))
    if ((scan.num_parser_errors + scan.num_scanner_errors) == 0):
      print("Parse succeeded, finding " + str(scan.num_iloc_ops) + " ILOC operations.")
    else:
      sys.stderr.write("Found " + str(scan.num_parser_errors + scan.num_scanner_errors) + " errors on " + str(scan.num_error_lines) + " lines\n")
    # print(str(scan.num_iloc_ops) + " valid ILOC operations")
  #   print(str(scan.num_parser_errors) + " parser errors.")
  # print(str(scan.num_scanner_errors) + " scanner errors.")
  
    



    
  

    
      
  


def main():
  # pr = cProfile.Profile()
  # pr.enable()
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
      ir_list.print_list()
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

  # pr.disable()
  # s = StringIO()
  # sortby = 'cumulative'
  # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
  # ps.print_stats()
  # sys.stdout.write(s.getvalue())




if __name__ == "__main__":
  main()