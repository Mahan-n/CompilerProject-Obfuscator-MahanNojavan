from lexer_parser.ast_nodes import Assignment, Num, BinOp, Var, Compound, If, While
from obfuscation_passes.base_pass import BaseObfuscationPass  # external contract


class _CFGFlattener:
    """Convert linear statement sequences into a dispatcher‑based loop."""

    _STATE_VAR = "__sf"  # internal state variable name

    # --------------------------------------------------------------
    # Transformation entry point
    # --------------------------------------------------------------
    def flatten(self, ast_root):
        for fn in ast_root.functions:
            # ORIGINAL statements
            seq = fn.body.statements
            if not seq:
                continue

            # Build dispatcher table
            idx_range = list(range(len(seq)))
            stmt_table = {idx: stmt for idx, stmt in enumerate(seq)}

            # 1) Initialize state variable to 0
            flattened = [Assignment(self._STATE_VAR, Num(0))]

            # 2) Construct loop body with per‑state if‑clauses
            cases = []
            for idx in idx_range:
                cond = BinOp(Var(self._STATE_VAR), "==", Num(idx))
                next_idx = idx + 1 if idx + 1 < len(idx_range) else -1
                jump_stmt = Assignment(self._STATE_VAR, Num(next_idx))
                cases.append(If(cond, Compound([stmt_table[idx], jump_stmt]), None))

            loop_guard = BinOp(Var(self._STATE_VAR), "!=", Num(-1))
            flatten_loop = While(loop_guard, Compound(cases))
            flattened.append(flatten_loop)

            # Replace function body
            fn.body.statements = flattened
        return ast_root


# ------------------------------------------------------------------
# Public wrapper for the pass manager
# ------------------------------------------------------------------
class FlattenControlFlow(BaseObfuscationPass):
    """Obfuscation pass: flattens structured control flow into a state machine."""

    def apply(self, ast):
        _CFGFlattener().flatten(ast)
