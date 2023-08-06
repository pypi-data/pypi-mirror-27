from prompt_toolkit.shortcuts import prompt,clear,print_tokens
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory
from prompt_toolkit.contrib.completers import WordCompleter
from os.path import expanduser

from gkraz.highlightlexer import HighlightLexer
from gkraz import functions
from gkraz.lexer import *
from gkraz.parser import Parser,FuncDefAST,VarDefAST
from gkraz.runtime import BcEnvironment
from gkraz import output
from gkraz.errors import err_msg_tokens,CommandError

calc_style = style_from_dict({
    Token: '#ffffff',
    Token.Comment.Preproc: '#ff5f00',
    Token.Operator: '#87ff5f',
    Token.Punctuation: '#87ff5f',
    Token.Name.Builtin: '#5fffff',
    Token.Prompt: '#ffff00 bold',
    Token.Number: '#ff5fff',
    Token.ErrorBold: '#ff0000 bold',
    Token.Error: '#ff0000'
})

config = {
    "vi_mode": False,
    "out_mode": "auto"
}

def get_ptok_main(num):
    def tok_func(cli):
        return [
            (Token.Prompt, '['),
            (Token.Number, str(num)),
            (Token.Prompt, ']: ')
        ]
    return tok_func

def get_ptok_continue(cli):
    return [
        (Token.Prompt, '.. ')
    ]

def index_split(str):
    tokens = []
    indices = []

    in_tok = False
    for i,c in enumerate(str):
        if not in_tok:
            if not c.isspace():
                tokens.append(c)
                indices.append(i)
                in_tok = True
        else:
            if c.isspace():
                in_tok = False
            else:
                tokens[-1] += c

    return tokens,indices

def main():
    history = FileHistory(expanduser("~/.gkraz_history"))
    completer = WordCompleter(functions.get_builtin_names())

    env = BcEnvironment()

    while True:
        try:
            input = prompt(
                    get_prompt_tokens=get_ptok_main(env.get_num()),
                    style=calc_style,
                    lexer=PygmentsLexer(HighlightLexer),
                    vi_mode=config["vi_mode"],
                    completer=completer,
                    complete_while_typing=False,
                    history=history)
            text = input.strip()
            env.inc_num()
            if text != '':
                if text[0] == '#':
                    cmd,indices = index_split(text[1:])
                    if len(cmd) == 0:
                        raise CommandError("Expected command after '#'",1)
                    elif cmd[0] == "exit" or cmd[0] == "quit":
                        if len(cmd) != 1:
                            raise CommandError(cmd[0] + " expects no arguments",indices[1]+1)
                        break
                    elif cmd[0] == "mode":
                        if len(cmd) == 2:
                            if (cmd[1] == "vi"):
                                config["vi_mode"] = True
                            elif (cmd[1] == "emacs"):
                                config["vi_mode"] = False
                            elif (cmd[1] == "sci"):
                                config["out_mode"] = "sci"
                            elif (cmd[1] == "auto"):
                                config["out_mode"] = "auto"
                            elif (cmd[1] == "eng"):
                                config["out_mode"] = "eng"
                            elif (cmd[1] == "dec"):
                                config["out_mode"] = "dec"
                            elif (cmd[1] == "frac"):
                                config["out_mode"] = "frac"
                            else:
                                raise CommandError("Invalid argument for mode",indices[1]+1)
                        else:
                            raise CommandError("mode expects one argument",indices[2]+1)
                    elif cmd[0] == "reset":
                        if len(cmd) != 1:
                            raise CommandError("reset expects no arguments",indices[1]+1)
                        env = BcEnvironment()
                    elif cmd[0] == "clear":
                        if len(cmd) != 1:
                            raise CommandError("clear expects no arguments",indices[1]+1)
                        clear()
                    elif cmd[0] == "matrix":
                        if len(cmd) == 2:
                            input = []
                            while True:
                                input.append(prompt(
                                        get_prompt_tokens=get_ptok_continue,
                                        style=calc_style,
                                        lexer=PygmentsLexer(HighlightLexer),
                                        vi_mode=config["vi_mode"],
                                        completer=completer,
                                        complete_while_typing=False))
                                if input[-1].strip() == "":
                                    break
                            mat = [line.split(" ") for line in input[:-1]]
                            if len(mat) == 0:
                                raise Exception("empty matrix")
                            lines = [ "[" + ",".join(line) + "]" for line in mat ]
                            code  = cmd[1] + " = [" + ",".join(lines) + "]"
                            print(code)

                            parser = Parser(lex(code))
                            stmt = parser.parseStmt()
                            bc = []
                            stmt.gen_bc(bc)
                            env.add_var(stmt.name,bc)
                        else:
                            raise CommandError("matrix expects variable name as argument",
                                    indices[1]+1)
                    else:
                        raise CommandError("unknown command",1)

                else:
                    parser = Parser(lex(text))
                    stmt = parser.parseStmt()
                    bc = []
                    stmt.gen_bc(bc)

                    if isinstance(stmt,FuncDefAST):
                        env.add_func(stmt.name,stmt.params,bc)
                    elif isinstance(stmt,VarDefAST):
                        env.add_var(stmt.name,bc)
                    else:
                        result = env.run_expr(bc)
                        if isinstance(result,float):
                            print(output.format_output(result,config["out_mode"]))
                        elif result is not None:
                            print(result)

        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print_tokens(err_msg_tokens(ex,env.get_num()),style=calc_style)

if __name__ == "__main__":
    main()
