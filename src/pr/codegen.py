from lexer_parser.ast_nodes import *


class CCodeGenerator:
    """Generate C source code for the custom AST."""

    def __init__(self):
        self.code_lines = []  # Stores emitted lines of C code

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate_c_code(self, ast_root):
        """Return full C translation for the given AST root."""
        self.code_lines = []  # fresh buffer
        self._emit(ast_root)
        return '\n'.join(self.code_lines)

    # ------------------------------------------------------------------
    # Internal node dispatcher
    # ------------------------------------------------------------------
    def _emit(self, node, indent_lvl: int = 0):
        indent_str = '    ' * indent_lvl

        if isinstance(node, Program):
            for func_node in node.functions:
                self._emit(func_node)

        elif isinstance(node, Function):
            params_c = ', '.join([f"int {name}" for _, name in node.params])
            self.code_lines.append(f"int {node.name}({params_c}) {{")
            self._emit(node.body, indent_lvl + 1)
            self.code_lines.append("}")

        elif isinstance(node, Compound):
            for stmt in node.statements:
                self._emit(stmt, indent_lvl)

        elif isinstance(node, VarDecl):
            self.code_lines.append(f"{indent_str}int {node.name};")

        elif isinstance(node, Assignment):
            rhs = self._expr_to_c(node.expr)
            self.code_lines.append(f"{indent_str}{node.name} = {rhs};")

        elif isinstance(node, If):
            cond_c = self._expr_to_c(node.condition)
            self.code_lines.append(f"{indent_str}if ({cond_c}) {{")
            self._emit(node.then_branch, indent_lvl + 1)
            self.code_lines.append(f"{indent_str}}}")
            if node.else_branch:
                self.code_lines.append(f"{indent_str}else {{")
                self._emit(node.else_branch, indent_lvl + 1)
                self.code_lines.append(f"{indent_str}}}")

        elif isinstance(node, While):
            cond_c = self._expr_to_c(node.condition)
            self.code_lines.append(f"{indent_str}while ({cond_c}) {{")
            self._emit(node.body, indent_lvl + 1)
            self.code_lines.append(f"{indent_str}}}")

        elif isinstance(node, Return):
            ret_c = self._expr_to_c(node.expr)
            self.code_lines.append(f"{indent_str}return {ret_c};")

    # ------------------------------------------------------------------
    # Expression helpers
    # ------------------------------------------------------------------
    def _expr_to_c(self, expr):
        """Translate an expression AST node into C source."""
        if isinstance(expr, BinOp):
            left_c = self._expr_to_c(expr.left)
            right_c = self._expr_to_c(expr.right)
            return f"({left_c} {expr.op} {right_c})"
        elif isinstance(expr, Num):
            return str(expr.value)
        elif isinstance(expr, Var):
            return expr.name
        elif isinstance(expr, Call):
            args_c = ', '.join([self._expr_to_c(arg) for arg in expr.args])
            return f"{expr.func_name}({args_c})"
        else:
            return "/* unsupported expression */"
