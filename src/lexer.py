import ply.lex as lex
import os

# -----------------------------
# دیکشنری کلمات کلیدی
# -----------------------------
reserved = {
    'int':    'INT',
    'char':   'CHAR',
    'if':     'IF',
    'else':   'ELSE',
    'while':  'WHILE',
    'for':    'FOR',
    'return': 'RETURN',
    'printf': 'PRINTF',
    'scanf':  'SCANF'
}

# -----------------------------
# فهرست توکن‌ها
# -----------------------------
tokens = list(reserved.values()) + [
    'IDENTIFIER', 'NUMBER',
    'OPERATOR', 'PUNCTUATION',
    'STRING'
]

# -----------------------------
# الگوهای ساده
# -----------------------------
t_OPERATOR    = r'==|!=|<=|>=|[+\-*/=<>]'
t_PUNCTUATION = r'[;{}()\[\],]'
t_STRING      = r'\"([^\\\n]|(\\.))*?\"'
t_ignore      = ' \t\r'

# -----------------------------
# شناسایی Identifier و کلمات کلیدی
# -----------------------------
def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# -----------------------------
# شناسایی عدد
# -----------------------------
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# -----------------------------
# شمارش خط
# -----------------------------
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# -----------------------------
# خطا
# -----------------------------
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}, pos {t.lexpos}")
    t.lexer.skip(1)

# -----------------------------
# ساختِ Lexer
# -----------------------------
lexer = lex.lex()

# -----------------------------
# تابع تست از فایل
# -----------------------------
def test_lexer_from_file(filename):
    # پیدا کردن مسیر فایل نسبت به این اسکریپت
    script_dir = os.path.dirname(os.path.realpath(__file__))
    filepath = filename if os.path.isabs(filename) else os.path.join(script_dir, filename)

    if not os.path.exists(filepath):
        print(f"❌ File '{filepath}' not found.")
        return

    data = open(filepath, 'r', encoding='utf-8').read()
    lexer.input(data)

    print(f"\n🔍 Tokens in '{os.path.basename(filepath)}':\n")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"{tok.type}: {tok.value} (Line: {tok.lineno}, Pos: {tok.lexpos})")

# -----------------------------
# بلوک اصلی
# -----------------------------
if __name__ == '__main__':
    # اگر خواستی می‌تونی اسم فایل رو از آرگومان بگیری:
    # import sys
    # filename = sys.argv[1] if len(sys.argv)>1 else 'input.mc'
    # اینجا من ثابت گذاشتم:
    test_lexer_from_file('input.mc')
