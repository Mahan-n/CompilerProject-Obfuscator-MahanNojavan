import random
from lexer_parser.ast_nodes import Assignment, Num
from obfuscation_passes.base_pass import BaseObfuscationPass  # Make sure this exists

DEAD_VARS = ['useless', 'dummy', 'junk', 'tmp', 'waste']

def generate_dead_code():
    var_name = random.choice(DEAD_VARS) + str(random.randint(100, 999))
    value = random.randint(0, 1000)
    return Assignment(var_name, Num(value))

def insert_dead_code(ast):
    for func in ast.functions:
        new_statements = []
        for stmt in func.body.statements:
            if random.random() < 0.4:
                new_statements.append(generate_dead_code())
            new_statements.append(stmt)
            if random.random() < 0.3:
                new_statements.append(generate_dead_code())
        func.body.statements = new_statements
    return ast

# ✅ Wrap it in a class so it works with the obfuscation framework
class RemoveDeadCode(BaseObfuscationPass):
    def apply(self, ast):
        insert_dead_code(ast)
