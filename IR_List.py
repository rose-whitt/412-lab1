MEMOP = 0   # load, store
LOADI = 1   # loadI
ARITHOP = 2 # add, sub, mult, lshift, rshift
OUTPUT = 3  # output, prints MEM(x) to stdout
NOP = 4     # nop, idle for one second
CONSTANT = 5    # a non-negative integer
REGISTER = 6    # 'r' followed by a constant
COMMA = 7   # ','
INTO = 8    # "=>"
EOF = 9     # input has been exhausted
EOL = 10    # end of current line ("\r\n" or "\n")


SR = 0
VR = 1
PR = 2
NU = 3
opcodes_list = ["load", "store", "loadI", "add", "sub", "mult", "lshift", "rshift", "output", "nop"]


class Operand:
    def __init__(self):
        self.sr = None
        self.vr = None
        self.pr = None
        self.nu = None


class Node:
    """
    A node in the IR's doubly linked list.
    """
    def __init__(self):
        """
        - value: representation of block record for operation ([line num, opcode, [sr, vr, pr, nu], [sr, vr, pr, nu], [sr, vr, pr, nu]])
        - next: next record pointer
        - prev: previous record pointer
        """
        # line num, opcode, [sr, vr, pr, nu], [sr, vr, pr, nu], [sr, vr, pr, nu]
        # TODO: possibly not do a nested list structure and do class for operand for speed
        # self.value = [None, None, Operand(), Operand(), Operand()]
        self.line = None
        self.opcode = None
        self.arg1 = Operand()
        self.arg2 = Operand()
        self.arg3 = Operand()

        self.next = None
        self.prev = None
    
    def __str__(self):
        l0 = self.arg1.sr   # SR slot in first record list
        opcode = self.opcode  # value[1] = (category, opcode)- we want the opcode
        if (opcode == 0 or opcode == 1 or (opcode >= 3 and opcode <= 7)):
            l0 = "sr" + str(l0)
        elif (opcode == 2 or opcode == 8):
            l0 = "val " + str(l0)
        else:
            l0 = ""
        
        # List 1- fourth elem in record list
        l1 = self.arg2.sr
        if (opcode >= 3 and opcode <= 7):
            l1 = "sr" + str(l1)
        else:
            l1 = ""
        
        # List 2- fifth element in record list
        l2 = self.arg3.sr
        if (opcode >= 0 and opcode <= 7):
            l2 = "sr" + str(l2)
        else:
            l2 = ""
        
        temp_str = str(self.line) + " : " +  opcodes_list[opcode] + " : [ "  + l0 + " ] , [ " + l1 + " ], [ " + l2 + " ]\n"
        return temp_str
        

    

    # to str
    #     st jskfgldksfg;dgsjlfn value\n
    #     return str


class LinkedList:
    """
    Represents doubly linked list for the IR.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.categories = ["MEMOP", "LOADI", "ARITHOP", "OUTPUT", "NOP", "CONST", "REG", "COMMA", "INTO", "ENDFILE", "NEWLINE"]
        self.opcodes = ["load", "store", "loadI", "add", "sub", "mult", "lshift", "rshift", "output", "nop"]

    def append(self, node: Node):
        if self.head == None and self.tail == None: # empty
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
    
    def print_list(self):
        start = self.head
        temp_string = ""
        while (start != None):
            # print(start)
            temp_string += str(start)
            start = start.next
        print(temp_string)
    
    def human_readable(self, value):
        """
        Convert values to human readable strings and print them in IR format
        """
        # List 0- third elem in record list
        # print("line: " + str(value[0]))
        l0 = value[2][SR]   # SR slot in first record list
        opcode = value[1]  # value[1] = (category, opcode)- we want the opcode
        if (opcode == 0 or opcode == 1 or (opcode >= 3 and opcode <= 7)):
            l0 = "sr" + str(l0)
        elif (opcode == 2 or opcode == 8):
            l0 = "val " + str(l0)
        else:
            l0 = ""
        
        # List 1- fourth elem in record list
        l1 = value[3][SR]
        if (opcode >= 3 and opcode <= 7):
            l1 = "sr" + str(l1)
        else:
            l1 = ""
        
        # List 2- fifth element in record list
        l2 = value[4][SR]
        if (opcode >= 0 and opcode <= 7):
            l2 = "sr" + str(l2)
        else:
            l2 = ""
        
        temp_str = str(value[0]) + " : " +  self.opcodes[opcode] + " : [ "  + l0 + " ] , [ " + l1 + " ], [ " + l2 + " ]\n"

        return temp_str
        # print(f"{self.opcodes[opcode] : <6}  [ {l0} ], [ {l1} ], [ {l2} ]")
        