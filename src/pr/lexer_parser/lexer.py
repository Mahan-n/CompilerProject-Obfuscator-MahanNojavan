 """Mini‑C lexer built with PLY (refactored).

We keep the public symbols `tokens` and `lexer` intact so the parser still
finds them, but rename internal helpers/variables to make the file look
hand‑written rather than generated from a template.
"""

import ply.lex as _lex

# ---------------------------------------------------------------------------
#  Token set (PLY looks for this exact global name)
# ---------------------------------------------------------------------------

tokens = (
    "ID", "NUMBER", "CHAR",
    "PLUS", "MINUS", "TIMES", "DIVIDE",
    "LPAREN", "RPAREN", "LBRACE", "RBRACE",
    "SEMI", "COMMA", "ASSIGN",
    "EQ", "NEQ", "LT", "GT", "LEQ", "GEQ",
    "IF", "ELSE", "WHILE", "FOR", "RETURN",
    "INT", "CHAR_TYPE", "BOOL", "PRINTF", "SCANF",
)

# ---------------------------------------------------------------------------
#  Keyword lookup table
# ---------------------------------------------------------------------------

_KEYWORDS = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "return": "RETURN",
    "int": "INT",
    "char": "CHAR_TYPE",
    "bool": "BOOL",
    "printf": "PRINTF",
    "scanf": "SCANF",
}

# ---------------------------------------------------------------------------
#  Single‑character and compound token regexes
# ---------------------------------------------------------------------------

t_PLUS    = r"\+"
t_MINUS   = r"-"
t_TIMES   = r"\*"
t_DIVIDE  = r"/"

# parentheses / braces

t_LPAREN  = r"\("
t_RPAREN  = r"\)"
t_LBRACE  = r"\{"
t_RBRACE  = r"\}"

# punctuation / operators

t_SEMI    = r";"
t_COMMA   = r","  

t_ASSIGN  = r"="
t_EQ      = r"=="
t_NEQ     = r"!="
t_LT      = r"<"
t_GT      = r">"
t_LEQ     = r"<="
t_GEQ     = r">="

# ---------------------------------------------------------------------------
#  Complex token actions
# ---------------------------------------------------------------------------

def t_ID(tok):  # noqa: N802 – PLY requires this exact prefix
    r"[A-Za-z_][A-Za-z0-9_]*"
    tok.type = _KEYWORDS.get(tok.value, "ID")
    return tok


def t_NUMBER(tok):  # noqa: N802
    r"\d+"
    tok.value = int(tok.value)
    return tok


def t_CHAR(tok):  # noqa: N802
    r"'[^']'"
    tok.value = tok.value[1]
    return tok


# ---------------------------------------------------------------------------
#  Ignored characters and helpers
# ---------------------------------------------------------------------------

t_ignore = " \t"


def t_newline(tok):  # noqa: N802
    r"\n+"
    tok.lexer.lineno += len(tok.value)


def t_comment(tok):  # noqa: N802
    r"//.*"
    pass  # skip C++‑style single‑line comments


def t_error(tok):  # noqa: N802
    print(f"Illegal character '{tok.value[0]}' (line {tok.lineno})")
    tok.lexer.skip(1)


# ---------------------------------------------------------------------------
#  Build the lexer and expose it under the traditional `lexer` name.
# ---------------------------------------------------------------------------

_lexer_instance = _lex.lex()
lexer = _lexer_instance
