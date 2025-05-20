import ply.yacc as yacc
import os, sys
from lexer import tokens

# -----------------------------------
# 1. برنامه: فهرست statementها
# -----------------------------------
def p_program(p):
    'program : statement_list'
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# -----------------------------------
# 2. انواع statement
# -----------------------------------
def p_statement(p):
    '''statement : declaration
                 | assignment
                 | if_statement
                 | while_statement
                 | return_statement
                 | call_statement'''
    p[0] = p[1]

# -----------------------------------
# 3. تعریف متغیر: int x; یا char y;
# -----------------------------------
def p_declaration(p):
    'declaration : type_specifier IDENTIFIER PUNCTUATION'
    if p[3] != ';':
        raise SyntaxError("Missing ';' after declaration")
    p[0] = ('declaration', p[1], p[2])

def p_type_specifier(p):
    '''type_specifier : INT
                      | CHAR'''
    p[0] = p[1]

# -----------------------------------
# 4. انتساب: x = expr;
# -----------------------------------
def p_assignment(p):
    'assignment : IDENTIFIER OPERATOR expression PUNCTUATION'
    # p[1]=x, p[2]='=', p[3]=expr, p[4]=';'
    if p[2] != '=':
        raise SyntaxError("Expected '=' in assignment")
    if p[4] != ';':
        raise SyntaxError("Missing ';' after assignment")
    p[0] = ('assign', p[1], p[3])

# -----------------------------------
# 5. عبارت (Expression)
# -----------------------------------
def p_expression(p):
    '''expression : NUMBER
                  | IDENTIFIER
                  | STRING'''
    p[0] = p[1]

def p_expression_binop(p):
    'expression : expression OPERATOR expression'
    p[0] = ('binop', p[2], p[1], p[3])

# -----------------------------------
# 6. شرط if … [else …]
# -----------------------------------
def p_if_statement(p):
    '''if_statement : IF PUNCTUATION expression PUNCTUATION compound_stmt
                    | IF PUNCTUATION expression PUNCTUATION compound_stmt ELSE compound_stmt'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if_else', p[3], p[5], p[7])

# -----------------------------------
# 7. حلقه while
# -----------------------------------
def p_while_statement(p):
    'while_statement : WHILE PUNCTUATION expression PUNCTUATION compound_stmt'
    p[0] = ('while', p[3], p[5])

# -----------------------------------
# 8. return expr;
# -----------------------------------
def p_return_statement(p):
    'return_statement : RETURN expression PUNCTUATION'
    if p[3] != ';':
        raise SyntaxError("Missing ';' after return")
    p[0] = ('return', p[2])

# -----------------------------------
# 9. بلوک { statements }
# -----------------------------------
def p_compound_stmt(p):
    'compound_stmt : PUNCTUATION statement_list PUNCTUATION'
    p[0] = ('block', p[2])

# -----------------------------------
# 10. فراخوانی تابع: name(arg,…);
# -----------------------------------
def p_call_statement(p):
    'call_statement : function_name PUNCTUATION argument_list PUNCTUATION PUNCTUATION'
    p[0] = ('call', p[1], p[3])

def p_function_name(p):
    '''function_name : IDENTIFIER
                     | PRINTF
                     | SCANF'''
    p[0] = p[1]

# -----------------------------------
# 11. لیست آرگومان‌ها
# -----------------------------------
def p_argument_list(p):
    '''argument_list : argument_list PUNCTUATION expression
                     | expression
                     | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    p[0] = None

# -----------------------------------
# 12. مدیریت ارور
# -----------------------------------
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

# -----------------------------------
# 13. ساخت Parser
# -----------------------------------
parser = yacc.yacc()

# -----------------------------------
# 14. بلوک اصلی برای تست
# -----------------------------------
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    filepath   = os.path.join(script_dir, 'input.mc')

    if not os.path.exists(filepath):
        print(f"❌ File '{filepath}' not found.")
        sys.exit(1)

    code = open(filepath, 'r', encoding='utf-8').read()
    ast  = parser.parse(code)
    print('\n🧩 AST:', ast)
