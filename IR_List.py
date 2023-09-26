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
        self.value = [None, None, [None, None, None, None], [None, None, None, None], [None, None, None, None]]
        self.next = None
        self.prev = None

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
        while (start != None):
            self.human_readable(start.value)
            start = start.next
    
    def human_readable(self, value):
        """
        Convert values to human readable strings and print them in IR format
        """
        # List 0- third elem in record list
        l0 = value[2][SR]   # SR slot in first record list
        opcode = value[1]
        if (opcode == MEMOP or opcode == LOADI or (opcode >= OUTPUT and opcode <= COMMA)):
            l0 = "sr" + str(l0)
        elif (opcode == ARITHOP or opcode == INTO):
            l0 = "val " + str(l0)
        else:
            l0 = ""
        
        # List 1- fourth elem in record list
        l1 = value[3][SR]
        if (opcode >= OUTPUT and opcode <= COMMA):
            l1 = "sr" + str(l1)
        else:
            l1 = ""
        
        # List 2- fifth element in record list
        l2 = value[4][SR]
        if (opcode >= MEMOP and opcode <= COMMA):
            l2 = "sr" + str(l2)
        else:
            l2 = ""
        
        print(f"{self.opcodes[value[1]] : <6}  [ {l0} ], [ {l1} ], [ {l2} ]")
        