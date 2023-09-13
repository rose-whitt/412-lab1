import sys
import scanner

class RoseParser():
    def __init__(self, scan):
        self.scan = scan
        self.CATEGORIES = scan.CATEGORIES
        self.line_num = scan.line_num
        self.num_iloc_ops = 0
        self.num_parser_errors = 0

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
        self.SCANNER_ERROR = 12 # not an opcode, used to signify error in scanner (lexical/spelling error)

