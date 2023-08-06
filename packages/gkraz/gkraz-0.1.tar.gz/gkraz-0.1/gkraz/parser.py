from collections import namedtuple, deque

from gkraz.lexer import *
from gkraz.bytecode import *
from gkraz.errors import ParseError

class BinaryOpAST:
    def __init__(self,op,left,right):
        self.op    = op
        self.left  = left
        self.right = right

    def gen_bc(self,bc):
        self.left.gen_bc(bc)
        self.right.gen_bc(bc)
        opcode = {
            "+":   OpCo.ADD,
            "-":   OpCo.SUB,
            "*":   OpCo.MUL,
            "/":   OpCo.DIV,
            "mod": OpCo.MOD,
            "and": OpCo.AND,
            "or":  OpCo.OR,
            "^":   OpCo.POW,
            "@":   OpCo.DOT
        }[self.op]
        bc.append(Bytecode(opcode))

class UnaryOpAST:
    def __init__(self,op,expr):
        self.op   = op
        self.expr = expr

    def gen_bc(self,bc):
        self.expr.gen_bc(bc)
        if self.op != "+":
            opcode = {
                "-":   OpCo.NEG,
                "not": OpCo.NOT,
            }[self.op]
            bc.append(Bytecode(opcode))

class CompOpAST:
    def __init__(self,ops,exprs):
        self.ops   = ops
        self.exprs = exprs

    def gen_bc(self,bc):
        for nr,expr in enumerate(self.exprs):
            expr.gen_bc(bc)
            if nr > 0:
                if nr < len(self.exprs)-1:
                    bc.append(Bytecode(OpCo.STO,0))
                opcode = {
                    ">":  OpCo.GT,
                    "<":  OpCo.LT,
                    ">=": OpCo.GTE,
                    "<=": OpCo.LTE,
                    "==": OpCo.EQ,
                    "!=": OpCo.NEQ
                }[self.ops[nr-1]]
                bc.append(Bytecode(opcode))
                if nr < len(self.exprs)-1:
                    bc.append(Bytecode(OpCo.LD,0))

        for i in range(1,len(self.ops)):
            bc.append(Bytecode(OpCo.AND))

class FuncCallAST:
    def __init__(self,name,params):
        self.name   = name
        self.params = params

    def gen_bc(self,bc):
        for param in self.params:
            param.gen_bc(bc)
        bc.append(Bytecode(OpCo.FUN,self.name,len(self.params)))

class VarExprAST:
    def __init__(self,name):
        self.name = name

    def gen_bc(self,bc):
        bc.append(Bytecode(OpCo.VAR,self.name))

class LiteralAST:
    def __init__(self,value):
        self.value = value

    def gen_bc(self,bc):
        bc.append(Bytecode(OpCo.LIT,self.value))

class VectorAST:
    def __init__(self,elements):
        self.elements = elements

    def gen_bc(self,bc):
        for element in self.elements:
            element.gen_bc(bc)
        bc.append(Bytecode(OpCo.VEC,len(self.elements)))

class FuncDefAST:
    def __init__(self,name,params,expr):
        self.name   = name
        self.params = params
        self.expr   = expr

    def gen_bc(self,bc):
        self.expr.gen_bc(bc)

class VarDefAST:
    def __init__(self,name,expr):
        self.name   = name
        self.expr   = expr

    def gen_bc(self,bc):
        self.expr.gen_bc(bc)

OpP = namedtuple("OpP",["ops","binary","comp"])

