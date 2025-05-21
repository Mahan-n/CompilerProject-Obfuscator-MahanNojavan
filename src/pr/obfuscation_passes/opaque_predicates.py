import random
from lexer_parser.ast_nodes import If, BinOp, Num, Compound


class OpaquePredicateInserter:
    def insert(self, ast):
        for func in ast.functions:
            new_statements = []
            for stmt in func.body.statements:
                if random.random() < 0.5:  # 50% chance to wrap with opaque predicate
                    opaque_if = self._make_opaque_if(stmt)
                    new_statements.append(opaque_if)
                else:
                    new_statements.append(stmt)
            func.body.statements = new_statements
        return ast

    def _make_opaque_if(self, stmt):
        # Always true: (1 * 1 == 1)
        inner = BinOp(left=Num(1), op='*', right=Num(1))
        cond = BinOp(left=inner, op='==', right=Num(1))
        return If(cond, Compound([stmt]), None)


# ✅ Wrapper for the obfuscation framework
from .base_pass import BaseObfuscationPass


class InsertOpaquePredicates(BaseObfuscationPass):
    def apply(self, ast):
        inserter = OpaquePredicateInserter()
        inserter.insert(ast)
