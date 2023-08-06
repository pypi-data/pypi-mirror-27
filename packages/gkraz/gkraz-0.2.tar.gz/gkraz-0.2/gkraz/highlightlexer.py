from pygments.lexer import RegexLexer, words
from pygments.token import *

from . import functions

class HighlightLexer(RegexLexer):
    name = 'HighlightLexer'
    aliases = [ 'highlightlexer' ]

    tokens = {
        'root': [
            ('^#.*$', Comment.Preproc),
            (r'\b(and|or|not|mod)\b', Operator),
            (words((functions.get_builtin_names()), suffix=r'\b'), Name.Builtin),
            ('[a-zA-Z_]\w*', Name),
            (r'(\d+\.\d*|\d+)([eE][+-]?[0-9]+)?', Number),
            (r'\d+', Number),
            (r'\(|\)|\[|\]|\{|\}|,', Punctuation),
            (r'=|\+|-|\*|/|\^|>|<|>=|<=|==|\!=|@|\$|->', Operator),
        ]
    }
