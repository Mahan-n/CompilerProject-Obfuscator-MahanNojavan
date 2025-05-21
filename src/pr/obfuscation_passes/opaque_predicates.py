import random
from lexer_parser.ast_nodes import If, BinOp, Num, Compound


class _OpaqueGuardAdder:
    """Inject no‑op conditional wrappers (opaque predicates) into AST blocks."""

    WRAP_PROBABILITY = 0.5  # 50 % chance for each statement

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------
    def inject(self, ast_tree):
        # Iterate over top‑level functions only
        for fn in ast_tree.functions:
            wrapped_body = []
            for stmt in fn.body.statements:
                if random.random() < self.WRAP_PROBABILITY:
                    wrapped_body.append(self._build_guard(stmt))
                else:
                    wrapped_body.append(stmt)
            fn.body.statements = wrapped_body
        return ast_tree

    # --------------------------------------------------------------
    # Helper to craft a trivially true condition (opaque predicate)
    # --------------------------------------------------------------
    @staticmethod
    def _build_guard(statement):
        # Predicate: (1 * 1 == 1) — always true, yet non‑obvious at glance
        opaque_left = BinOp(left=Num(1), op="*", right=Num(1))
        opaque_cond = BinOp(left=opaque_left, op="==", right=Num(1))
        return If(opaque_cond, Compound([statement]), None)


# ------------------------------------------------------------------
# Public wrapper used by the obfuscator framework
# ------------------------------------------------------------------
from .base_pass import BaseObfuscationPass


class InsertOpaquePredicates(BaseObfuscationPass):
    """Pass that decorates statements with opaque if‑guards to confuse static analysis."""

    def apply(self, ast):
        _OpaqueGuardAdder().inject(ast)
