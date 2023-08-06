from .errors import ParseError

class LexTok:
    ID  = 1
    SYM = 2
    NUM = 3
    EOF = 4
    def __init__(self,type,content,pos):
        self.type = type
        self.content = content
        self.pos = pos

def lex(expr):
    class State:
        NONE     = 0
        ID       = 1
        NUM      = 2
        NUM_AC   = 3
        NUM_EXP1 = 4
        NUM_EXP  = 5

    expr += " "

    state = State.NONE
    tok = ""

    i = 0
    while True:
        if state == State.NONE:
            if expr[i].isspace():
                i+=1
                if (i == len(expr)):
                    yield LexTok(LexTok.EOF,None,i)
                    return
            elif expr[i].isalpha() or expr[i] == "_":
                state = State.ID
            elif expr[i].isnumeric():
                state = State.NUM
            else:
                op = expr[i:][:2]
                if op in [">=","<=","==","!=","->"]:
                    yield LexTok(LexTok.SYM,op,i)
                    i+=2
                else:
                    op = expr[i:][:1]
                    if op in ["(",")","[","]","{","}","+","-",
                            "*","/","^","=","<",">",",","@","$"]:
                        yield LexTok(LexTok.SYM,op,i)
                        i+=1
                    else:
                        raise ParseError("Unknown character",i)
        if state == State.ID:
            if expr[i].isalnum() or expr[i] == "_":
                tok += expr[i]
                i += 1
            else:
                if tok in ["and","or","not","mod"]:
                    yield LexTok(LexTok.SYM,tok,i-len(tok))
                else:
                    yield LexTok(LexTok.ID,tok,i-len(tok))
                tok = ""
                state = State.NONE
        elif state >= State.NUM:
            if expr[i].isnumeric():
                tok += expr[i]
                i += 1
                if state == State.NUM_EXP1:
                    state = State.NUM_EXP
            elif state == State.NUM and expr[i] == ".":
                state = State.NUM_AC
                tok += expr[i]
                i += 1
            elif (state == State.NUM or state == State.NUM_AC) and (expr[i] == "e" or expr[i] == "E"):
                tok += expr[i]
                i += 1
                if expr[i] == "+" or expr[i] == "-":
                    tok += expr[i]
                    i += 1
                state = State.NUM_EXP1
            elif state == State.NUM_EXP1:
                raise ParseError("Expected digit in exponent",i)
            else:
                yield LexTok(LexTok.NUM,float(tok),i-len(tok))
                tok = ""
                state = State.NONE
