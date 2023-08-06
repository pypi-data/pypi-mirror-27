from prompt_toolkit.token import Token

class StmtException(Exception):
    def __init__(self,message,pos):
        self.message = message
        self.pos = pos

    def __str__(self):
        return self.message

class ParseError(StmtException):
    pass

class CommandError(StmtException):
    pass

def err_msg_tokens(err,num):
    if isinstance(err,StmtException):
        postok = [(Token.Prompt," "*(len(str(num))+4+err.pos) + "^\n")]
    else:
        postok = []


    return postok + [
        (Token.ErrorBold, type(err).__name__ + ": "),
        (Token.Error, str(err)+"\n")
    ]
