import ply.lex as lex

# لیست توکن‌ها
tokens = [
    'KEYWORD', 'IDENTIFIER', 'NUMBER', 'OPERATOR', 'PUNCTUATION'
]

# تعریف الگوها (regular expressions) برای هر توکن
t_KEYWORD = r'if|else|int|char|void|return'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER = r'\d+'
t_OPERATOR = r'\+|\-|\*|\/|\=|==|!=|<|>'
t_PUNCTUATION = r'\;|\{|\}|\(|\)|\[\]'

# تعریف توکن‌های خاص (برای جلوگیری از چاپ کردن کاراکترهای سفید یا جدید)
t_ignore = ' \t\n'

# تابع برای شناسایی اشتباهات
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# ایجاد Lexer
lexer = lex.lex()

# مثال برای تست Lexer
data = '''
int main() {
    int a = 5;
    if (a > 3) {
        return a;
    }
}
'''

# تجزیه کردن داده‌ها
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
