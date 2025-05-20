import random
from .base_pass import BaseObfuscationPass  # keep external reference intact


class _NameMint:
    """Generate unique identifiers with a simple numeric suffix."""

    def __init__(self):
        self._taken = set()

    def mint_name(self, prefix: str = "var") -> str:
        while True:
            candidate = f"{prefix}{random.randint(100, 999)}"
            if candidate not in self._taken:
                self._taken.add(candidate)
                return candidate


class _IdScrambler:
    """Traverse the AST and rename variable/function identifiers."""

    def __init__(self):
        self._lookup = {}
        self._mint = _NameMint()

    # --------------------------------------------------------------
    # Public dispatcher
    # --------------------------------------------------------------
    def scramble(self, node):
        method_name = f"scramble_{type(node).__name__}"
        handler = getattr(self, method_name, self._scramble_generic)
        return handler(node)

    # --------------------------------------------------------------
    # Generic walker (fallback)
    # --------------------------------------------------------------
    def _scramble_generic(self, node):
        # Skip primitives without __dict__ (e.g., Num)
        if not hasattr(node, "__dict__"):
            return node

        for attr, val in vars(node).items():
            if isinstance(val, list):
                for idx, item in enumerate(val):
                    if hasattr(item, "__class__"):
                        val[idx] = self.scramble(item)
            elif hasattr(val, "__class__"):
                setattr(node, attr, self.scramble(val))
        return node

    # --------------------------------------------------------------
    # Node‑specific handlers
    # --------------------------------------------------------------
    def scramble_Program(self, node):
        node.functions = [self.scramble(fn) for fn in node.functions]
        return node

    def scramble_Function(self, node):
        node.name = self._new_id(node.name, prefix="func")
        node.params = [(typ, self._new_id(name)) for typ, name in node.params]
        node.body = self.scramble(node.body)
        return node

    def scramble_VarDecl(self, node):
        node.name = self._new_id(node.name)
        return node

    def scramble_Assignment(self, node):
        node.name = self._new_id(node.name)
        node.expr = self.scramble(node.expr)
        return node

    def scramble_Var(self, node):
        node.name = self._new_id(node.name)
        return node

    def scramble_Call(self, node):
        node.func_name = self._new_id(node.func_name)
        node.args = [self.scramble(arg) for arg in node.args]
        return node

    # --------------------------------------------------------------
    # Helper
    # --------------------------------------------------------------
    def _new_id(self, original: str, prefix: str = "v") -> str:
        if original not in self._lookup:
            self._lookup[original] = self._mint.mint_name(prefix)
        return self._lookup[original]


# ------------------------------------------------------------------
# Public wrapper expected by the obfuscator’s pass manager
# ------------------------------------------------------------------
class RenameVariables(BaseObfuscationPass):
    """Obfuscation pass that hides original identifiers by renaming them."""

    def apply(self, ast):
        _IdScrambler().scramble(ast)
