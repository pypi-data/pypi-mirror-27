from enum import Enum

class OpCo(Enum):
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    MOD = 5
    AND = 6
    OR  = 7
    NOT = 8
    NEG = 9
    EQ  = 10
    NEQ = 11
    GT  = 12
    GTE = 13
    LT  = 14
    LTE = 15
    POW = 16
    FUN = 17
    VAR = 18
    LIT = 19
    VEC = 20
    STO = 21
    LD  = 22
    DOT = 23

class Bytecode:
    def __init__(self,opcode,*args):
        self.opcode = opcode
        self.args = args

    def print_bc(self):
        print(self.opcode.name,self.args)