OP_PREC = [
    OpP( ["or"],                        True,  False ),
    OpP( ["and"],                       True,  False ),
    OpP( ["not"],                       False, False ),
    OpP( ["==","!=",">","<","<=",">="], True,  True  ),
    OpP( ["+","-"],                     True,  False ),
    OpP( ["*","/","mod","@"],           True,  False ),
    OpP( ["^"],                         True,  False ),
    OpP( ["+","-"],                     False, False ),
]

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.cur = next(self.tokens)
        self.la  = deque()

    def op_is(self,tok,op):
        return tok.type == LexTok.SYM and tok.content == op

    def accept(self,op):
        if self.op_is(self.cur,op):
            self.next_tok()
            return True
        else:
            return False

    def next_tok(self,n=1):
        for i in range(0,n):
            if len(self.la) == 0:
                self.cur = next(self.tokens)
            else:
                self.cur = self.la.popleft()

    def lookahead(self,n):
        if len(self.la) < n:
            for i in range(0,n-len(self.la)):
                self.la.append(next(self.tokens))
        return self.la[n-1]

    def parseStmt(self):
        stmt = self.parseVarDef() or self.parseFuncDef() or self.parseExpr()
        if self.cur.type != LexTok.EOF:
            raise ParseError("Expected variable or function definition or expression",
                    self.cur.pos)
        return stmt

    def parseVarDef(self):
        if self.cur.type != LexTok.ID:
            return None
        name = self.cur.content
        eq = self.lookahead(1)
        if not self.op_is(eq,"="):
            return None
        self.next_tok(2)

        expr = self.parseExpr()
        if expr is None:
            raise ParseError("Expected expression for variable value",self.cur.pos)
        return VarDefAST(name,expr)

    def parseFuncDef(self):
        if self.cur.type != LexTok.ID:
            return None
        name = self.cur.content
        bra = self.lookahead(1)
        if not self.op_is(bra,"("):
            return None
        params = []
        ntok = self.lookahead(2)
        lai = 2
        if ntok.type == LexTok.ID:
            params.append(ntok.content)
            lai += 1
            while self.op_is(self.lookahead(lai),","):
                lai += 1
                ntok = self.lookahead(lai)
                if ntok.type != LexTok.ID:
                    return None
                params.append(ntok.content)
                lai += 1
        if not self.op_is(self.lookahead(lai),")"):
            return None
        lai += 1
        if not self.op_is(self.lookahead(lai),"="):
            return None
        lai += 1

        self.next_tok(lai)
        expr = self.parseExpr()
        if expr is None:
            raise ParseError("Expected expression for function body",self.cur.pos)
        return FuncDefAST(name,params,expr)

    def parseExpr(self):
        return self.parseOpExpr(0)

    def parseFuncExpr(self):
        if self.cur.type != LexTok.ID:
            return None
        name = self.cur.content
        bra = self.lookahead(1)
        if not self.op_is(bra,"("):
            return None
        self.next_tok(2)

        params = []
        expr = self.parseExpr()
        if expr is not None:
            params.append(expr)
            while self.accept(","):
                expr = self.parseExpr()
                if expr is None:
                    raise ParseError("Expected parameter expression",self.cur.pos)
                params.append(expr)
        if not self.accept(")"):
            raise ParseError("Expected ')'",self.cur.pos)
        return FuncCallAST(name,params)

    def parseOpExpr(self,prec):
        if prec == len(OP_PREC):
            return self.parseMulExpr()
        opr = OP_PREC[prec]
        if opr.binary:
            expr1 = self.parseOpExpr(prec+1)
            if expr1 is None:
                return None
            if opr.comp:
                ops = []
                exprs = [expr1]

            while self.cur.type == LexTok.SYM and self.cur.content in opr.ops:
                op = self.cur.content
                self.next_tok()
                expr2 = self.parseOpExpr(prec+1)
                if expr2 is None:
                    raise ParseError("Expected expression after operator",self.cur.pos)
                if opr.comp:
                    ops.append(op)
                    exprs.append(expr2)
                else:
                    expr1 = BinaryOpAST(op,expr1,expr2)

            if opr.comp:
                if len(exprs) == 1:
                    return exprs[0]
                else:
                    return CompOpAST(ops,exprs)
            else:
                return expr1
        else:
            if self.cur.type == LexTok.SYM and self.cur.content in opr.ops:
                op = self.cur.content
                self.next_tok()
            else:
                op = None
            expr = self.parseOpExpr(prec+1)
            if op is None:
                return expr
            else:
                if expr is None:
                    raise ParseError("Expected expression after operator",self.cur.pos)
                else:
                    return UnaryOpAST(op,expr)

    def parseMulExpr(self):
        retexpr = None
        while True:
            expr = self.parsePrimaryExpr()
            if expr is None:
                break
            if retexpr is None:
                retexpr = expr
            else:
                retexpr = BinaryOpAST("*",retexpr,expr)

        return retexpr

    def parsePrimaryExpr(self):
        expr = self.parseFuncExpr()
        if expr is not None:
            return expr

        if self.cur.type == LexTok.ID:
            name = self.cur.content
            self.next_tok()
            return VarExprAST(name)

        if self.cur.type == LexTok.NUM:
            value = self.cur.content
            self.next_tok()
            return LiteralAST(value)

        if self.op_is(self.cur,"("):
            self.next_tok()
            expr = self.parseExpr()
            if expr is None:
                raise ParseError("Expected expression after opening bracket",self.cur.pos)
            if not self.accept(")"):
                raise ParseError("Expected ')'",self.cur.pos)
            return expr

        if self.op_is(self.cur,"["):
            self.next_tok()

            elements = []
            expr = self.parseExpr()
            if expr is not None:
                elements.append(expr)
                while self.accept(","):
                    expr = self.parseExpr()
                    if expr is None:
                        raise ParseError("Expected expression after ','",self.cur.pos)
                    elements.append(expr)
            if not self.accept("]"):
                raise ParseError("Expected ']'",self.cur.pos)
            return VectorAST(elements)

        return None
