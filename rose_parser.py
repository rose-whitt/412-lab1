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


    def parse_line(self, token_list, line_num):
        idx = 0
        if (token_list[idx][0] == self.MEMOP):
            idx += 1
            if (token_list[idx][0] != self.REGISTER):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[idx - 1][1])
                return False
            else:
                idx += 1
                if (token_list[idx][0] != self.INTO):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[idx - 2][1] + "\n")
                    return False
                idx += 1
                if (token_list[idx][0] != self.REGISTER):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[idx - 3][1] + "\n")
                    return False
                idx += 1
                if (token_list[idx][0] == self.EOL):
                    print("[parser] valid sentence")
                    return True
                else:
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing EOL in ' + token_list[idx - 4][1] + "\n")
                    return False
        return self.CATEGORIES
    