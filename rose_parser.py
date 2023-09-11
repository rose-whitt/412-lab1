import sys
import scanner

class RoseParser():
    def __init__(self, scan):
        self.scan = scan
        self.CATEGORIES = scan.CATEGORIES
        self.line_num = scan.line_num
        self.OPS = []

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


        



    def parse_line(self, token_list, line_num):
        idx = 0
        memop_idx = idx
        print('IN PARSE LINE')
        if (token_list[idx][0] == self.MEMOP):
            idx += 1
            if (token_list[idx][0] != self.REGISTER):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                return False
            else:
                idx += 1
                if (token_list[idx][0] != self.INTO):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                if (token_list[idx][0] != self.REGISTER):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                if (token_list[idx][0] == self.EOL):
                    # print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                    return True
                else:
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing EOL in ' + token_list[memop_idx][1] + "\n")
                    return False
        elif (token_list[idx][0] == self.LOADI):
            idx += 1
            if (token_list[idx][0] != self.CONSTANT):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing CONSTANT in ' + token_list[memop_idx][1])
                return False
            else:
                idx += 1

                if (token_list[idx][0] != self.INTO):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1

                if (token_list[idx][0] != self.REGISTER):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1

                if (token_list[idx][0] == self.EOL):
                    # print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                    return True
                else:
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing EOL in ' + token_list[memop_idx][1] + "\n")
                    return False
        elif (token_list[idx][0] == self.ARITHOP):
            idx += 1
            
            if (token_list[idx][0] != self.REGISTER):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                return False
            else:
                idx += 1
                if (token_list[idx][0] != self.COMMA):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing COMMA in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                # ARITHOP REG COMMA 
                if (token_list[idx][0] != self.REGISTER):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                if (token_list[idx][0] != self.INTO):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing INTO in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                if (token_list[idx][0] != self.REGISTER):
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing REGISTER in ' + token_list[memop_idx][1] + "\n")
                    return False
                idx += 1
                # while (token_list[idx][0] == self.BLANK):   # iterate to next non-blank
                #     idx += 1
                if (token_list[idx][0] == self.EOL):
                    # print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                    return True
                else:
                    sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing EOL in ' + token_list[memop_idx][1] + "\n")
                    return False
        elif (token_list[idx][0] == self.OUTPUT):
            idx += 1

            if (token_list[idx][0] != self.CONSTANT):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing CONSTANT in ' + token_list[memop_idx][1] + "\n")
                return False
            idx += 1

            if (token_list[idx][0] == self.EOL):
                # print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                return True
            else:
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               Missing EOL in ' + token_list[memop_idx][1] + "\n")
                return False
        elif (token_list[idx][0] == self.NOP):
            idx += 1
            if (token_list[idx][0] != self.EOL and token_list[idx][0] != self.EOF):
                sys.stderr.write("[PARSER] ERROR " + str(line_num) + '               wrong thing after NOP' +  "\n")
                return False
            else:
                # print("[PARSER] Valid NOP sentence")
                return True



        
        return self.CATEGORIES
    

    def finish_memop(self, scan):
        token = scan.get_token()
        while (token[0] == self.BLANK):
            token = scan.get_token()
        if (token[0] != self.REGISTER):
            sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing first REGISTER in MEMOP (load or store); token: ' + str(token[0]) +  '\n')
            return False
        else:
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            if (token[0] != self.INTO):
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing INTO in MEMOP (load or store); token: ' + str(token[0]) +  '\n')
                return False
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            if (token[0] != self.REGISTER):
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing target (second) REGISTER in MEMOP (load or store); token: ' + str(token[0]) +  '\n')
                return False
            else:
                token = scan.get_token()
                while (token[0] == self.BLANK):
                    token = scan.get_token()
                if (token[0] == self.EOL):
                    # print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                    # TODO: build IR for this OP, add IR to list of OPS
                    self.OPS.append([scan.line_num, 'MEMOP'])
                    scan.line_num += 1
                    scan.char_idx = -1
                    scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
                    return True
                else:
                    sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing EOL in MEMOP (load or store); token: ' + str(token[0]) +  '\n')
                    return False

    def finish_loadI(self, scan):
        token = scan.get_token()
        while (token[0] == self.BLANK):
            token = scan.get_token()
        if (token[0] != self.CONSTANT):
            sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing CONSTANT in LOADI; token: ' + str(token[0]) +  '\n')
            return False
        else:
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            if (token[0] != self.INTO):
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing INTO in LOADI; token: ' + str(token[0]) +  '\n')
                return False
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            if (token[0] != self.REGISTER):
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing REGISTER in LOADI; token: ' + str(token[0]) +  '\n')
                return False
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            if (token[0] == self.EOL):
                # print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                self.OPS.append([scan.line_num, 'LOADI'])
                scan.line_num += 1
                scan.char_idx = -1
                scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
                return True
            else:
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing EOL in LOADI; token: ' + str(token[0]) +  '\n')
                return False
            
    def finish_arithop(self, scan):
        token = scan.get_token() 
        # if (token[0] != self.BLANK):
        #     sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing BLANK after ARITHOP opcode; token: ' + str(token[0]) +  '\n')
        #     return False
        while (token[0] == self.BLANK):
            token = scan.get_token()
        if (token[0] != self.REGISTER):
            sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing first REGISTER in ARITHOP; token: ' + str(token[0]) +  '\n')
            return False
        else:
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            if (token[0] != self.COMMA):
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing COMMA in ARITHOP; token: ' + str(token[0]) +  '\n')
                return False
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            # ARITHOP REG COMMA 
            if (token[0] != self.REGISTER):
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing second REGISTER in ARITHOP; token: ' + str(token[0]) +  '\n')
                return False
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            if (token[0] != self.INTO):
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing INTO in ARITHOP; token: ' + str(token[0]) +  '\n')
                return False
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            if (token[0] != self.REGISTER):
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing target (third) REGISTER in ARITHOP; token: ' + str(token[0]) +  '\n')
                return False
            token = scan.get_token()
            while (token[0] == self.BLANK):
                token = scan.get_token()
            if (token[0] == self.EOL):
                # print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
                self.OPS.append([scan.line_num, 'ARITHOP'])
                scan.line_num += 1
                scan.char_idx = -1
                scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
                return True
            else:
                sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing EOL in ARITHOP; token: ' + str(token[0]) +  '\n')
                return False
            
    def finish_output(self, scan):
        token = scan.get_token()
        while (token[0] == self.BLANK):
            token = scan.get_token()
        # NOTE: i think the scanner picks up on the no 
        # if (token[0] != self.BLANK):
        #     sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing BLANK after OUTPUT opcode; token: ' + str(token[0]) +  '\n')
        #     return False
        # token = scan.get_token()
        if (token[0] != self.CONSTANT):
            sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing CONSTANT in OUTPUT; token: ' + str(token[0]) +  '\n')
            return False
        token = scan.get_token()
        if (token[0] == self.EOL):
            # print("[PARSER] Valid " + token_list[memop_idx][1] + " sentence")
            self.OPS.append([scan.line_num, 'OUTPUT'])
            scan.line_num += 1
            scan.char_idx = -1
            scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
            return True
        else:
            sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               Missing EOL in OUTPUT; token: ' + str(token[0]) +  '\n')
            return False
    
    def finish_nop(self, scan):
        token = scan.get_token()
        while (token[0] == self.BLANK):
            token = scan.get_token()
        if (token[0] != self.EOL and token[0] != self.EOF):
            sys.stderr.write("[PARSER] ERROR " + str(scan.line_num) + '               wrong thing after NOP; token: ' + str(token[0]) +  '\n')
            return False
        else:
            # print("[PARSER] Valid NOP sentence")
            self.OPS.append([scan.line_num, 'NOP'])
            scan.line_num += 1
            scan.char_idx = -1
            scan.cur_line = scan.convert_line_to_ascii_list(scan.input_file.readline())
            return True