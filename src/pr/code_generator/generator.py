from lexer_parser.ast_nodes import *  # noqa: F401,F403


class MiniCEmitter:
    """Emit C code from the AST. Obfuscated naming version."""

    def __init__(self):
        self._lines: list[str] = []  # collected source lines

    # ------------------------------------------------------------------
    # Public driver
    # ------------------------------------------------------------------
    def emit(self, node):
        """Return C translation for *node* (expected: Program root)."""
        self._dispatch(node)
        return "\n".join(self._lines)

    # ------------------------------------------------------------------
    # Internal dispatch
    # ------------------------------------------------------------------
    def _dispatch(self, node):
        handler_name = f"_on_{type(node).__name__}"
        handler = getattr(self, handler_name, self._on_unknown)
        return handler(node)

    # ------------------------------------------------------------------
    # Handlers for each AST node type
    # ------------------------------------------------------------------
    def _on_unknown(self, node):
        raise RuntimeError(f"No emitter implemented for {type(node).__name__}")

    def _on_Program(self, node: Program):  # noqa: N802
        for fn in node.functions:
            self._dispatch(fn)

    def _on_Function(self, node: Function):  # noqa: N802
        param_str = ", ".join(f"int {n}" for _, n in node.params)
        self._lines.append(f"int {node.name}({param_str}) {{")
        self._dispatch(node.body)
        self._lines.append("}")

    def _on_Compound(self, node: Compound):  # noqa: N802
        for st in node.statements:
            self._dispatch(st)

    def _on_VarDecl(self, node: VarDecl):  # noqa: N802
        self._lines.append(f"{node.vtype} {node.name};")

    def _on_Assignment(self, node: Assignment):  # noqa: N802
        rhs = self._dispatch(node.expr)
        self._lines.append(f"{node.name} = {rhs};")

    def _on_If(self, node: If):  # noqa: N802
        cond_code = self._dispatch(node.condition)
        self._lines.append(f"if ({cond_code}) {{")
        self._dispatch(node.then_branch)
        self._lines.append("}")
        if node.else_branch:
            self._lines.append("else {")
            self._dispatch(node.else_branch)
            self._lines.append("}")

    def _on_While(self, node: While):  # noqa: N802
        cond_code = self._dispatch(node.condition)
        self._lines.append(f"while ({cond_code}) {{")
        self._dispatch(node.body)
        self._lines.append("}")

    def _on_Return(self, node: Return):  # noqa: N802
        val = self._dispatch(node.expr)
        self._lines.append(f"return {val};")

    # ------------------------------------------------------------------
    # Expression helpers (return strings, do not write to _lines)
    # ------------------------------------------------------------------
    def _on_BinOp(self, node: BinOp):  # noqa: N802
        lhs = self._dispatch(node.left)
        rhs = self._dispatch(node.right)
        return f"({lhs} {node.op} {rhs})"

    def _on_Num(self, node: Num):  # noqa: N802
        return str(node.value)

    def _on_Var(self, node: Var):  # noqa: N802
        return node.name

    def _on_Call(self, node: Call):  # noqa: N802
        args_code = ", ".join(self._dispatch(a) for a in node.args)
        return f"{node.func_name}({args_code})"
