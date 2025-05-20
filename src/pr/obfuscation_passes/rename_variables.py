import random
import string
from .base_pass import BaseObfuscationPass  # make sure this exists and is correct


class NameGenerator:
    def __init__(self):
        self.used_names = set()

    def generate_name(self, prefix='var'):
        while True:
            name = f"{prefix}{random.randint(100, 999)}"
            if name not in self.used_names:
                self.used_names.add(name)
                return name


class Renamer:
    def __init__(self):
        self.name_map = {}
        self.generator = NameGenerator()

    def rename(self, node):
        method_name = f'rename_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_rename)
        return method(node)

    def generic_rename(self, node):
        # Only apply vars() to things that are objects with a __dict__
        if not hasattr(node, '__dict__'):
            return node  # Skip things like Num, which are basic data structures

        for attr in vars(node):
            value = getattr(node, attr)
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if hasattr(item, '__class__'):
                        value[i] = self.rename(item)
            elif hasattr(value, '__class__'):
                setattr(node, attr, self.rename(value))
        return node

    def rename_Program(self, node):
        node.functions = [self.rename(fn) for fn in node.functions]
        return node

    def rename_Function(self, node):
        if node.name not in self.name_map:
            self.name_map[node.name] = self.generator.generate_name("func")
        node.name = self.name_map[node.name]
        node.params = [(typ, self._rename_id(name)) for typ, name in node.params]
        node.body = self.rename(node.body)
        return node

    def rename_VarDecl(self, node):
        node.name = self._rename_id(node.name)
        return node

    def rename_Assignment(self, node):
        node.name = self._rename_id(node.name)
        node.expr = self.rename(node.expr)
        return node

    def rename_Var(self, node):
        node.name = self._rename_id(node.name)
        return node

    def rename_Call(self, node):
        node.func_name = self._rename_id(node.func_name)
        node.args = [self.rename(arg) for arg in node.args]
        return node

    def _rename_id(self, name):
        if name not in self.name_map:
            self.name_map[name] = self.generator.generate_name("v")
        return self.name_map[name]


# ✅ This is the wrapper expected by your obfuscator
class RenameVariables(BaseObfuscationPass):
    def apply(self, ast):
        renamer = Renamer()
        renamer.rename(ast)
