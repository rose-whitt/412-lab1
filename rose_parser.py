import sys
import scanner

class RoseParser():
    def __init__(self, scan):
        self.scan = scan
        self.CATEGORIES = scan.CATEGORIES
        self.MEMOP = 0   # load, store
        self.LOADI = 1   # loadI
        self.ARITHOP = 2 # add, sub, mult, lshift, rshift
        self.OUTPUT = 3  # output, prints MEM(x) to stdout
        self.NOP = 4     # nop, idle for one second
        self.CONSTANT = 5    # a non-negative integer
        self.REGISTER = 6    # 'r' followed by a constant
        self.COMMA = 7   # ','
        self.INTO = 8    # "=>"
        self.EOF = 9     # input has been exhausted
        self.EOL = 10    # end of current line ("\r\n" or "\n")
        self.BLANK = 11     # not an opcode, but used to signal blank space or tab



    def parse_line(self, token_list, line_num):
        idx = 0
        while (token_list[idx][0] == self.BLANK):   # iterate to first non-blank
            # print("poo")
            idx += 1
        # print("[PARSER-DEBUG] " + str(idx) + " index, number of blanks.")
        memop_idx = idx
        if (token_list[idx][0] == self.MEMOP):
            idx += 1
            if (token_list[idx][0] != self.BLANK):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing blank after opcode ' + token_list[memop_idx][1] + "\n")
                return False
            else:
                while (token_list[idx][0] == self.BLANK):   # iterate to first non-blank after opcode
                    # print("CUNT")
                    idx += 1
            
            # remove rest of blanks now that we checked -- jk i think its faster to just skip them bc with removing wed have to iterate over list twice
            
            if (token_list[idx][0] != self.REGISTER):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                return False
            else:
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] != self.INTO):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] != self.REGISTER):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] == self.EOL):
                    print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                    return True
                else:
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing EOL in ' + token_list[memop_idx][1] + "\n")
                    return False
        elif (token_list[idx][0] == self.LOADI):
            idx += 1
            if (token_list[idx][0] != self.BLANK):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing blank after opcode ' + token_list[memop_idx][1] + "\n")
                return False
            else:
                while (token_list[idx][0] == self.BLANK):   # iterate to first non-blank after opcode
                    # print("CUNT")
                    idx += 1
            # print("[PARSER] next char is " +  token_list[idx][1])


            if (token_list[idx][0] != self.CONSTANT):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing CONSTANT in ' + token_list[memop_idx][1])
                return False
            else:
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] != self.INTO):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[memop_idx][1] + "\n")
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) +  " - got character '" +  token_list[idx][1] + "' instead.\n")
                    return False
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] != self.REGISTER):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] == self.EOL):
                    print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                    return True
                else:
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing EOL in ' + token_list[memop_idx][1] + "\n")
                    return False
        elif (token_list[idx][0] == self.ARITHOP):
            idx += 1
            if (token_list[idx][0] != self.BLANK):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing blank after opcode ' + token_list[memop_idx][1] + "\n")
                return False
            else:
                while (token_list[idx][0] == self.BLANK):   # iterate to first non-blank after opcode
                    # print("CUNT")
                    idx += 1
            # print("[PARSER] next char is " +  token_list[idx][1])

            
            if (token_list[idx][0] != self.REGISTER):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                return False
            else:
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] != self.COMMA):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing COMMA in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                # ARITHOP REG COMMA 
                if (token_list[idx][0] != self.REGISTER):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] != self.INTO):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] != self.REGISTER):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
                if (token_list[idx][0] == self.EOL):
                    print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                    return True
                else:
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing EOL in ' + token_list[memop_idx][1] + "\n")
                    return False
        elif (token_list[idx][0] == self.OUTPUT):
            idx += 1
            if (token_list[idx][0] != self.BLANK):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing blank after opcode ' + token_list[memop_idx][1] + "\n")
                return False
            else:
                while (token_list[idx][0] == self.BLANK):   # iterate to first non-blank after opcode
                    # print("CUNT")
                    idx += 1
            # print("[PARSER] next char is " +  token_list[idx][1])

            if (token_list[idx][0] != self.CONSTANT):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing CONSTANT in ' + token_list[memop_idx][1] + "\n")
                return False
            idx += 1
            while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                    idx += 1
            if (token_list[idx][0] == self.EOL):
                print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                return True
            else:
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing EOL in ' + token_list[memop_idx][1] + "\n")
                return False
        elif (token_list[idx][0] == self.NOP):
            idx += 1
            if (token_list[idx][0] != self.BLANK and token_list[idx][0] != self.EOL and token_list[idx][0] != self.EOF):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               wrong thing after NOP' +  "\n")
                return False
            else:
                print("[PARSER] Valid NOP sentence")
                return True



        
        return self.CATEGORIES
    