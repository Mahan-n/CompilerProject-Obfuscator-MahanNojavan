class CodeGenerator:
    def __init__(self):
        self.code = []

    def generate(self, node):
        method_name = f'gen_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_gen)
        return method(node)

    def generic_gen(self, node):
        raise Exception(f"No code generator for {type(node).__name__}")

    def gen_Program(self, node):
        for func in node.functions:
            self.generate(func)
        return '\n'.join(self.code)

    def gen_Function(self, node):
        params = ', '.join(f"int {name}" for _, name in node.params)
        self.code.append(f"int {node.name}({params}) {{")
        self.generate(node.body)
        self.code.append("}")

    def gen_Compound(self, node):
        for stmt in node.statements:
            self.generate(stmt)

    def gen_VarDecl(self, node):
        self.code.append(f"{node.vtype} {node.name};")

    def gen_Assignment(self, node):
        expr = self.generate(node.expr)
        self.code.append(f"{node.name} = {expr};")

    def gen_If(self, node):
        cond = self.generate(node.condition)
        self.code.append(f"if ({cond}) {{")
        self.generate(node.then_branch)
        self.code.append("}")
        if node.else_branch:
            self.code.append("else {")
            self.generate(node.else_branch)
            self.code.append("}")

    def gen_While(self, node):
        cond = self.generate(node.condition)
        self.code.append(f"while ({cond}) {{")
        self.generate(node.body)
        self.code.append("}")

    def gen_Return(self, node):
        expr = self.generate(node.expr)
        self.code.append(f"return {expr};")

    def gen_BinOp(self, node):
        left = self.generate(node.left)
        right = self.generate(node.right)
        return f"({left} {node.op} {right})"

    def gen_Num(self, node):
        return str(node.value)

    def gen_Var(self, node):
        return node.name

    def gen_Call(self, node):
        args = ', '.join(self.generate(arg) for arg in node.args)
        return f"{node.func_name}({args})"

